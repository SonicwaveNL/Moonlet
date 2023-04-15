import re
from functools import reduce
from .tokens import TokenTypes, NewLine, Float, String, Integer, EndOfFile
from .position import Position
from .errors import Error, InvalidSyntaxError, UnknownCharError


class Lexer:

    def __init__(self, text):
        self.text = text
        self.pos = Position()
        self.error = None

    def run(self):

        # Only start tokenizing when
        # the size of the 'text' > 0
        if len(self.text) == 0:
            self.error = Error("Empty", "Couldn't perform Lexing as no 'text' input was given")
            return [EndOfFile(pos=self.pos)], self.error

        tokens = self.tokenize(self.text)
        self.pos.nextl()
        return tokens + [EndOfFile(pos=self.pos)], self.error

    def tokenize(self, text):

        if text is None or len(text) == 0 or self.error is not None:
            return []
        
        elif text[0] == ' ':
            self.pos.next()
            return self.tokenize(text[1:])
        
        token, rest = self.match_expr(text)
        return [token] + self.tokenize(rest)
        
    def match_expr(self, text):

        # First try to match for a symbol token
        token, match = self.match_tokens(
            text[0],
            TokenTypes.MATH_OPS.value + \
            TokenTypes.SINGLE_CHARS.value
        )
        
        # If a match with a symbol was made,
        # then return the found token
        if token is not None and match is not None:

            # If the token is a newline,
            # then reformat the value and
            # set the Lexer position to nextline
            if token is NewLine:
                found = token('\\n', self.pos.copy())
                self.pos.nextl()
            
            # Or else
            else:
                found = token(text[0], self.pos.copy())
                self.pos.next()

            return found, text[1:] if len(text) > 1 else None
        
        # Start building a part to
        # continue with the token matching
        rest, part, size = self.build_part(text)

        # Try to find the matching token,
        # with the part that was made before
        token, match = self.match_tokens(
            part,
            TokenTypes.DATA_TYPES.value + \
            TokenTypes.COMPERATIONS.value + \
            TokenTypes.ASSIGNMENT_OPS.value + \
            TokenTypes.STATEMENTS.value
        )

        # If a match with the part was made,
        # then return the found token as a part
        if token is not None and match is not None:

            # Try to format the value of the part,
            # and define an 'error' when an exception
            # happend during the process
            try:

                # Else if the token is a Float,
                # then convert the part to it's type
                if token is Float:
                    part = float(part)

                # Else if the token is a Integer,
                # then convert the part to it's type
                elif token is Integer:
                    part = int(part)

                # Else if the token is a String,
                # then strip the (double) quotes
                elif token is String:
                    part = part.replace("'", '')
                    part = part.replace('"', '')

                found = token(part, self.pos.copy(size - 1))
                self.pos.next(size)
                return found, rest

            except ValueError:
                self.error = InvalidSyntaxError(f"Cannot create {token} with value '{part}'")
                return None, None
        
        self.error = UnknownCharError(f"'{part}' is not recognized", self.pos.copy(size - 1))
        return None, None
    
    def match_tokens(self, text, tokens):
        return reduce(
            lambda x, y: x if x[1] is not None else y,
            map(lambda x: (x, self.match_token(text, x)), tokens),
        )

    def match_token(self, text, token):

        if isinstance(token, object):
            token = token()
            
            # Return 'None' if the token
            # has no expression to match
            if token.expr is None: return None
            
            pattern = re.compile(token.expr)
            return re.match(pattern, text)

        return None
    
    def build_part(self, text, result = '', size = 0):

        # Define a list of chars, where if
        # the current char is one of these chars,
        # then stop with building the part
        stops = [' ', '\t', '\n', '(', ')', ',']
        
        # Return the result if no char is
        # left for the part building process
        if len(text) == 0:
            return None, result, size
        
        # Stop building the part, if current
        # char is within the 'stops' list
        elif text[0] in stops:
            return text, result, size

        # Return the result + the last char,
        # when there is only one last char left
        elif len(text) == 1:
            return None, result + text[0], size + 1
        
        # Continue building the part with
        # the remaining text, and add
        # the current char to the result
        return self.build_part(text[1:], result + text[0], size + 1)