from typing import Optional, Union
from enum import Enum
from .position import Position


# Base
class Token:
    def __init__(self, type: Optional[str] = '???', value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        self.type = type
        self.value = value
        self.pos = pos
        self.expr = None

    def format_value(self):
        return f"'{self.value}'" if isinstance(self.value, str) else str(self.value)

    def __str__(self) -> str:
        return f"Token(type='{self.type}', value={self.format_value()}, pos={self.pos})"

    def __repr__(self) -> str:
        return f"Token(type='{self.type}', value={self.format_value()}, pos={self.pos})"


# Data types
class Integer(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("INT", value, pos)
        self.expr = "([-+]?\d+)"

class Float(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("FLOAT", value, pos)
        self.expr = "([-+]?\d*\.\d+)"

class String(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("STRING", value, pos)
        self.expr = "(\'{1}\w+\'{1}|\"{1}\w+\"{1})"

class Identifier(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("IDEF", value, pos)
        self.expr = "(\w)+"


# Arithmetic Operators
class Add(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("ADD", value, pos)
        self.expr = "\+{1}"

class Substract(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("SUBSTRACT", value, pos)
        self.expr = "\-{1}"

class Multiply(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("MUTIPLY", value, pos)
        self.expr = "\*{1}"

class Devide(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("DEVIDE", value, pos)
        self.expr = "\/{1}"


# Characters
class Comma(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("COMMA", value, pos)
        self.expr = "\,{1}"

class Colon(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("COLON", value, pos)
        self.expr = "\:{1}"

class ParOpen(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("PAR_OPEN", value, pos)
        self.expr = "\({1}"

class ParClose(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("PAR_CLOSE", value, pos)
        self.expr = "\){1}"

class BracketOpen(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("BRACKET_OPEN", value, pos)
        self.expr = "\{{1}"

class BracketClose(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("BRACKET_CLOSE", value, pos)
        self.expr = "\}{1}"

class NewLine(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("NEWLINE", value, pos)
        self.expr = "\n{1}"

class EndOfFile(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("EOF", value, pos)
        self.expr = "\s{1}"


# Comparison Operators
class Equal(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("EQUAL", value, pos)
        self.expr = "\=\="

class Greater(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("GREATER", value, pos)
        self.expr = "\>"

class GreaterOrEqual(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("GREATER_OR_EQUAL", value, pos)
        self.expr = "\>\="

class Less(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("LESS", value, pos)
        self.expr = "\<"

class LessOrEqual(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("LESS_OR_EQUAL", value, pos)
        self.expr = "\<\="


# Assignment Operators
class AssignAdd(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("ASSIGN_ADD", value, pos)
        self.expr = "\=\+"

class AssignSub(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("ASSIGN_SUB", value, pos)
        self.expr = "\=\-"

class AssignMul(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("ASSIGN_MUL", value, pos)
        self.expr = "\=\*"

class AssignDev(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("ASSIGN_DEV", value, pos)
        self.expr = "\=\/"


# Statements
class Variable(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("VAR", value, pos)
        self.expr = "\=\:"

class Func(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("FUNC", value, pos)
        self.expr = "\=\|"

class CodeBlock(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("CODE_BLOCK", value, pos)
        self.expr = "\=\{"

class If(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("IF", value, pos)
        self.expr = "\=\?"

class Return(Token):
    def __init__(self, value: Union[int, float, str, None] = None, pos: Optional[Position] = None):
        super().__init__("RETURN", value, pos)
        self.expr = "\=\>"


class TokenTypes(Enum):

    DATA_TYPES = [
        Float,
        Integer,
        String,
        Identifier,
    ]

    MATH_OPS = [
        Add,
        Substract,
        Multiply,
        Devide,
    ]

    SINGLE_CHARS = [
        Comma,
        Colon,
        ParOpen,
        ParClose,
        BracketOpen,
        BracketClose,
        NewLine,
    ]

    COMPERATIONS = [
        Equal,
        Greater,
        GreaterOrEqual,
        Less,
        LessOrEqual,
    ]

    ASSIGNMENT_OPS = [
        AssignAdd,
        AssignSub,
        AssignMul,
        AssignDev,
    ]

    STATEMENTS = [
        Variable,
        Func,
        CodeBlock,
        If,
        Return,
    ]

    OPERATORS = MATH_OPS + COMPERATIONS + ASSIGNMENT_OPS