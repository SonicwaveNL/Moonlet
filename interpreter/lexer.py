import re

from functools import reduce
from typing import List, Union, Tuple
from pprint import pprint, pp

from .tokens import Tab, Token, TokenTypes, Undefined


class Lexer:
    """Represents the Lexer of the Interpeter.

    The Lexer scans the lines within the document
    to convert the lines to the matching TokenTypes.
    """

    def __init__(self, file_input):
        self.input = file_input
        self.token_data_types = TokenTypes.DATA_TYPES.value
        self.token_operations = TokenTypes.OPERATIONS.value
        self.token_comparisons = TokenTypes.COMPARISONS.value

    def __str__(self) -> str:
        return "Lexer()"

    def scan(self):

        print('\nLINES\n==============')
        file_lines = self.convert_to_lines(self.input)
        file_lines = list(filter(None, file_lines))
        pprint(file_lines)

        print('\nMAPPED PARTS\n==============')
        file_parts = list(map(self.convert_to_parts, file_lines))
        pprint(file_parts)

        print('\nTO TOKENS\n==============')
        file_tokens = list(map(self.convert_to_tokens, file_parts))
        pprint(file_tokens)

        return file_lines, file_parts, file_tokens

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

        return str_input.split("\n")

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

        str_input = self.handle_parentheses(str_input)
        parts = str_input.split(" ")
        parts = list(filter(None, parts))
        return parts

    # handle_parentheses :: str -> str
    def handle_parentheses(self, str_input: str) -> str:

        result = re.sub(r"\,", "", str_input)
        result = re.sub(r"\(", "( ", result)
        result = re.sub(r"\)", " )", result)
        return result
       
    # convert_to_tokens :: [str] -> () or None
    def convert_to_tokens(self, parts_input: List[str]) -> Union[tuple, None]:
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
            return None

        elif len(parts_input) == 1:
            return (None, None)

        arguments = self.match_arguments(
            parts_input,
            self.token_data_types + self.token_comparisons + self.token_operations,
        )

        return (arguments[0], arguments[1:])

    def match_arguments(self, args_input, tokens) -> Union[list, None]:

        # Try to match the args with any token
        value = reduce(
            lambda x, y: x if x[1] is not None else y,
            map(lambda x: (x, self.match_token(args_input[0], x)), tokens),
        )

        # If it's still undefined/unknown, try again as it might 
        # has an tab in front of the Token we're looking for.
        if value[0] == Undefined and isinstance(args_input[0], str):
    
            new_args = args_input[0].replace('\t', '')
            new_value = reduce(
                lambda x, y: x if x[1] is not None else y,
                map(
                    lambda x: (
                        (Tab, x), self.match_token(new_args, x)
                    ), tokens
                ),
            )

            if new_value[0][1] != Undefined:
                value = new_value

        if len(args_input) == 1:
            return [value]

        return [value] + self.match_arguments(args_input[1:], tokens)

    def match_token(self, str_input, operation) -> Union[str, None]:

        if isinstance(operation, object):
            operation = operation()
            pattern = re.compile(operation.expr)
            match = re.fullmatch(pattern, str_input)

            return self.match_data_type(str_input) if match is not None else None

        return None

    def match_data_type(self, str_input):

        try:
            return int(str_input)

        except ValueError:

            try:
                return float(str_input)

            except ValueError:
                return str_input
