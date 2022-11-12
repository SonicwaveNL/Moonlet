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
        self.expr = "[a-zA-Z|\_]+"

    def __str__(self) -> str:
        return "STRING"

class Boolean(Token):
    def __init__(self):
        super().__init__()
        self.expr = "true|false"

    def __str__(self) -> str:
        return "BOOLEAN"

class DataTypes(Token):
    def __init__(self):
        super().__init__()
        self.expr = f"{Integer().expr}|{Float().expr}|{String().expr}|{Boolean().expr}"
    
    def __str__(self) -> str:
        return f"DATATYPE"


class Equal(Token):
    def __init__(self):
        super().__init__()
        self.expr = "\=\="

    def __str__(self) -> str:
        return "EQUAL"

class Greater(Token):
    def __init__(self):
        super().__init__()
        self.expr = "\>"

    def __str__(self) -> str:
        return "GREATER"

class GreaterOrEqual(Token):
    def __init__(self):
        super().__init__()
        self.expr = "\>\="

    def __str__(self) -> str:
        return "GREATEROFEQUAL"

class Less(Token):
    def __init__(self):
        super().__init__()
        self.expr = "\<"

    def __str__(self) -> str:
        return "LESS"

class LessOrEqual(Token):
    def __init__(self):
        super().__init__()
        self.expr = "\<\="

    def __str__(self) -> str:
        return "LESSOREQUAL"

class Operations(Token):
    def __init__(self):
        super().__init__()
        self.expr = f"[{Less().expr}|{LessOrEqual().expr}|{Greater().expr}|{GreaterOrEqual().expr}|{Equal().expr}]+"

    def __str__(self) -> str:
        return "OPERATIONS"


class Add(Token):
    def __init__(self):
        super().__init__()
        # self.expr = "=\+"
        self.expr = f"\=\+\s+(?P<lhs>{String().expr})\s+(?P<rhs>{DataTypes().expr})"
        self.args = ["lhs", "rhs"]

    def __str__(self) -> str:
        return "ADD"

class Substract(Token):
    def __init__(self):
        super().__init__()
        # self.expr = "=\-"
        self.expr = f"\=\-\s+(?P<lhs>{String().expr})\s+(?P<rhs>{DataTypes().expr})"
        self.args = ["lhs", "rhs"]

    def __str__(self) -> str:
        return "SUBSTRACT"


class Destination(Token):
    def __init__(self):
        super().__init__()
        self.expr = f"\=\:(?P<name>{String().expr})"
    
    def __str__(self) -> str:
        return "DESTINATION {name}"

class Variable(Token):
    def __init__(self):
        super().__init__()
        # self.expr = "^=:"
        self.expr = f"\=\:\s+(?P<name>{String().expr})\s+\"*\'*(?P<value>{DataTypes().expr})\"*\'*"
        self.args = ["name", "value"]

    def __str__(self) -> str:
        return "VARIABLE {name}"

class Func(Token):
    # "^\=\|\s+(?P<func_name>\w+)\s*\(+\s*(?P<func_params>[\w|\,\s*]+)\s*\)+"

    def __init__(self):
        super().__init__()
        # self.expr = "=\|"
        # self.expr = f"\=\|\s+(?P<name>{String().expr})\s+\(\s*(?P<params>[\w|\,\s*]+)\)\s+\=\:\s+(?P<destination>{String().expr})"
        # self.expr = "\=\|\s+(?P<name>[a-zA-Z]+)\s+\(\s*(?P<params>[\w|\,\s*]+)\)\s+\=\{(?P<content>[\t\=\+\-|\>|\<|\w|\,|\n|\s*]+)\}"
        self.expr = "\=\|\s+(?P<name>[a-zA-Z]+)\s+\(\s*(?P<params>[\w|\,\s*]+)\)\s+\=\{"
        self.args = ['name', 'params']

    def __str__(self) -> str:
        return "FUNCTION {name} ({params})"

class If(Token):
    def __init__(self):
        super().__init__()
        # self.expr = "=\?"
        # self.expr = f"\=\?\s+(?P<lhs>[{Float().expr}|{Integer().expr}|{String().expr}]+)\s+(?P<operation>[{Less().expr}|{LessOrEqual().expr}|{Greater().expr}|{GreaterOrEqual().expr}|{Equal().expr}]+)\s+(?P<rhs>[{Float().expr}|{Integer().expr}|{String().expr}]+)\s+\=\:\s+(?P<destination>[{Float().expr}|{Integer().expr}|{String().expr}]+)"
        # \=\?\s+(?P<lhs>[a-zA-Z]+)\s+(?P<operation>[\<|\=\<|\>|\=\>|\=\=]+)\s+(?P<rhs>[\d*.\d+|\d+|a-zA-Z]+)\s+\=\:\s+(?P<destination>[a-zA-Z]+)\s+(?P<value>[\d*.\d+|\d+|a-zA-Z]+)
        self.expr = f"\=\?\s+(?P<lhs>{DataTypes().expr})\s+(?P<operation>{Operations().expr})\s+(?P<rhs>{DataTypes().expr})\s+(?P<action>.+)"
        self.args = ['lhs', 'operation', 'rhs', 'action']

    def __str__(self) -> str:
        return "IF {lhs} {operation} {rhs} {action}"

class Goto(Token):
    def __init__(self):
        super().__init__()
        # self.expr = "=\]"
        # self.expr = "\=\]\s+(?P<name>{String}+)"
        self.expr = f"\=\]\s+(?P<name>{String().expr})\s+\((?P<params>[\w|\,\s*]+)\)\s+[\=\:\s]*(?P<destination>{String().expr})*"
        self.args = ["name", "params", "destination"]

    def __str__(self) -> str:
        return "GOTO {name}"

class Return(Token):
    def __init__(self):
        super().__init__()
        # self.expr = "\=\>"
        self.expr = f"\=\>\s+(?P<name>{String().expr})"
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

class BracketOpen(Token):
    def __init__(self):
        super().__init__()
        self.expr = "\{"

    def __str__(self) -> str:
        return "BRACKETOPEN"

class BracketClose(Token):
    def __init__(self):
        super().__init__()
        self.expr = "\}"

    def __str__(self) -> str:
        return "BRACKETCLOSE"

class Tab(Token):

    def __init__(self):
        super().__init__()
        self.expr = "^[ \t]+"

    def __str__(self) -> str:
        return "TAB"

class EmptyLine(Token):
    def __init__(self):
        super().__init__()
        self.expr = "^\n{1}\s*\n*"
        # self.expr = "^\}\n"
        # self.expr = "\n\s*\n|^\s*"
        # self.expr = "\n\s+\n|^\s+"
        # self.expr = "\n\s*\n"
        # self.expr = "^\s{1}\n*"
        # self.expr = "\n\s*\n|^\s*"

    def __str__(self) -> str:
        return "EMPTYLINE"

class Undefined(Token):
    def __init__(self):
        super().__init__()
        self.expr = ""

    def __str__(self) -> str:
        return "UNDEFINED"


class TokenTypes(Enum):

    DATA_TYPES = [
        Float,
        Integer,
        Boolean,
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
        BracketOpen,
        BracketClose,
        Undefined,
    ]
