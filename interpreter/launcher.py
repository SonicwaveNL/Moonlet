from .lexer import Lexer
from .parser import Parser
from .program import Program, Scope

class Launcher:

    def __init__(self, file_path):
        self.file_path = file_path

        # Try to open the file
        self.file_path = file_path
        self.input_file = open(file_path, 'r').read()

        # Init the Lexer with the 'input_file'
        self.lexer = Lexer(self.input_file)

        # Define the placeholder for
        # the 'tokens' and any 'error'
        self.tokens, self.error = None, None

    def run(self):

        # Run the Lexer to generate the 'tokens'
        print(f"\nLEXER\n{'='*60}")
        self.tokens, self.error = self.lexer.run()

        if self.error is not None:
            print(f"{self.error.type}: {self.error.details}")
            return
        
        print(f"{'TOKENS': <15}", end=' | ')
        print(f"{'VALUE': ^12}", end=' | ')
        print(f"{'LINE': ^7}", end=' | ')
        print(f"{'START': ^7}", end=' | ')
        print(f"{'END': >5}")
        print(f"{'='*60}")

        line = 0
        for token in self.tokens:

            if line != token.pos.line:
                print(f"{'-'*60}\n", end='')
                line = token.pos.line

            print(f"{token.type: <15}", end=' | ')
            print(f"{token.format_value(): ^12}", end=' | ')
            print(f"{token.pos.line: ^7}", end=' | ')
            print(f"{token.pos.start: ^7}", end=' | ')
            print(f"{token.pos.end: >5}")

        # Run the Parser to generate the 'AST'
        print(f"\nPARSER\n{'='*60}")
        parser = Parser(self.tokens)
        ats = parser.parse()

        if ats.error is not None: 
            print(f"{'='*60}")
            print(f"{ats.error.type}: {ats.error.details}")
        
        # print(f"{ats.node}")
        print(f"\n{'='*60}")
        print(f"{'NODES': <60}")
        print(f"{'='*60}")

        if ats.node is not None:
            for sub_node in ats.node.items:
                for name, value in sub_node.__dict__.items():

                    if name == 'args' or name == 'body':
                        print(f"{name: <15}")
                        for item in value:
                            print(f"{' '*15}", end=' ')
                            print(f"{str(item): <45}")
                    
                    else:
                        print(f"{name: <15}", end=' ')
                        print(f"{str(value): <45}")                    
                
                print(f"{'-'*60}\n", end='')
                
                # print(f"{node.type: <15}", end=' | ')
                # print(f"{node}")

        # Run the Interpeter to execute the 'AST'
        print(f"\nPROGRAM\n{'='*60}")
        main_scope = Scope("<Program>")

        prog = Program()
        prog_result = prog.exec(ats.node, main_scope)

        if prog_result.error is not None:
            print(f"\n{prog_result.error.type}: {prog_result.error.details}")
            print(f"{'='*60}")