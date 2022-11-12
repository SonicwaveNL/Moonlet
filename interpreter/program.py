from enum import Enum
from functools import reduce
from typing import List, Union, Tuple

from .tokens import Token, TokenTypes
from .lexer import Lexer
from .parser import Parser

from pprint import pprint, pp


class Program:
    """Represents the Program of the Interpeter.

    The Program reads the AST (abstract syntax tree)
    created by the Parser and executes it.
    """

    def __init__(self, file_path):
        self.state = -1
        self.errors = []
        self.current_line = 0
        self.instructions = []

        # Try to open the file
        self.file_path = file_path
        self.input_file = open(file_path, 'r').read()
        
        # Init the Lexer and scan the file
        self.lexer = Lexer(self.input_file)
        self.lines, self.parts, self.tokens = self.lexer.scan()

        # Init the Parser
        self.parser = Parser()

    def __str__(self):
        return "Program()"

    def run(self):
        
        print('\nPARSER\n==============')
        self.completed, self.current_line, self.errors = self.parser.parse(self.tokens)

        if not self.completed:
            error_line = self.lines[self.current_line - 1]
            self.errors = ",\n".join(self.errors)

            print(f'\nMOONLET Program interupted - line {self.current_line}, in file "{self.file_path}"')
            print(f'  {error_line}\nError: "{self.errors}"')
            # print('  {}\nError: "{}"'.format(error_line.strip('\t'), self.errors))
            print(f'{self.parser}')
            print('\nBREAK\n==============')

        else:
            # {
            #     'line': self.parser.line,
            #     'errors': self.
            # }
            print(self.parser)
            print('\nDONE!\n==============')