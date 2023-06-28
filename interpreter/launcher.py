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
        self.file_path = file_path
        self.debug_mode = debug_mode
        self.test_mode = test_mode

        if file_path is not None:

            # Check if the given 'file_path' even exists
            if not os.path.exists(file_path):
                print(FileNotFoundError(f"Couldn't find '{file_path}', no such file."))

            # Also check if the 'file_path' has the Moonlet extention
            elif not file_path.endswith('.mnl'):
                print(FileNotFoundError(f"File '{file_path}' has an invalid extention (must be '.mnl')"))

            else:
                self.old_run_moonlet()

        elif test_mode:
            pass

    def print_error(self, error: Error) -> None:

        file_line = f"In file '{self.file_path}', line {error.pos.line}"
        file_line += f", from {error.pos.start}" if error.pos.start else ""
        file_line += f" to {error.pos.end}" if error.pos.end else ""

        print(f"\nMoonlet — Traceback ({type(error).__name__}):")
        print(f"    {file_line}")
        print(error)

    def run_moonlet(self):

        # Run the Lexer to generate the 'tokens'
        input_file = open(self.file_path, 'r').read()
        lexer = Lexer(text=input_file)
        tokens, lexer_error = lexer.run()

        # Check for potential errors caused 
        # during the lexing process of the file 
        if lexer_error is not None: return print(lexer_error)
        
        # Run the Parser to generate the 'AST'
        parser = Parser(tokens)
        ats = parser.parse()

        # Check for potential errors caused 
        # during the parsing process of the tokens 
        if ats.error is not None: return print(ats.error)

        # Runt the Program/Interpreter to handle
        # the nodes created within the ATS
        prog = Program()
        prog_scope = Scope(name="<Program>", origin=ats.node)
        prog_result = prog.exec(ats.node, prog_scope)

        # Check for potential errors caused 
        # during the execution process of the Program
        if prog_result.error is not None: return print(f"{prog_result.error}")
        
        print(prog_scope.format_args())

    def old_run_moonlet(self):

        # Run the Lexer to generate the 'tokens'
        print(f"\nLEXER\n{'='*61}")
        input_file = open(self.file_path, 'r').read()
        lexer = Lexer(text=input_file)
        tokens, lexer_error = lexer.run()

        if lexer_error is not None: return self.print_error(lexer_error)
        
        print(f"{'TOKENS': <20} | {'VALUE': ^10} | {'LINE': ^7} | {'START': ^7} | {'END': >5}")
        print(f"{'='*61}")

        line = 0
        for token in tokens:

            if line != token.pos.line:
                print(f"{'-'*61}\n", end='')
                line = token.pos.line

            print(f"{token.__class__.__name__: <20} | {repr(token.value): ^10} | {token.pos.line: ^7} | {token.pos.start: ^7} | {token.pos.end: >5}")

        # Run the Parser to generate the 'AST'
        print(f"\nPARSER\n{'='*61}")
        parser = Parser(tokens)
        ats = parser.parse()

        if ats.error is not None: 
            self.print_error(ats.error)
            return
        
        # print(f"{ats.node}")
        print(f"\n{'='*61}")
        print(f"{'NODES': <61}")
        print(f"{'='*61}")

        if ats.node is not None:
            for sub_node in ats.node.items:
                for name, value in sub_node.__dict__.items():

                    if name == 'args' or name == 'body':
                        print(f"{name: <15}")
                        for item in value.items:
                            print(f"{' '*15}", end=' ')
                            print(f"{str(item): <45}")
                    
                    else:
                        print(f"{name: <15}", end=' ')
                        print(f"{str(value): <45}")                    
                
                print(f"{'-'*61}\n", end='')
                
                # print(f"{node.type: <15}", end=' | ')
                # print(f"{node}")

        # Run the Interpeter to execute the 'AST'
        print(f"\nPROGRAM\n{'='*61}")
        prog = Program()
        prog_scope = Scope(name="<Program>", origin=ats.node)
        prog_result = prog.exec(ats.node, prog_scope)

        if prog_result.error is not None:
            self.print_error(prog_result.error)
            # print(f"{'='*61}")

        print(f"{'='*61}")
        print(prog_scope.format_args())
        # print(prog_scope)