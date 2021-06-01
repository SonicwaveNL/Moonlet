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
        - [X] Create: Return value of function
        - [X] Create: Set variable on function returned value
        - [X] Create: Check variable Token type
        - [X] Create: 'Add' value
        - [X] Create: 'Substract' value
        - [X] Create: Undefined
        - [ ] Create: Print function
        - [ ] Create: Comment function
        - [ ] Edit: Rename Goto -> Call
        - [ ] Edit: Set variables only with the same type (str, int, float)
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
                return self.goto_function(args, place=place)

            elif instruction[0][0] == Tokens.Tab and instruction[0][1] == Tokens.Return:
                return self.return_function(args, place=place)

            elif instruction[0][0] == Tokens.Tab and instruction[0][1] == Tokens.Add:
                return self.add_value(args, place=place)

            elif instruction[0][0] == Tokens.Tab and instruction[0][1] == Tokens.Substract:
                return self.substract_value(args, place=place)

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

            elif instruction[0] == Tokens.Add:
                return self.add_value(args)

            elif instruction[0] == Tokens.Substract:
                return self.substract_value(args)

            elif instruction[0] == Tokens.Undefined:
                return self.undefined(args)

        return False, "Unknown Token at line {}".format(self.line)

    def set_variable(self, args, place=None):

        # Check if the input args has enough values
        # to set a name and a value for the var
        if len(args) < 2:
            return False, "Couldn't set Variable, invalid size"

        # Set the name, the type and the value of the var
        var_name = str(args[0][1])
        var_type = args[1][0]
        var_value = args[1][1]

        # If a place was given (when witthin a function),
        # use that place to store the vars to prevent
        # global vars from beeing overrided.
        if place and isinstance(place, dict):

            new_var = {var_name: {'type': var_type, 'value': var_value}}

            if 'vars' in place:
                place['vars'] = {**place['vars'], **new_var}

            else:
                place['vars'] = new_var

        else:
            self.variables[var_name] = {'type': var_type, 'value': var_value}

        return True, "Variable set"

    def get_variable(self, args, place=None):

        # Check if the input args has enough values
        # to do a variable lookup.
        if len(args) < 2:
            return None

        # If a place is given, try to retrieve 
        # the value from that place.
        if place and str(args[1]) in place['vars']:
            return place['vars'][str(args[1])]
        
        # Elif try to retrieve the value from
        # the global variables
        elif str(args[1]) in self.variables:
            return self.variables[args[1]]

        return args

    def check_variable(self, args, place=None):

        # Check if the input args is a packed value,
        # if it is a packed value, unpack it for the check
        if len(args) == 2 and isinstance(args, tuple):
            value = args[0]

        else:
            value = args

        # If a place is given, check if the variable
        # can be found within that place
        if place and value in place['vars']:
            return True, "Variable exist"
            
        elif value in self.variables:
            return True, "Variable exist"

        return False, "Variable doesn't exist"

    def match_type(self, input, token):

        # If the input value is stored within a tuple,
        # then access the value within that tuple
        if len(input) == 2 and isinstance(input, tuple):
            if input[0] == token:
                return True

        # If the input is straight up the token that
        # needs to be checked, then use the input directly
        elif len(input) == 1:
            if input == token:
                return True

        return False

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

        else:
            
            # Check if the runned function has a 'Return' value
            if 'return' in self.instructions[self.function]:
                return True, self.instructions[self.function]['return']

            else:
                return True, None

    def check_if_statement(self, args, place=None):

        if len(args) < 5:
            return False, "Couldn't check if statement, statement is incomplete"

        # Define the left side of the if statement
        left = self.get_variable(args[0], place)

        if left:
            left = left['value'] if 'value' in left else left[1]

        else:
            return False, "Couldn't perform if statement, invalid use of variable retrieval for 'left'"

        # Define the type of the expression
        if args[1][0] != Tokens.Undefined and args[1][1] != None:
            expression = args[1][0]

        else:
            return False, "Couldn't check if statement, expression '{}' is an invalid Token".format(args[1][1])

        # Define the right side of the if statement
        right = self.get_variable(args[2], place)

        if right:
            right = right['value'] if 'value' in right else right[1]

        else:
            return False, "Couldn't perform if statement, invalid use of variable retrieval for 'right'"
        
        # Check if a valid action is given
        if args[3][0] != Tokens.Variable and args[3][0] != Tokens.Goto:
            return False, "Couldn't check if statement, action of statement '{}' is an invalid Token".format(args[3][1])

        # Run the statement
        result = self.run_if_statement(left['value'], expression, right['value'])

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
        result, output = self.run_function(function_instructions)

        # If the function result in a 'Return' action,
        # Then perform the followup action.
        if result and output:
            
            # Check if the function includes parameters,
            # so we know where to check for the followup action
            if 'params' in self.instructions[self.function]:
                params_amount = self.instructions[self.function]['params']['amount'] + 3

            else:
                params_amount = 1

            # Check if their are enough values to perform the followup action
            if len(args) >= params_amount + 2:

                # Check if the followup action is to set a variable with the result of the function
                if args[params_amount][0] == Tokens.Variable and args[params_amount + 1][0] == Tokens.String:
                    
                    # Try to set the variable as the result of the function
                    result, message = self.set_variable((args[params_amount + 1], output), place)
                    
                    if result:
                        return result, "Performed function call, and stored the result in {}".format(self.function)

                    else:
                        return result, "Couldn't set variable as result of function, cause of: '{}'".format(message)

                else:
                    token = args[params_amount + 1][0]
                    return False, "Calling the '{}' function gives back a return value, but token '{}' can't be used to store that value".format(self.function, token())

            else:
                return False, "Calling the '{}' function gives back a return value, but no followup action is defined to handle the result".format(self.function)

        # If the function is completed, but the function returns no result
        elif result and not output:
            return result, "Performed function call"

    def return_function(self, args, place=None):

        if not place:
            return False, "Couldn't return a function value, invalid function definition"

        elif len(args[0]) < 2:
            return False, "Couldn't return a function value, the returned value is not defined"

        place['return'] = self.get_variable(args[0], place)
        
        return True, "Return for function defined"

    def add_value(self, args, place=None):

        # Check if the input args has enough values
        # to update the variable with the added value
        if len(args) < 2:
            return False, "Couldn't add Value to variable, invalid size"

        # Check if the designated variable can be found
        if not self.check_variable(args[0][1], place):
            return False, "Couldn't add Value to variable, variable '{}' is unknown".format(args[0][1])

        # Check if the value is a pointer to a variable and
        # use that variabel if found, otherwise use the value on it own
        value = self.get_variable(args[1], place)
        
        if not value:
            return False, "Couldn't add Value to variable, invalid variable retrieval"

        # Check and select the way to access the 'type' and 'value' before checking
        if 'value' in value:
            value_type = value['type']
            value_value = value['value']

        else:
            value_type = value[0]
            value_value = value[1]

        # Check if the value that needs to be added to the designated
        # variable has the same type as the designated variable
        if not self.match_type(args[0][0], value_type):
            return False, "Couldn't add Value to variable, can't add '{}' to '{}'".format(value_type(), args[0][0]())

        else:

            # Perform 'add' action to create the new value
            new_value = args[0][0] + value_value
            
            # Store the result in the designated variable
            result, message = self.set_variable((args[0], new_value), place)

            # Check if the variable is correctly updated with the new value
            if result:
                return True, "Added '{}' to '{}'".format(value_value, args[0][0])

            else:
                return False, "Couldn't add Value to variable, because of: {}".format(message)

    def substract_value(self, args, place=None):

        # Check if the input args has enough values
        # to update the variable with the added value
        if len(args) < 2:
            return False, "Couldn't substract Value from variable, invalid size"

        # Check if the designated variable can be found
        if not self.check_variable(args[0][1], place):
            return False, "Couldn't substract Value from variable, variable '{}' is unknown".format(args[0][1])

        # Check if the value is a pointer to a variable and
        # use that variabel if found, otherwise use the value on it own
        value = self.get_variable(args[1], place)
        
        if not value:
            return False, "Couldn't substract Value from variable, invalid variable retrieval"

        # Check and select the way to access the 'type' and 'value' before checking
        if 'value' in value:
            value_type = value['type']
            value_value = value['value']

        else:
            value_type = value[0]
            value_value = value[1]

        # Check if both values are not a 'Tokens.String',
        # as we're not able to substract strings from eachother
        if args[0][0] == Tokens.String or value_type == Tokens.String:
            return False, "Couldn't substract Value from variable, it's disallowed to substract Strings"

        # Check if the value that needs to be added to the designated
        # variable has the same type as the designated variable
        if not self.match_type(args[0][0], value_type):
            return False, "Couldn't substract Value from variable, can't substract '{}' from '{}'".format(value_type(), args[0][0]())

        else:
            # Perform 'substract' action to create the new value
            new_value = args[0][0] - value_value
            
            # Store the result in the designated variable
            result, message = self.set_variable((args[0], new_value), place)

            # Check if the variable is correctly updated with the new value
            if result:
                return True, "Substracted '{}' from '{}'".format(value_value, args[0][0])

            else:
                return False, "Couldn't substract Value from variable, because of: {}".format(message)

    def undefined(self, args, place=None):

        if place:
            return False, "Token within function '{}' is Undefined".format(self.function)

        else:
            return False, "Token is Undefined"
