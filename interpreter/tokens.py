from typing import Optional, Union
from enum import Enum
from .position import Position


# Base
class Token:
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        self.value = value
        self.pos = pos
        self.expr = None

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.value!r})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value!r}, pos={self.pos!r})"


# Data types
class IntegerToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "([-+]?\d+)"

class FloatToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "([-+]?\d*\.\d+)"

class StringToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "(\'{1}[^\']+\'{1}|\"{1}[^\"]+\"{1})"

class IDToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "(\w)+"


# Arithmetic Operators
class AddToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\+{1}"

class SubToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\-{1}"

class MulToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\*{1}"

class DivToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\/{1}"


# Characters
class CommaToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\,{1}"

class ColonToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\:{1}"

class ParOpenToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\({1}"

class ParCloseToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\){1}"

class BracketOpenToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\{{1}"

class BracketCloseToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\}{1}"

class NewLineToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\n{1}"

class EOFToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\s{1}"


# Comparison Operators
class EqualToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\=\="

class NotEqualToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\!\="

class GreaterToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\>"

class GreaterOrEqualToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\>\="

class LessToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\<"

class LessOrEqualToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\<\="


# Assignment Operators
class AssignAddToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\=\+"

class AssignSubToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\=\-"

class AssignMulToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\=\*"

class AssignDivToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\=\/"


# Statements
class VarToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\=\:"

class FuncToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\=\|"

class CodeBlockToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\=\{"

class CallToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\=\@"

class IfToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\=\?"

class ReturnToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\=\>"

class PrintToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\=\!"

class CommentToken(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__(value, pos)
        self.expr = "\=\#"


class TokenTypes(Enum):

    DATA_TYPES = [
        FloatToken,
        IntegerToken,
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