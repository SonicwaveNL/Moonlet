import os
from typing import Optional
from .lexer import Lexer
from .parser import Parser
from .program import Program, Scope
from .errors import Error, FileNotFoundError

class Launcher:
    """Controller of the Moonlet language.
    
    Attributes:
        file_path: Direct path to the Moonlet file.
        input_file: Opened file bytes, using the 'file_path'.
        
    """

    def __init__(self, file_path: Optional[str] = None, debug_mode: bool = False, test_mode = False) -> None:
        """Initialise the Launcher with given file.

        Args:
            file_path: Direct path to file. Defaults to None.
            debug_mode: If 'debug_mode' is enabled. Defaults to False.
            test_mode: If 'test_mode' is enabled. Defaults to False.
        """        
        self.file_path = file_path
        self.debug_mode = debug_mode
        self.test_mode = test_mode

        if file_path is not None and len(file_path) > 0:

            # Check if the given 'file_path' even exists
            if not os.path.exists(file_path):
                print(FileNotFoundError(f"Couldn't find '{file_path}', no such file."))

            # Also check if the 'file_path' has the Moonlet extention
            elif not file_path.endswith('.mnl'):
                print(FileNotFoundError(f"File '{file_path}' has an invalid extention (must be '.mnl')"))

            else:
                self.run_moonlet()

        elif test_mode:
            print(f"{'TESTING':-^60}")

    def print_error(self, error: Error) -> None:
        """Print a given Error.

        Args:
            error: The Error to print.
        """        

        file_line = f"In file '{self.file_path}', line {error.pos.line}"
        file_line += f", from {error.pos.start}" if error.pos.start else ""
        file_line += f" to {error.pos.end}" if error.pos.end else ""

        if self.debug_mode: print(f"{'ERROR':=^60}")
        print(f"\nMoonlet — Traceback ({type(error).__name__}):")
        print(f"    {file_line}")
        print(error)

    def run_moonlet(self):
        """Launch the Moonlet steps."""        

        # Run the Lexer to generate the 'tokens'
        input_file = open(self.file_path, 'r').read()
        
        if self.debug_mode: print(f"{'LEXER':-^60}")
        
        lexer = Lexer(input_file, self.debug_mode)
        tokens, lexer_error = lexer.run()

        # Check for potential errors caused 
        # during the lexing process of the file 
        if lexer_error is not None: return self.print_error(lexer_error)
        
        # Run the Parser to generate the 'AST'
        if self.debug_mode: print(f"{'PARSER':-^60}")
        parser = Parser(tokens, self.debug_mode)
        ats = parser.parse()

        # Check for potential errors caused 
        # during the parsing process of the tokens 
        if ats.error is not None: return self.print_error(ats.error)

        # Runt the Program/Interpreter to handle
        # the nodes created within the ATS
        if self.debug_mode: print(f"{'PROGRAM':-^60}")
        prog = Program(self.debug_mode)
        prog_scope = Scope(name="<Program>", origin=ats.node)
        prog_result = prog.exec(ats.node, prog_scope)

        # Check for potential errors caused 
        # during the execution process of the Program
        if prog_result.error is not None: return self.print_error(prog_result.error)
        
        if self.debug_mode:
            print('')
            print(f"{'='*60}")
            print(f"{'RESULT_PROGRAM:': <30} {str(prog_scope.format_args()): <50}")