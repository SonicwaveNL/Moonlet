from enum import Enum


class Token:
    def __init__(self):
        self.expr = None
        self.args = []

    def __str__(self) -> str:
        return "TOKEN"

class Integer(Token):
    def __init__(self):
        super().__init__()
        self.expr = "([-+]?\d+)"

    def __str__(self) -> str:
        return "INTEGER"

class Float(Token):
    def __init__(self):
        super().__init__()
        self.expr = "([-+]?\d*\.\d+)"

    def __str__(self) -> str:
        return "FLOAT"

class String(Token):
    def __init__(self):
        super().__init__()
        self.expr = "[a-zA-Z]+"

    def __str__(self) -> str:
        return "STRING"


class Equal(Token):
    def __init__(self):
        super().__init__()
        self.expr = "=="

    def __str__(self) -> str:
        return "EQUAL"

class Greater(Token):
    def __init__(self):
        super().__init__()
        self.expr = ">"

    def __str__(self) -> str:
        return "GREATER"

class GreaterOrEqual(Token):
    def __init__(self):
        super().__init__()
        self.expr = ">="

    def __str__(self) -> str:
        return "GREATEROFEQUAL"

class Less(Token):
    def __init__(self):
        super().__init__()
        self.expr = "<"

    def __str__(self) -> str:
        return "LESS"

class LessOrEqual(Token):
    def __init__(self):
        super().__init__()
        self.expr = "<="

    def __str__(self) -> str:
        return "LESSOREQUAL"


class Add(Token):
    def __init__(self):
        super().__init__()
        # self.expr = "=\+"
        self.expr = f"\=\+\s+(?P<lhs>{String}+)\s+(?P<rhs>{Float}|{Integer}|{String})"
        self.args = ["lhs", "rhs"]

    def __str__(self) -> str:
        return "ADD"

class Substract(Token):
    def __init__(self):
        super().__init__()
        # self.expr = "=\-"
        self.expr = f"\=\-\s+(?P<lhs>{String}+)\s+(?P<rhs>{Float}|{Integer}|{String})"
        self.args = ["lhs", "rhs"]

    def __str__(self) -> str:
        return "SUBSTRACT"


class Variable(Token):
    def __init__(self):
        super().__init__()
        # self.expr = "^=:"
        self.expr = f"\=\:\s+(?P<name>{String().expr})\s+\"*\'*(?P<value>{Float().expr}|{Integer().expr}|{String().expr})\"*\'*"
        self.args = ["name", "value"]

    def __str__(self) -> str:
        return "VARIABLE {name}"

class Func(Token):
    # "^\=\|\s+(?P<func_name>\w+)\s*\(+\s*(?P<func_params>[\w|\,\s*]+)\s*\)+"

    def __init__(self):
        super().__init__()
        self.expr = "=\|"
        self.args = ['name', 'params']

    def __str__(self) -> str:
        return "FUNCTION {name} ({params})"

class If(Token):
    def __init__(self):
        super().__init__()
        # self.expr = "=\?"
        self.expr = f"\=\?\s+(?P<lhs>[{Float}|{Integer}|{String}]+)\s+(?P<operation>[{Less}|{LessOrEqual}|{Greater}|{GreaterOrEqual}|{Equal}]+)\s+(?P<rhs>[{Float}|{Integer}|{String}]+)\s+\=\:\s+(?P<destination>[{Float}|{Integer}|{String}]+)"
        self.args = ['lhs', 'operation', 'rhs', 'destination']

    def __str__(self) -> str:
        return "IF {lhs} {operation} {rhs} ASSIGN {destination}"

class Goto(Token):
    def __init__(self):
        super().__init__()
        # self.expr = "=\]"
        self.expr = "\=\]\s+(?P<name>{String}+)"
        self.args = ["name"]

    def __str__(self) -> str:
        return "GOTO {name}"

class Return(Token):
    def __init__(self):
        super().__init__()
        # self.expr = "\=\>"
        self.expr = "\=\>\s+(?P<name>[a-zA-Z]+)"
        self.args = ["name"]

    def __str__(self) -> str:
        return "RETURN {name}"

class ParOpen(Token):
    def __init__(self):
        super().__init__()
        self.expr = "\("

    def __str__(self) -> str:
        return "PARENTHESISOPEN"

class ParClose(Token):
    def __init__(self):
        super().__init__()
        self.expr = "\)"

    def __str__(self) -> str:
        return "PARENTHESISCLOSE"

class Tab(Token):

    def __init__(self):
        super().__init__()
        self.expr = "^[ \t]+"

    def __str__(self) -> str:
        return "TAB"

class Undefined(Token):
    def __init__(self):
        super().__init__()
        self.expr = ""

    def __str__(self) -> str:
        return "UNDEFINED"


class TokenTypes(Enum):

    DATA_TYPES = [
        Integer,
        Float,
        String,
    ]

    COMPARISONS = [
        Equal,
        Greater,
        GreaterOrEqual,
        Less,
        LessOrEqual,
    ]

    OPERATIONS = [
        Variable,
        Func,
        If,
        Goto,
        Return,
        Add,
        Substract,
        ParOpen,
        ParClose,
        Undefined,
    ]
