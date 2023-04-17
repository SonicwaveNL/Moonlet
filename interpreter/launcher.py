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
        print(f"\nLEXER\n{'='*61}")
        self.tokens, self.error = self.lexer.run()

        if self.error is not None:
            print(self.error)
            return
        
        print(f"{'TOKENS': <20} | {'VALUE': ^10} | {'LINE': ^7} | {'START': ^7} | {'END': >5}")
        print(f"{'='*61}")

        line = 0
        for token in self.tokens:

            if line != token.pos.line:
                print(f"{'-'*61}\n", end='')
                line = token.pos.line

            print(f"{token.__class__.__name__: <20} | {repr(token.value): ^10} | {token.pos.line: ^7} | {token.pos.start: ^7} | {token.pos.end: >5}")

        # Run the Parser to generate the 'AST'
        print(f"\nPARSER\n{'='*61}")
        parser = Parser(self.tokens)
        ats = parser.parse()

        if ats.error is not None: 
            print(ats.error)
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
            print(f"\n{prog_result.error}")
            print(f"{'='*61}")

        print(prog_scope.format_args())
        # print(prog_scope)