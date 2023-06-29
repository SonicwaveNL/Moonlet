from typing import Optional, Union
from enum import Enum
from interpreter.position import Position
from .position import Position


class Token:
    """Default base of a Token.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        self.value = value
        self.pos = pos
        self.expr = None

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.value!r})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value!r}, pos={self.pos!r})"


class IntegerToken(Token):
    """Token representing an Integer.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "([-+]?\d+)"


class FloatToken(Token):
    """Token representing a Float.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "([-+]?\d*\.\d+)"


class StringToken(Token):
    """Token representing a String.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "('{1}[^']+'{1}|\"{1}[^\"]+\"{1})"


class IDToken(Token):
    """Token representing a Identifier of a variable.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "(\w)+"


class BooleanToken(Token):
    """Token representing a Boolean.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "(false|true)"


class AddToken(Token):
    """Token representing 2 values added to eachother.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.

    Example:
        ```
        x + y
        ```
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\+{1}"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"


class SubToken(Token):
    """Token representing 2 values substracted from eachother.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.

    Example:
        ```
        x - y
        ```
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\-{1}"


class MulToken(Token):
    """Token representing 2 values multiplied by eachother.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.

    Example:
        ```
        x * y
        ```
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\*{1}"


class DivToken(Token):
    """Token representing 2 values divided by eachother.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.

    Example:
        ```
        x / y
        ```
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\/{1}"


class CommaToken(Token):
    """Token representing seperation comma.

    This is mainly used with parameter specification.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.

    Example:
        ```
        (x, y)
        ```
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\,{1}"


class ColonToken(Token):
    """Token representing a Colon.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\:{1}"


class ParOpenToken(Token):
    """Token representing an opening parenthesis.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\({1}"


class ParCloseToken(Token):
    """Token representing a closing parenthesis.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\){1}"


class BracketOpenToken(Token):
    """Token representing an opening bracket.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\{{1}"


class BracketCloseToken(Token):
    """Token representing a closing bracket.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\}{1}"


class NewLineToken(Token):
    """Token representing a Newline.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\n{1}"


class EOFToken(Token):
    """Token representing a EOF (End of File).

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\s{1}"


class EqualToken(Token):
    """Token representing a Equal sign.

    This is mainly used within an if-statement.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\=\="


class NotEqualToken(Token):
    """Token representing a Not Equal sign.

    This is mainly used within an if-statement.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\!\="


class GreaterToken(Token):
    """Token representing a Greater Than sign.

    This is mainly used within an if-statement.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\>"


class GreaterOrEqualToken(Token):
    """Token representing a Greater or Equal.

    This is mainly used within an if-statement.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\>\="


class LessToken(Token):
    """Token representing a Less sign.

    This is mainly used within an if-statement.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\<"


class LessOrEqualToken(Token):
    """Token representing a Less or Equal sign.

    This is mainly used within an if-statement.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\<\="


class AssignAddToken(Token):
    """Token representing an Add and Assign operation.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\=\+"


class AssignSubToken(Token):
    """Token representing a Substract and Assign operation.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\=\-"


class AssignMulToken(Token):
    """Token representing a Multiply and Assign operation.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\=\*"


class AssignDivToken(Token):
    """Token representing a Divide and Assign operation.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\=\/"


class VarToken(Token):
    """Token representing a Variable assignment.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\=\:"


class FuncToken(Token):
    """Token representing a Function definition.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\=\|"


class CodeBlockToken(Token):
    """Token representing a Code Block of a function.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\=\{"


class CallToken(Token):
    """Token representing a Function Call.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\=\@"


class IfToken(Token):
    """Token representing a If-statement.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\=\?"


class ReturnToken(Token):
    """Token representing a Return statement.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\=\>"


class PrintToken(Token):
    """Token representing a Print operation.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\=\!"


class CommentToken(Token):
    """Token representing a Comment.

    Attributes:
        value: Intial value of the Token.
        pos: Position of the Token.
        expr: Expression to perform the regex with.
    """

    def __init__(
        self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None
    ):
        """Initializes the instance based on value of the token.

        Args:
            value: Initial value of the Token. Defaults to None.
            pos: Position of the Token. Defaults to None.
        """
        super().__init__(value, pos)
        self.expr = "\=\#"


class TokenTypes(Enum):
    """Enumeration of the different Token Types

    Attributes:
        DATA_TYPES: All data tokens.
        MATH_OPS: All mathmatical tokens.
        SINGLE_CHARS: All single character tokens.
        COMPERATIONS: All comperation tokens.
        ASSIGNMENT_OPS: All assignment operational tokens.
        STATEMENTS: All statement tokens.
        OPERATORS: All operations tokens.
    """

    DATA_TYPES = [
        FloatToken,
        IntegerToken,
        BooleanToken,
        StringToken,
        IDToken,
    ]

    MATH_OPS = [
        AddToken,
        SubToken,
        MulToken,
        DivToken,
    ]

    SINGLE_CHARS = [
        CommaToken,
        ColonToken,
        ParOpenToken,
        ParCloseToken,
        BracketOpenToken,
        BracketCloseToken,
        NewLineToken,
    ]

    COMPERATIONS = [
        EqualToken,
        NotEqualToken,
        GreaterToken,
        GreaterOrEqualToken,
        LessToken,
        LessOrEqualToken,
    ]

    ASSIGNMENT_OPS = [
        AssignAddToken,
        AssignSubToken,
        AssignMulToken,
        AssignDivToken,
    ]

    STATEMENTS = [
        VarToken,
        FuncToken,
        CallToken,
        CodeBlockToken,
        IfToken,
        ReturnToken,
        PrintToken,
        CommentToken,
    ]

    OPERATORS = MATH_OPS + COMPERATIONS + ASSIGNMENT_OPS
