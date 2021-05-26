from functools import reduce
from enum import Enum
import re


class Token:
    
    def __init__(self):
        self.expr = r''
        self.args = []

    def __str__(self) -> str:
        return "Token"


class Variable(Token):
    
    def __init__(self):
        super().__init__()
        self.expr = r''
        self.args = []

    def __str__(self) -> str:
        return "Variable"


class Integer(Token):
    
    def __init__(self):
        super().__init__()
        self.expr = r''
        self.args = []

    def __str__(self) -> str:
        return "Integer"


class Float(Token):
    
    def __init__(self):
        super().__init__()
        self.expr = r''
        self.args = []

    def __str__(self) -> str:
        return "Float"


class String(Token):
    
    def __init__(self):
        super().__init__()
        self.expr = r''
        self.args = []

    def __str__(self) -> str:
        return "String"


class Func(Token):
    
    def __init__(self):
        super().__init__()
        self.expr = r''
        self.args = []

    def __str__(self) -> str:
        return "Func"


class If(Token):
    
    def __init__(self):
        super().__init__()
        self.expr = r''
        self.args = []

    def __str__(self) -> str:
        return "If"


class Goto(Token):
    
    def __init__(self):
        super().__init__()
        self.expr = r''
        self.args = []

    def __str__(self) -> str:
        return "Goto"


class Equal(Token):
    
    def __init__(self):
        super().__init__()
        self.expr = r''
        self.args = []

    def __str__(self) -> str:
        return "Equal"


class Greater(Token):
    
    def __init__(self):
        super().__init__()
        self.expr = r''
        self.args = []

    def __str__(self) -> str:
        return "Greater"    


class GreaterOrEqual(Token):
    
    def __init__(self):
        super().__init__()
        self.expr = r''
        self.args = []

    def __str__(self) -> str:
        return "GreaterOrEqual"


class Less(Token):
    
    def __init__(self):
        super().__init__()
        self.expr = r''
        self.args = []

    def __str__(self) -> str:
        return "Less" 


class LessOrEqual(Token):
    
    def __init__(self):
        super().__init__()
        self.expr = r''
        self.args = []

    def __str__(self) -> str:
        return "LessOrEqual"


class TokenType(Enum):
    """All available TokenType's Regex maps"""

    # Values
    VAR = r"([a-zA-Z])+"
    INT = r''
    FLOAT = r''
    STRING = r''
    
    # Functions
    FUNC = r'^=\|'
    IF = r''
    GOTO = r''

    # Comparisons
    EQUAL = r''
    GEATER = r''
    GEATER_OR_EQUAL = r''
    LESS = r''
    LESS_OR_EQUAL = r''

    # Operations
    INCREMENT = r''
    DECREMENT = r''

    @classmethod
    def items(cls):
        return list(map(lambda c: c, cls))

    TYPES = [
        Variable, Integer, Float, String,
        Func, If, Goto,
        Equal, Greater, GreaterOrEqual, Less, LessOrEqual,
    ]

    # Token functions
    # TOKEN_FUNCTIONS = [
    #     Variable, Integer, Float, String,
    #     Func, If, Goto,
    #     Equal, Greater, GreaterOrEqual, Less, LessOrEqual,
    # ]