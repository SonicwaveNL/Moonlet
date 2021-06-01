from enum import Enum


class Token:
    def __init__(self):
        self.expr = r""

    def __str__(self) -> str:
        return "TOKEN"


class Integer(Token):
    def __init__(self):
        super().__init__()
        self.expr = r"([-+]?\d+)"

    def __str__(self) -> str:
        return "INTEGER"


class Float(Token):
    def __init__(self):
        super().__init__()
        self.expr = r"([-+]?\d*\.\d+)"

    def __str__(self) -> str:
        return "FLOAT"


class String(Token):
    def __init__(self):
        super().__init__()
        self.expr = r"([a-zA-Z])+"

    def __str__(self) -> str:
        return "STRING"


class Equal(Token):
    def __init__(self):
        super().__init__()
        self.expr = r"=="

    def __str__(self) -> str:
        return "EQUAL"


class Greater(Token):
    def __init__(self):
        super().__init__()
        self.expr = r">"

    def __str__(self) -> str:
        return "GREATER"


class GreaterOrEqual(Token):
    def __init__(self):
        super().__init__()
        self.expr = r">="

    def __str__(self) -> str:
        return "GREATEROFEQUAL"


class Less(Token):
    def __init__(self):
        super().__init__()
        self.expr = r"<"

    def __str__(self) -> str:
        return "LESS"


class LessOrEqual(Token):
    def __init__(self):
        super().__init__()
        self.expr = r"<="

    def __str__(self) -> str:
        return "LESSOREQUAL"


class Add(Token):
    def __init__(self):
        super().__init__()
        self.expr = r"=\+"

    def __str__(self) -> str:
        return "ADD"


class Substract(Token):
    def __init__(self):
        super().__init__()
        self.expr = r"=\-"

    def __str__(self) -> str:
        return "SUBSTRACT"


class Variable(Token):
    def __init__(self):
        super().__init__()
        self.expr = r"^=:"

    def __str__(self) -> str:
        return "VARIABLE"


class Func(Token):
    def __init__(self):
        super().__init__()
        self.expr = r"=\|"

    def __str__(self) -> str:
        return "FUNCTION"


class If(Token):
    def __init__(self):
        super().__init__()
        self.expr = r"=\?"

    def __str__(self) -> str:
        return "IF"


class Goto(Token):
    def __init__(self):
        super().__init__()
        self.expr = r"=\]"

    def __str__(self) -> str:
        return "GOTO"


class Return(Token):
    def __init__(self):
        super().__init__()
        self.expr = r"=\>"

    def __str__(self) -> str:
        return "RETURN"


class ParOpen(Token):
    def __init__(self):
        super().__init__()
        self.expr = r"^\("

    def __str__(self) -> str:
        return "PARENTHESIS OPEN"


class ParClose(Token):
    def __init__(self):
        super().__init__()
        self.expr = r"^\)"

    def __str__(self) -> str:
        return "PARENTHESIS CLOSE"


class Tab(Token):

    def __init__(self):
        super().__init__()
        self.expr = r"^[ \t]+"

    def __repr__(self) -> str:
        return "TAB"

    def __str__(self) -> str:
        return "TAB"


class Undefined(Token):
    def __init__(self):
        super().__init__()
        self.expr = r""

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
