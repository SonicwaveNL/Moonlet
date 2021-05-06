from functools import reduce
from typing import List, Tuple
from enum import Enum
import re

from .tokens import Token, TokenType


class Lexer:
    """Represents the Lexer of the Interpeter.

    The Lexer scans the lines within the document
    to convert the lines to the matching TokenTypes.
    """

    def __init__(self, file_input):
        self.input = file_input
        self.token_types = TokenType.items()
        # self.token_functions = TokenType.TOKEN_FUNCTIONS.value


    def __str__(self) -> str:
        return "Lexer()"


    # convert_to_lines :: str -> [str]
    def convert_to_lines(self, str_input: str) -> List[str]:
        """Convert a given `str` input to lines
        
        This function converts the given input string to
        a list of strings, each item in the list is a line
        derived from the input string.

        Args:
            - str_input (str): The input string.

        Return:
            a list of strings, containing the lines.

        """
        return str_input.split('\n')


    # convert_to_parts :: str -> [str]
    def convert_to_parts(self, str_input: str) -> List[str]:
        """Convert a given `str` input to parts
        
        This function converts the given input string to
        a list of string parts, each item in the list is a part
        derived from the input string.

        Args:
            - str_input (str): The input string.

        Return:
            a list of strings, containing each parts.

        """
        return str_input.split(' ')


    # convert_to_tokens :: [[str]] -> [[(Token)]]
    def convert_to_tokens(self, parts_input: List[List[str]]) -> List[List[Tuple[Token]]]:
        """Convert given list of parts to a list of Tokens.
        
        This function converts the given input list of strings
        to a list of associated tokens.

        Args:
            - parts_input (list): The list of parts.

        Return:
            A list of parts, which each part contains a tuple
            of associated token.

        """
        if not parts_input:
            return list()

        return list(map(self.match_token, parts_input))


    # match_token :: str -> (Token)
    def match_token(self, str_input) -> Tuple[Token]:



        return 

