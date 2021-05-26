from enum import Enum
from functools import reduce
from pprint import pprint
from typing import List, Union, Tuple

from . import tokens as Tokens


class Parser:
    """Represents the Parser of the Interpeter.

    The Parser reads the given Tokens, and convert it to
    an AST (abstract syntax tree) that is executable.

    TODO:
        - [ ] Create: Return value of function
        - [ ] Create: Set variable on function returned value
        - [ ] Create: Increment value
        - [ ] Create: Decrement value
        - [ ] Create: Print function
        - [ ] Create: Comment function
        - [ ] Edit: Rename Goto -> Call
    """

    def __init__(self):
        self.line = 0
        self.errors = []
        self.function = None
        self.variables = {}
        self.instructions = {}
        self.tokens = None

    def __str__(self):
        return "\nParser(\n\tline: {}\n\tfunction: {}\n\tvars: {}\n\tinstructions: {}\n)".format(self.line, self.function, self.variables, self.instructions)

    # REMOVE THIS - Dev function
    def line_follower(self, instruction, args):

        print('{}) >> {}'.format(self.line, instruction[1]), end=' ')

        for arg in args:
            print('{} '.format(arg[1]), end='')

        print('')

    def parse(self, tokens):

        # Save a copy of the tokens for function/line jumps
        if not self.tokens:
            self.tokens = tokens

        # Check if parsing is at the end of the tokens
        if not tokens:
            return True, self.line, self.errors

        # Check if the parsing has enough information
        # to conintue with the parsing
        elif len(tokens[0]) == 2:

            self.line += 1
            success, message = self.parse_line(tokens[0][0], tokens[0][1])

            # REMOVE THIS - Dev function
            self.line_follower(tokens[0][0], tokens[0][1])

            if success:
                return self.parse(tokens[1:])

            else:
                return False, self.line, self.errors + [message]

        else:
            return False, self.line, self.errors + ['Invalid operation at line {}'.format(self.line + 1)]

    def parse_line(self, instruction, args):

        if isinstance(instruction[0], tuple):

            # Define the place where the result needs to be stored
            if instruction[0][0] == Tokens.Tab and not self.function:
                return False, "Indented Token at line {} is not a member of any function"
            
            elif not self.function:
                return False, "Trying to access a function that doesn't exist?"

            else:
                place = self.instructions[self.function]
                place['inline'] += [(instruction, args)]

            # Try to match the right Token
            if instruction[0][0] == Tokens.Tab and instruction[0][1] == Tokens.Variable:
                return self.set_variable(args, place=place)

            elif instruction[0][0] == Tokens.Tab and instruction[0][1] == Tokens.If:
                return self.check_if_statement(args, place=place)

            elif instruction[0][0] == Tokens.Tab and instruction[0][1] == Tokens.Goto:
                return self.increment_value(args, place=place)

            elif instruction[0][0] == Tokens.Tab and instruction[0][1] == Tokens.Return:
                return self.return_function(args, place=place)

            elif instruction[0][0] == Tokens.Tab and instruction[0][1] == Tokens.Increment:
                return self.increment_value(args, place=place)

            elif instruction[0][0] == Tokens.Tab and instruction[0][1] == Tokens.Decrement:
                return self.decrement_value(args, place=place)

            elif instruction[0][0] == Tokens.Tab and instruction[0][1] == Tokens.Undefined:
                return self.undefined(args, place=place)

        else:

            # If no 'Tab' token is in front of the instruction,
            # then function var back
            self.function = None

            if instruction[0] == Tokens.Variable:
                return self.set_variable(args)

            elif instruction[0] == Tokens.Func:
                return self.create_function(args)

            elif instruction[0] == Tokens.If:
                return self.check_if_statement(args)

            elif instruction[0] == Tokens.Goto:
                return self.goto_function(args)

            elif instruction[0] == Tokens.Return:
                return self.return_function(args)

            elif instruction[0] == Tokens.Increment:
                return self.increment_value(args)

            elif instruction[0] == Tokens.Decrement:
                return self.decrement_value(args)

            elif instruction[0] == Tokens.Undefined:
                return self.undefined(args)

        return False, "Unknown Token at line {}".format(self.line)

    def set_variable(self, args, place=None):

        # Check if the input args has enough values
        # to set a name and a value for the var
        if len(args) < 2:
            return False, "Couldn't set Variable, invalid size"

        # Set the name and the value of the var
        var_name = str(args[0][1])
        var_value = args[1][1]

        # If a place was given (when witthin a function),
        # use that place to store the vars to prevent
        # global vars from beeing overrided.
        if place is not None and isinstance(place, dict):

            new_var = {var_name: var_value}

            if 'vars' in place:
                place['vars'] = {**place['vars'], **new_var}

            else:
                place['vars'] = new_var

        else:
            self.variables[var_name] = var_value

        return True, "Variable set"

    def get_variable(self, args, place=None):

        # Check if the input args has enough values
        # to do a variable lookup.
        if len(args) < 2:
            return None

        # If a place is given, try to retrieve 
        # the value from that place.
        if place and str(args[1]) in self.instructions['vars']:
            return self.instructions['vars'][str(args[1])]
            
        elif str(args[1]) in self.variables:
            return self.variables[args[1]]

        return args[1]

    def create_function(self, args):

        # Check if the input args has enough values
        # to set a name for the function
        if len(args[0]) < 2:
            return False, "Couldn't create function, invalid 'name' given"

        # Get the name of the function
        func_name = args[0][1]

        # Check if the function with name already exist
        if func_name in self.instructions:
            return False, "Couldn't create function, function '{}' already exist".format(func_name)

        else:

            # Check if the args include enough values to start
            # checking for open/closing parentheses
            if len(args) >= 5:

                # Try to create the parameters, and validate
                # if the args include both valid open/closing parentheses
                params, is_opened, is_closed = self.create_parameters(args[1:])

                if isinstance(params, str):
                    return False, params

                elif not params:
                    return False, "Invalid parameters definition for '{}' function, couldn't process format".format(func_name)

                elif not is_opened:
                    return False, "No '(' Open parentheses found for function with name '{}'".format(func_name)

                elif not is_closed:
                    return False, "No ')' Closing parentheses found for function with name '{}'".format(func_name)

                else:
                    self.function = func_name
                    self.instructions[func_name] = {'line': self.line, 'inline': [], 'params': params}

            else:
                self.function = func_name
                self.instructions[func_name] = {'line': self.line, 'inline': []}

        return True, "Function created"

    def create_parameters(self, args, output=None, open_index=None, close_index=None):
        
        # If the list of args are empty, return the function result
        if not args:
            return output, open_index, close_index

        # Check if we have enough values to continue the process
        if len(args[0]) < 2:
            return output, open_index, close_index

        # Check if the current selection is a '(' parenthese
        if args[0][0] == Tokens.ParOpen and not open_index:
            return self.create_parameters(args[1:], output, 1, close_index)

        # Check if we found not more then 1 '(' so far
        elif args[0][0] == Tokens.ParOpen and open_index:
            return "Found multiple 'Opening parentheses'", open_index, close_index

        # Check if the current selection is a ')' parenthese
        elif args[0][0] == Tokens.ParClose and open_index and not close_index:
            return self.create_parameters(args[1:], output, 1, open_index)

        # Check if the current selection is a ')' parenthese,
        # but we haven't found the '(' parenthese yet
        elif args[0][0] == Tokens.ParClose and not open_index and not close_index:
            return "Found 'Closing parentheses', but couldn't find the leading 'Opening parentheses'", open_index, close_index

        # Check if we found more then 1 ')' parenthese
        elif args[0][0] == Tokens.ParClose and close_index:
            return "Found multiple 'Closing parentheses'", open_index, close_index

        # Check if the current selection is a valid Token to use as function parameter
        elif args[0][0] == Tokens.String:

            # Create a output dict if we haven't created one already
            if not output:
                return self.create_parameters(args[1:], {'amount': 1, 'values': [args[0][1]]}, open_index, close_index)

            # Check if the new parameter is not a duplication
            elif not args[0][1] in output['values']:
                output['amount'] += 1
                output['values'] += [args[0][1]]
                return self.create_parameters(args[1:], output, open_index, close_index)
                
            else:
                return "Can't define parameter '{}' for function more then ones".format(args[0][1]), open_index, close_index

        else:
            return "Token '{}' is disallowed to be used as a valid parameter".format(args[0][0]()), open_index, close_index

    def run_function(self, inline_instructions):

        # Execute the inline instructions, if there are
        # still inline instructions that needs to be executed
        if inline_instructions:
            
            success, message = self.parse_line(inline_instructions[0][0], inline_instructions[0][1])

            if success:
                return self.run_function(inline_instructions[1:])

            else:
                return False, message

        return True, "Function executed"

    def check_if_statement(self, args, place=None):

        if len(args) < 5:
            return False, "Couldn't check if statement, statement is incomplete"

        # Define the left side of the if statement
        left = self.get_variable(args[0], place)

        # Define the type of the expression
        if args[1][0] != Tokens.Undefined and args[1][1] != None:
            expression = args[1][0]

        else:
            return False, "Couldn't check if statement, expression '{}' is an invalid Token".format(args[1][1])

        # Define the right side of the if statement
        right = self.get_variable(args[2], place)
        
        # Check if a valid action is given
        if args[3][0] != Tokens.Variable and args[3][0] != Tokens.Goto:
            return False, "Couldn't check if statement, action of statement '{}' is an invalid Token".format(args[3][1])

        # Run the statement
        result = self.run_if_statement(left, expression, right)

        if result is None:
            return False, "Couldn't perform if statement, invalid expression"

        # Perform action based on result
        if result and args[3][0] == Tokens.Variable:

            # Check if the value after the action is defined
            if len(args) >= 6:
                return self.set_variable((args[4], args[5]), place)
                
            else:
                return False, "Couldn't perform if statement, invalid or unkown value as an result of the if statement"

        elif result and args[3][0] == Tokens.Goto:
            return self.goto_function(args[4], place)

        return True, "If statement complete"        
        
    def run_if_statement(self, left, expression, right):

        is_valid = None

        if expression == Tokens.Equal:
            is_valid = left == right

        elif expression == Tokens.Greater:
            is_valid = left > right

        elif expression == Tokens.GreaterOrEqual:
            is_valid = left >= right

        elif expression == Tokens.Less:
            is_valid = left < right

        elif expression == Tokens.LessOrEqual:
            is_valid = left <= right

        return is_valid

    def goto_function(self, args, place=None):

        # Check if a valid function is given
        if len(args) < 2:
            return False, "Couldn't goto function, function is unknown"

        # Check if the function exist within the current state
        elif args[0][1] not in self.instructions:
            return False, "Couldn't goto function, function '{}' doesn't exist".format(args[0][1])

        # Perform the Goto function, and reset the vars of that function
        function_instructions = self.instructions[args[0][1]]['inline']
        self.function = args[0][1]
        self.instructions[args[0][1]]['vars'] = {}
        self.instructions[args[0][1]]['inline'] = []
        result, message = self.run_function(function_instructions)

        return result, message

    def return_function(self, args, place=None):
        return True, "Variable set"

    def increment_value(self, args, place=None):
        return True, "Variable set"

    def decrement_value(self, args, place=None):
        return True, "Variable set"

    def undefined(self, args, place=None):
        return True, "Variable set"
