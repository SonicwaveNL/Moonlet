import copy
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
        return f"\nParser(\n  line: {self.line}\n  function: {self.function}\n  vars: {self.variables}\n  instructions: {self.instructions}\n)"

    # REMOVE THIS - Dev function
    def line_follower(self, instruction, args):

        print(f'{self.line}) >> {instruction}', end=' ')

        if args is not None:
            for arg in args:
                print(f'\n    > {arg}: {arg}', end='')

        print('\n')

    def parse(self, tokens):
        # print(f'PARSE_TOKENS:\n', end=' ')
        # pprint(tokens)

        # Save a copy of the tokens for function/line jumps
        if not self.tokens:
            self.tokens = tokens

        # Check if parsing is at the end of the tokens
        if not tokens:
            return True, self.line, self.errors

        # Check if the parsing has enough information
        # to conintue with the parsing
        elif len(tokens) >= 1:
            # token, arguments, raw_line, line_number = tokens
            # print(f'TOKENS: {tokens}')

            self.line += 1
            success, message = self.parse_line(tokens[0][0], tokens[0][1], tokens[0][2], tokens[0][3])

            # REMOVE THIS - Dev function
            # self.line_follower(tokens[0], tokens[0][1])

            if success:
                return self.parse(tokens[1:])

            else:
                return False, self.line, self.errors + [message]

        else:
            return False, self.line, self.errors + [f'Invalid operation at line {self.line + 1}']

    def parse_line(self, instruction, args, raw, number):

        print(f"\n LINE({self.line}:{number}):\t'{raw}'\n   INST:\t{instruction}\n   ARGS:\t{args}")

        if isinstance(instruction, tuple):

            # Define the place where the result needs to be stored
            if instruction[0] == Tokens.Tab and not self.function:
                return False, "Indented Token at line '{}' is not a member of any function"
            
            elif not self.function:
                return False, "Trying to access a function that doesn't exist?"

            else:
                place = self.instructions[self.function]
                place['inline'] += [(instruction, args)]

            # Try to match the right Token
            if instruction[0] == Tokens.Tab and instruction[1] == Tokens.Variable:
                return self.set_variable(args, place=place)

            elif instruction[0] == Tokens.Tab and instruction[1] == Tokens.If:
                return self.check_if_statement(args, place=place)

            elif instruction[0] == Tokens.Tab and instruction[1] == Tokens.Goto:
                return self.goto_function(args, place=place)

            elif instruction[0] == Tokens.Tab and instruction[1] == Tokens.Return:
                return self.return_function(args, place=place)

            elif instruction[0] == Tokens.Tab and instruction[1] == Tokens.Add:
                return self.add_value(args, place=place)

            elif instruction[0] == Tokens.Tab and instruction[1] == Tokens.Substract:
                return self.substract_value(args, place=place)

            elif instruction[0] == Tokens.Tab and instruction[1] == Tokens.EmptyLine:
                return True, "Skipping emptyline"

            elif instruction[0] == Tokens.Tab and instruction[1] == Tokens.Undefined:
                return self.undefined(args, place=place)

        else:

            # If no 'Tab' token is in front of the instruction,
            # then function var back
            self.function = None

            if instruction == Tokens.Variable:
                return self.set_variable(args)

            elif instruction == Tokens.Func:
                return self.create_function(args, raw)

            elif instruction == Tokens.If:
                return self.check_if_statement(args)

            elif instruction == Tokens.Goto:
                return self.goto_function(args)

            elif instruction == Tokens.Add:
                return self.add_value(args)

            elif instruction == Tokens.Substract:
                return self.substract_value(args)

            elif instruction == Tokens.BracketClose:
                return self.close_function(args)

            elif instruction == Tokens.EmptyLine:
                return True, "Skipping emptyline"

            elif instruction == Tokens.Undefined:
                return self.undefined(args)

        return False, "Unknown Token at line {}".format(self.line)

    def set_variable(self, args, place=None):

        if place is not None:
            print(f"  SET_VAR:\n   ARGS:\t{args}\n   PLACE:\t{place.get('name', None)}")
        else:
            print(f"  SET_VAR:\n   ARGS:\t{args}\n   PLACE:\tNone")


        # Check if the input args has enough values
        # to set a name and a value for the var
        if len(args) < 2:
            return False, "Couldn't set Variable, invalid size"

        # Set the name, the type and the value of the var
        # var_name = str(args[0][1])
        # var_type = args[1][0]
        # var_value = args[1][1]
        var_name = args['name'][0]
        var_value = args['value'][0]
        var_type = args['value'][1]

        # If a place was given (when witthin a function),
        # use that place to store the vars to prevent
        # global vars from beeing overrided.
        if place is not None and isinstance(place, dict):

            new_var = {var_name: {'type': var_type, 'value': var_value}}

            if 'vars' in place:
                place['vars'] = {**place['vars'], **new_var}

            else:
                place['vars'] = new_var

        else:
            self.variables[var_name] = {'type': var_type, 'value': var_value}

        return True, "Variable set"

    def get_variable(self, args, place=None):

        if place is not None:
            print(f"  GET_VAR:\n   ARGS:\t{args}\n   PLACE:\t{place.get('name', None)}")
        else:
            print(f"  GET_VAR:\n   ARGS:\t{args}\n   PLACE:\tNone")

        # Check if the input args has enough values
        # to do a variable lookup.
        # if len(args) < 2:
        if args is not None:

            # If a place is given, try to retrieve 
            # the value from that place.
            if place is not None and args in place['vars']:
                return place['vars'][args]
            
            # Elif try to retrieve the value from
            # the global variables
            elif args in self.variables:
                return self.variables[args]

        return args

    def check_variable(self, args, place=None):

        # Check if the input args is a packed value,
        # if it is a packed value, unpack it for the check
        if isinstance(args, tuple):
            value = args[0]

        else:
            value = args

        # If a place is given, check if the variable
        # can be found within that place
        if place is not None and value in place['vars']:
            return True, "Variable exist"
            
        elif value in self.variables:
            return True, "Variable exist"

        return False, "Variable doesn't exist"

    def match_type(self, input, token):

        print(f"  MATCH:\t{input} ? {token}")

        # If the input value is stored within a tuple,
        # then access the value within that tuple
        if isinstance(input, tuple):
            if input[0] == token:
                return True

        # If the input is straight up the token that
        # needs to be checked, then use the input directly
        if input == token:
            return True

        return False

    def create_function(self, args, raw):

        # Check if the input args has enough values
        # to set a name for the function
        if 'name' not in args:
            return False, "Couldn't create function, invalid 'name' given"

        # Get the name of the function
        func_name = args['name']

        # Check if the function with name already exist
        if func_name in self.instructions:
            return False, f"Couldn't create function, function '{func_name}' already exist"

        else:
            self.function = func_name
            success, value = self.new_create_params(args['params'])

            if success:
                self.instructions[func_name] = {'line': self.line, 'inline': [], 'params': args['params'], 'vars': value, 'raw': raw}

            else:
                False, value

            # # Check if the args include enough values to start
            # # checking for open/closing parentheses
            # if len(args) >= 5:

            #     # Try to create the parameters, and validate
            #     # if the args include both valid open/closing parentheses
            #     params, is_opened, is_closed = self.create_parameters(args[1:])

            #     if isinstance(params, str):
            #         return False, params

            #     elif not params:
            #         return False, f"Invalid parameters definition for '{func_name}' function, couldn't process format"

            #     elif not is_opened:
            #         return False, f"No '(' Open parentheses found for function with name '{func_name}'"

            #     elif not is_closed:
            #         return False, f"No ')' Closing parentheses found for function with name '{func_name}'"
            #     else:
            #         self.function = func_name
            #         self.instructions[func_name] = {'line': self.line, 'inline': [], 'params': params}

            # else:
            #     self.function = func_name
            #     self.instructions[func_name] = {'line': self.line, 'inline': []}

        return True, "Function created"

    def new_create_params(self, args, reference=None):

        if len(args) == 0:
            return False, "Couldn't create params with '0' arguments given"

        if reference is not None:
            if len(args) == len(reference):
                found_value = self.variables[reference[0]]
                params = {args[0]: found_value}
                
                if len(args) == 1 and len(reference) == 1:
                    return True, params
                else:
                    return True, {**params, **self.new_create_params(args[1:], reference[1:])[1]}

            return False, f"Couldn't create params: '{len(args)}' args, were '{len(reference)}' is given"

        if len(args) == 1:
            # return copy.deepcopy({args[0]: {}})
            return True, {args[0]: None}

        return True, {args[0]: None, **self.new_create_params(args[1:])[1]}

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
                return f"Can't define parameter '{args[0][1]}' for function more then ones", open_index, close_index

        else:
            return f"Token '{args[0][0]()}' is disallowed to be used as a valid parameter", open_index, close_index

    def run_function(self, inline_instructions, raw, number):

        # print(f' INLINE_INSTRUCTIONS: {inline_instructions}')

        # Execute the inline instructions, if there are
        # still inline instructions that needs to be executed
        if inline_instructions:

            print(f"   RUN('{self.function}'):\t{inline_instructions[0]}")
            
            success, message = self.parse_line(inline_instructions[0][0], inline_instructions[0][1], raw, number)

            if success:
                return self.run_function(inline_instructions[1:], raw, number)

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
            return False, f"Couldn't check if statement, expression '{args[1][1]}' is an invalid Token"

        # Define the right side of the if statement
        right = self.get_variable(args[2], place)

        if right:
            right = right['value'] if 'value' in right else right[1]

        else:
            return False, "Couldn't perform if statement, invalid use of variable retrieval for 'right'"
        
        # Check if a valid action is given
        if args[3][0] != Tokens.Variable and args[3][0] != Tokens.Goto:
            return False, f"Couldn't check if statement, action of statement '{args[3][1]}' is an invalid Token"

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
        if 'name' not in args:
            return False, "Couldn't goto function, function is unknown"

        name = args['name']

        # Check if the function exist within the current state
        if name not in self.instructions:
            return False, f"Couldn't goto function, function '{name}' doesn't exist"

        # Perform the Goto function, and reset the vars of that function
        function_instructions = self.instructions[name]['inline']
        self.function = name

        # Try to create the parameters using
        # the globally stored variable values
        result, output = self.new_create_params(self.instructions[name]['params'], args['params'])

        # If paramaters couldn't be created,
        # then return the caused error message
        if not result:
            return False, output        
        
        self.instructions[name]['vars'] = output
        self.instructions[name]['inline'] = []
        print(f"  INST_VARS:\t{self.instructions[name]['vars']}")
        # print(f"  INST_VARS {output}")
        result, output = self.run_function(function_instructions, self.instructions[name]['raw'], self.instructions[name]['line'])

        print(f' RESULT:\t{result}\n OUTPUT:\t{output}')

        # If the function result in a 'Return' action,
        # Then perform the followup action.
        if result and output:

            if 'destination' in args:
                return self.set_variable({'name': args['destination'], 'value': (output['value'], output['type'])}, place)
            
            # # Check if the function includes parameters,
            # # so we know where to check for the followup action
            # if 'params' in self.instructions[self.function]:
            #     params_amount = self.instructions[self.function]['params']['amount'] + 3

            # else:
            #     params_amount = 1

            # # Check if their are enough values to perform the followup action
            # if len(args) >= params_amount + 2:

            #     # Check if the followup action is to set a variable with the result of the function
            #     if args[params_amount][0] == Tokens.Variable and args[params_amount + 1][0] == Tokens.String:
                    
            #         # Try to set the variable as the result of the function
            #         result, message = self.set_variable((args[params_amount + 1], output), place)
                    
            #         if result:
            #             return result, f"Performed function call, and stored the result in {self.function}"

            #         else:
            #             return result, f"Couldn't set variable as result of function, cause of: '{message}'"

            #     else:
            #         token = args[params_amount + 1][0]
            #         return False, f"Calling the '{self.function}' function gives back a return value, but token '{token()}' can't be used to store that value"

            # else:
            #     return False, f"Calling the '{self.function}' function gives back a return value, but no followup action is defined to handle the result"

        # If the function is completed, but the function returns no result
        elif result and not output:
            return result, f"Called function: '{name}'"

        return False, f"Calling function '{name}' has caused an invalid operation"

    def return_function(self, args, place=None):

        if place is not None:
            print(f"  RTRN_FUNC:\n   ARGS:\t{args}\n   PLACE:\t{place.get('name', None)}")
        else:
            print(f"  RTRN_FUNC:\n   ARGS:\t{args}\n   PLACE:\tNone")

        if not place:
            return False, "Couldn't return a function value, invalid function definition"

        elif 'name' not in args:
            return False, "Couldn't return a function value, the returned value is not defined"

        place['return'] = self.get_variable(args['name'], place)
        
        return True, "Return for function defined"

    def add_value(self, args, place=None):

        if 'lhs' not in args:
            return False, "Couldn't add Value to variable, the 'lhs' is either not defined or invalid"

        elif 'rhs' not in args:
            return False, "Couldn't add Value to variable, the 'lhs' is either not defined or invalid"

        lhs_value, lhs_type = args['lhs']
        rhs_value, rhs_type = args['rhs']
        print(f'  ADD_VALUE:\t{lhs_value} + {rhs_value}')
        print(f'   LHS:\t\t{lhs_type}')
        print(f'   RHS:\t\t{rhs_type}')

        if lhs_type != Tokens.String:
            return False, "Couldn't add Value to variable, '{lhs_value}' isn't a valid variable name"

        # Check if the input args has enough values
        # to update the variable with the added value
        # if len(args) < 2:
        #     return False, "Couldn't add Value to variable, invalid size"

        # Check if the designated variable can be found
        # if not self.check_variable(args[0][1], place):
        lhs_found, _ = self.check_variable(lhs_value, place)
        if not lhs_found:
            return False, f"Couldn't add Value to variable, variable '{lhs_value}' is unknown"

        # Check if the right-hand side is a variable as well,
        # if so: try to validate the variable as well.
        rhs_found, _ = self.check_variable(rhs_value, place)
        if rhs_found:
            rhs_loopup = self.get_variable(rhs_value, place)

            if rhs_loopup is None and place is not None:
                return True, "Skipping cause of function initiialization"

            print(f"  RHS_LOOPUP:\t{rhs_loopup}")
            rhs_type = rhs_loopup['type'] if 'type' in rhs_loopup else rhs_loopup[0]
            rhs_value = rhs_loopup['value'] if 'value' in rhs_loopup else rhs_loopup[1]

        # Check if the value is a pointer to a variable and
        # use that variabel if found, otherwise use the value on it own
        value = self.get_variable(lhs_value, place)

        if value is None and place is not None:
            return True, "Skipping cause of function initiialization"

        if not value:
            return False, "Couldn't add Value to variable, invalid variable retrieval"

        # Check and select the way to access the 'type' and 'value' before checking
        value_type = value['type'] if 'type' in value else value[0]
        value_value = value['value'] if 'value' in value else value[1]

        print(f"   VAR:\t\t{value_value} - {value_type}")

        # Check if the value that needs to be added to the designated
        # variable has the same type as the designated variable
        if not self.match_type(rhs_type, value_type):
            return False, f"Couldn't add Value to variable, can't add '{rhs_type()}' to '{value_type()}'"

        else:

            # Perform 'add' action to create the new value
            new_value = value_value + rhs_value
            
            # Store the result in the designated variable
            # result, message = self.set_variable((args[0], new_value), place)
            result, message = self.set_variable({'name': lhs_value, 'value': (new_value, value_type)}, place)

            # Check if the variable is correctly updated with the new value
            if result:
                return True, f"Added '{rhs_value}' to '{lhs_value}'"

            else:
                return False, f"Couldn't add Value to variable, because of: {message}"

    def substract_value(self, args, place=None):

        if 'lhs' not in args:
            return False, "Couldn't substract Value to variable, the 'lhs' is either not defined or invalid"

        elif 'rhs' not in args:
            return False, "Couldn't substract Value to variable, the 'lhs' is either not defined or invalid"

        lhs_value, lhs_type = args['lhs']
        rhs_value, rhs_type = args['rhs']
        print(f'  SUB_VALUE:\t{lhs_value} + {rhs_value}')
        print(f'   LHS:\t\t{lhs_type}')
        print(f'   RHS:\t\t{rhs_type}')

        if lhs_type != Tokens.String:
            return False, "Couldn't substract Value to variable, '{lhs_value}' isn't a valid variable name"

        # Check if the input args has enough values
        # to update the variable with the substracted value
        # if len(args) < 2:
        #     return False, "Couldn't substract Value to variable, invalid size"

        # Check if the designated variable can be found
        # if not self.check_variable(args[0][1], place):
        lhs_found, _ = self.check_variable(lhs_value, place)
        if not lhs_found:
            return False, f"Couldn't substract Value from variable, variable '{lhs_value}' is unknown"

        # Check if the right-hand side is a variable as well,
        # if so: try to validate the variable as well.
        rhs_found, _ = self.check_variable(rhs_value, place)
        if rhs_found:
            rhs_loopup = self.get_variable(rhs_value, place)

            if rhs_loopup is None and place is not None:
                return True, "Skipping cause of function initiialization"

            print(f"  RHS_LOOPUP:\t{rhs_loopup}")
            rhs_type = rhs_loopup['type'] if 'type' in rhs_loopup else rhs_loopup[0]
            rhs_value = rhs_loopup['value'] if 'value' in rhs_loopup else rhs_loopup[1]

        # Check if the value is a pointer to a variable and
        # use that variabel if found, otherwise use the value on it own
        value = self.get_variable(lhs_value, place)

        if value is None and place is not None:
            return True, "Skipping cause of function initiialization"

        if not value:
            return False, "Couldn't substract Value from variable, invalid variable retrieval"

        # Check and select the way to access the 'type' and 'value' before checking
        value_type = value['type'] if 'type' in value else value[0]
        value_value = value['value'] if 'value' in value else value[1]

        print(f"   VAR:\t\t{value_value} - {value_type}")

        # Check if the value that needs to be substracted from the designated
        # variable has the same type as the designated variable
        if not self.match_type(rhs_type, value_type):
            return False, f"Couldn't substract Value from variable, can't substract '{rhs_type()}' from '{value_type()}'"

        else:

            # Perform 'Substract' action to create the new value
            new_value = value_value - rhs_value
            
            # Store the result in the designated variable
            # result, message = self.set_variable((args[0], new_value), place)
            result, message = self.set_variable({'name': lhs_value, 'value': (new_value, value_type)}, place)

            # Check if the variable is correctly updated with the new value
            if result:
                return True, f"Substracted '{rhs_value}' from '{lhs_value}'"

            else:
                return False, f"Couldn't substract Value to variable, because of: {message}"

    def close_function(self, args):
        self.function = None
        return True, "Closedup current function"

    def undefined(self, args, place=None):

        if place:
            return False, "Token within function '{self.function}' is Undefined"

        else:
            return False, "Token is Undefined"
