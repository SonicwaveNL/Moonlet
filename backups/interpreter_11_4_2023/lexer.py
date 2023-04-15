import re
import copy

from functools import reduce
from typing import List, Union, Tuple
from pprint import pprint, pp
from . import tokens
# from .tokens import Tab, Token, TokenTypes, Undefined, Integer, Float, String

# def unwrapper(input, indentations=-1):

#     if isinstance(input,  list) or isinstance(input, tuple):
#         tabs = '\t' * indentations
#         print(f"{tabs}{input}")
#         unwrapper(input[0], indentations + 1)

#     else:
#         tabs = '\t' * indentations
#         print(f"{tabs}{input}")

    # if isinstance(input, list) and len(input) != 0:
        
    #     unwrapper(input[0], indentations+1)

    # elif isinstance(input, tuple):
    #     unwrapper(input[0], indentations+1)
    #     unwrapper(input[1], indentations+1)

    # else:
    #     tabs = '\s' * (indentations - 2)
    #     print(f"{tabs}{input}")

class Lexer:
    """Represents the Lexer of the Interpeter.

    The Lexer scans the lines within the document
    to convert the lines to the matching TokenTypes.
    """

    def __init__(self, file_input):
        self.input = file_input
        self.token_data_types = tokens.TokenTypes.DATA_TYPES.value
        self.token_operations = tokens.TokenTypes.OPERATIONS.value
        self.token_comparisons = tokens.TokenTypes.COMPARISONS.value
        self.line = 0

    def __str__(self) -> str:
        return "Lexer()"

    def new_convert_to_tokens(self, arg_input):

        if arg_input is None:
            return None
        
        # elif len(arg_input) == 1:
        #     return (None, None, None, None)

        match = self.new_match_arguments(
            arg_input,
            self.token_data_types + self.token_comparisons + self.token_operations,
        )

        self.line += 1
        print(f" LINE({self.line}):\t'{arg_input}'\n   TOKN:\t{match[0]}\n   ARGS:\t{match[1]}\n")

        return (match[0], match[1], arg_input, self.line)

    def new_match_arguments(self, args_input, tokens_input):

        value = reduce(
            lambda x, y: x if x[1] is not None else y,
            map(lambda x: (x, self.new_match_token(args_input, x)), tokens_input),
        )

        # print(f' VALUE{value}')

        # If it's still undefined/unknown, try again as it might 
        # has an tab in front of the Token we're looking for.
        if value[0] == tokens.Undefined:
            new_args = args_input.lstrip(' ')
            new_value = reduce(
                lambda x, y: x if x[1] is not None else y,
                map(lambda x: ((tokens.Tab, x), self.new_match_token(new_args, x)), tokens_input),
            )

            # If the token has been found, assign it as the value
            # otherwise, try to check if it's just an 'EmptyLine'
            if new_value[0][1] != tokens.Undefined:
                value = new_value

            else:
                new_value = self.new_match_token(args_input, tokens.EmptyLine)
                if new_value != tokens.Undefined:
                    value = (tokens.EmptyLine, {})

        if len(args_input) == 1:
            return value[0], value[1]

        return value[0], value[1]

    def new_match_token(self, str_input, operation):

        if isinstance(operation, object):
            operation = operation()
            pattern = re.compile(operation.expr)
            match = re.match(pattern, str_input)

            if match is not None:
                if len(operation.args) >= 1:
                    found_args = self.new_unwrap_args(match, operation.args, {})
                    return found_args

                return self.match_data_type(str_input) if match is not None else None

        return None

    def new_unwrap_args(self, match, arguments, values={}):

        if len(arguments) == 0:
            return values

        if arguments[0] == 'params':
            values[arguments[0]] = match.group('params').replace(' ', '').split(',')

        elif arguments[0] == 'action':
            print('TAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADAAA')
            output = self.new_convert_to_tokens(match.group('action'))
            print(f'OUTPUT:{output}')
            values['action'] = output

        # elif arguments[0] != 'operation':
            # values['operation'] = 

        elif arguments[0] != 'name':
            values[arguments[0]] = self.match_data_type(match.group(arguments[0])) if arguments[0] is not None else None

        else:
            values[arguments[0]] = match.group('name') if arguments[0] is not None else None

        if len(arguments) == 1:
            return values

        return self.new_unwrap_args(match, arguments[1:], values)

    def scan(self):

        print('\nLINES\n==============')
        file_lines = self.convert_to_lines(self.input)

        # Remove empty newlines
        # file_lines = list(filter(None, file_lines))
        pprint(file_lines)

        # print('\nMAPPED PARTS\n==============')
        # file_parts = list(map(self.convert_to_parts, file_lines))
        # pprint(file_parts)

        # print('\nTO TOKENS\n==============')
        # file_tokens = list(map(self.convert_to_tokens, file_parts))
        # pprint(file_tokens)

        print('\nTO TOKENS\n==============')
        file_tokens = self.scan_line(file_lines)
        # file_tokens = list(map(self.convert_to_tokens, file_lines))
        # file_tokens = list(map(self.new_convert_to_tokens, file_lines))

        # print(f'FILE_TOKENS: ')
        # pprint(file_tokens)

        return file_lines, file_lines, file_tokens

    def scan_line(self, lines):
        
        if len(lines) == 0:
            return [None]

        value = copy.deepcopy([self.new_convert_to_tokens(lines[0])])
        
        if len(lines) == 1:
            return value

        return value + self.scan_line(lines[1:])

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
        # value = reduce(
        #     lambda x, y: x if x[1] is not None else y,
        #     map(lambda x: (x, self.match_token(args_input[0], x)), tokens),
        # )
        value = reduce(
            lambda x, y: x if x[1] is not None else y,
            map(lambda x: (x, self.match_token(args_input, x)), tokens),
        )

        print(f'\t{value}')

        # If it's still undefined/unknown, try again as it might 
        # has an tab in front of the Token we're looking for.
        if value[0] == tokens.Undefined and isinstance(args_input[0], str):
    
            new_args = args_input[0].replace('\t', '')
            new_value = reduce(
                lambda x, y: x if x[1] is not None else y,
                map(
                    lambda x: (
                        (tokens.Tab, x), self.match_token(new_args, x)
                    ), tokens
                ),
            )

            if new_value[0][1] != tokens.Undefined:
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

        print(f"  TRY_MATCH:\t{str_input}")

        try:
            return int(str_input), tokens.Integer

        except ValueError:
            try:
                return float(str_input), tokens.Float

            except ValueError:
                if 'true' in str_input or 'false' in str_input:
                    return str_input, tokens.Boolean

                return str_input, tokens.String
