import re
from typing import Optional, Tuple, Union, List
from functools import reduce
from interpreter.tokens import (
    TokenTypes,
    NewLineToken,
    FloatToken,
    StringToken,
    IntegerToken,
    EOFToken,
    CommentToken,
)
from interpreter.position import Position
from interpreter.errors import Error, InvalidSyntaxError
from interpreter.utils import debug_log


class Lexer:
    """Reperesentation of the Moonlet Lexer.

    Attributes:
        text: Input text to lexial.
        debug_mode: If 'debug mode' is enabled. Defaults to False.
        pos: Current position of the Lexer.
        error: Optional causes Error. Defaults to None.
    """

    def __init__(self, text: str = "", debug_mode: bool = False):
        """Initialise the Lexer with the given text.

        Args:
            text: input text to lexial. Defaults to Empty str.
            debug_mode: If 'debug mode' is enabled. Defaults to False.
        """
        self.text = text
        self.debug_mode = debug_mode
        self.pos = Position()
        self.error = None

    def __str__(self) -> str:
        return f"Lexer({self.debug_mode})"

    def __repr__(self) -> str:
        return f"Lexer(text={self.text!r}, debug_mode={self.debug_mode!r})"

    @debug_log("Lexer.run", True)
    def run(self):
        """Run the Lexer.

        Returns:
            List of found and created Tokens.
        """

        # Only start tokenizing when
        # the size of the 'text' > 0
        if len(self.text) == 0:
            self.error = Error(
                "Empty", "Couldn't perform Lexing as no 'text' input was given"
            )
            return [EOFToken(pos=self.pos)], self.error

        tokens = self.tokenize(self.text)
        self.pos.nextl()
        return tokens + [EOFToken(pos=self.pos)], self.error

    @debug_log("Lexer.tokenize", True)
    def tokenize(self, text):
        """Tokenize the given text.

        Args:
            text: Text to tonenize.

        Returns:
            List of tokens.
        """

        if text is None or len(text) == 0 or self.error is not None:
            return []

        elif text[0] == " ":
            self.pos.next()
            return self.tokenize(text[1:])

        token, rest = self.match_expr(text)

        # Ignore Comment lines
        if isinstance(token, CommentToken):
            return self.tokenize(rest)

        return [token] + self.tokenize(rest)

    def match_expr(self, text):
        """Match the text against a Token expression.

        Args:
            text: Text to perform the match with.

        Returns:
            Tuple with the matched token and the rest
            of the remaining text.
        """

        # First try to match for a symbol token
        token, match = self.match_tokens(
            text[0], TokenTypes.MATH_OPS.value + TokenTypes.SINGLE_CHARS.value
        )

        # If a match with a symbol was made,
        # then return the found token
        if token is not None and match is not None:
            # If the token is a newline,
            # then reformat the value and
            # set the Lexer position to nextline
            if token is NewLineToken:
                found = token("\\n", self.pos.copy())
                self.pos.nextl()

            # Or else define the found token,
            # and return the found result
            else:
                found = token(text[0], self.pos.copy())
                self.pos.next()

            return found, text[1:] if len(text) > 1 else None

        # If current 'char' is a 'quote'
        # or a 'double quote', then
        # build the next part, while
        # ignoring whitespaces
        if len(text) > 1 and (text[0] == '"' or text[0] == "'"):
            rest, part, size = self.build_part(text=text[1:], find=text[0])

            if part.count(text[0]) < 1:
                self.error = InvalidSyntaxError(
                    f"Expected '\"', \"'\"", self.pos.copy(size - 1)
                )
                return None, None

            part = text[0] + part
        else:
            rest, part, size = self.build_part(text)

        # Try to find the matching token,
        # with the part that was made before
        token, match = self.match_tokens(
            part,
            TokenTypes.DATA_TYPES.value
            + TokenTypes.COMPERATIONS.value
            + TokenTypes.ASSIGNMENT_OPS.value
            + TokenTypes.STATEMENTS.value,
        )

        # If a match with the part was made,
        # then return the found token as a part
        if token is not None and match is not None:
            # Try to format the value of the part,
            # and define an 'error' when an exception
            # happend during the process
            try:
                # Else if the token is a FloatToken,
                # then convert the part to it's type
                if token is FloatToken:
                    part = float(part)

                # Else if the token is a IntegerToken,
                # then convert the part to it's type
                elif token is IntegerToken:
                    part = int(part)

                # Else if the token is a CommentToken,
                # continue part building, until the end
                elif token is CommentToken:
                    found = token(part, self.pos.copy(size - 1))
                    rest, _, comment_size = self.build_part(text=rest, stops=["\n"])
                    self.pos.next(size + comment_size - 1)
                    found.pos.end += comment_size
                    return found, rest

                # Else if the token is a StringToken,
                # then strip the (double) quotes
                elif token is StringToken:
                    part = part.replace("'", "")
                    part = part.replace('"', "")

                found = token(part, self.pos.copy(size - 1))
                self.pos.next(size)
                return found, rest

            except ValueError:
                self.error = InvalidSyntaxError(
                    f"Cannot create {token} with value '{part}'"
                )
                return None, None

        self.error = InvalidSyntaxError(
            f"{part!r} isn't a valid expression", self.pos.copy(size - 1)
        )
        return None, None

    def match_tokens(self, text, tokens):
        """Match text against a list of Tokens.

        Args:
            text: Text to match.
            tokens: Tokens to match against.

        Returns:
            Found Tokens match.
        """
        return reduce(
            lambda x, y: x if x[1] is not None else y,
            map(lambda x: (x, self.match_token(text, x)), tokens),
        )

    def match_token(self, text, token):
        """Match text against a Token.

        Args:
            text: Text to match.
            tokens: Token to match against.

        Returns:
            Found Token match.
        """

        if isinstance(token, object):
            token = token()

            # Return 'None' if the token
            # has no expression to match
            if token.expr is None:
                return None

            pattern = re.compile(token.expr)
            return re.match(pattern, text)

        return None

    def build_part(
        self,
        text: str,
        result: Optional[str] = "",
        size: Optional[int] = 0,
        stops: Optional[List] = None,
        find: Optional[str] = None,
    ) -> Tuple[Union[str, None], Union[str, None], int]:
        """Build a Token part.

        Args:
            text: Input text to build the part with.
            result: Passed result of the part building. Defaults to ''.
            size: Size of the build part. Defaults to 0.
            stops: End stop of the build part. Defaults to None.
            find: Symbol to look for during part building. Defaults to None.

        Returns:
            The build part.
        """

        # Define a list of chars, where if
        # the current char is one of these chars,
        # then stop with building the part,
        # (if no 'find' param is given)
        if stops is None:
            stops = [" ", "\t", "\n", "(", ")", ","]

        # Return the result if no char is
        # left for the part building process
        if len(text) == 0:
            return None, result, size

        # Return when the 'find' char is found
        if find is not None and text[0] == find:
            if len(text) > 1:
                return text[1:], result + text[0], size + 1
            return None, result + text[0], size + 1

        # Stop building the part, if current
        # char is within the 'stops' list
        elif find is None and text[0] in stops:
            return text, result, size

        # Return the result + the last char,
        # when there is only one last char left
        elif len(text) == 1:
            return None, result + text[0], size + 1

        # Continue building the part with
        # the remaining text, and add
        # the current char to the result
        return self.build_part(
            text=text[1:],
            result=result + text[0],
            size=size + 1,
            stops=stops,
            find=find,
        )
