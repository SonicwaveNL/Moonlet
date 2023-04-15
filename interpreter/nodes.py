from typing import Optional, Union, List
from .tokens import (
    Token,
    Integer, Float, String, Identifier,
    Comma, Colon, ParOpen, ParClose,
    BracketOpen, BracketClose, NewLine, EndOfFile,
    Add, Substract, Multiply, Devide,
    Equal, Greater, GreaterOrEqual, Less, LessOrEqual,
    AssignAdd, AssignSub, AssignMul, AssignDev,
    Variable, Func, CodeBlock, If, Return,
)

# Base
class BaseNode:
    def __init__(self, type: str = "BaseNode", token: Optional[Token] = None):
        self.type = type
        self.token = token
    
    def __str__(self) -> str:
        return f"Node(type='{self.type}', token={self.token})"

    def __repr__(self) -> str:
        return f"Node(type='{self.type}', token={self.token})"


# Data types
class NumberNode(BaseNode):
    def __init__(self, token: Union[Integer, Float]):
        super().__init__("NumberNode", token)

    @property
    def value(self):
        return self.token.value

class StringNode(BaseNode):
    def __init__(self, token: String):
        super().__init__("StringNode", token)

    @property
    def value(self):
        return self.token.value

class IDNode(BaseNode):
    def __init__(self, token: Identifier):
        super().__init__("IDNode", token)

    @property
    def value(self): 
        return self.token.value

class ListNode(BaseNode):
    def __init__(self, items: Optional[List[BaseNode]] = None, token: Optional[BaseNode] = None):
        super().__init__("ListNode", token)
        self.items = items

    def __str__(self) -> str:
        return f"Node(type='{self.type}', items={self.items}, token={self.token})"

    def __repr__(self) -> str:
        return f"Node(type='{self.type}', items={self.items}, token={self.token})"


# Assignment Operations
class AssignOpNode(BaseNode):
    def __init__(self, id: IDNode, value: Optional[BaseNode], token: Union[AssignAdd, AssignSub, AssignMul, AssignDev]):
        super().__init__("AssignOpNode", token)
        self.id = id
        self.value = value

    def __str__(self) -> str:
        return f"Node(type='{self.type}', id={self.id}, value={self.value}, operation={self.token})"

    def __repr__(self) -> str:
        return f"Node(type='{self.type}', id={self.id}, value={self.value}, operation={self.token})"


# Statements
class VarNode(BaseNode):
    def __init__(self, id: IDNode, value: Optional[BaseNode], token: Variable):
        super().__init__("VarNode", token)
        self.id = id
        self.value = value

    def __str__(self) -> str:
        return f"Node(type='{self.type}', id={self.id}, value={self.value}), token={self.token}"
    
    def __repr__(self) -> str:
        return f"Node(type='{self.type}', id={self.id}, value={self.value}), token={self.token}"

class ReturnNode(BaseNode):
    def __init__(self, return_value: Optional[BaseNode], token: Return):
        super().__init__("ReturnNode", token)
        self.return_value = return_value

    def __str__(self) -> str:
        return f"Node(type='{self.type}', return_value={self.return_value}, token={self.token})"
    
    def __repr__(self) -> str:
        return f"Node(type='{self.type}', return_value={self.return_value}, token={self.token})"

class FuncNode(BaseNode):
    def __init__(self, id: IDNode, args: Union[List[IDNode], IDNode, None], body: Union[List[BaseNode], ReturnNode], start: CodeBlock, end: BracketClose, token: Func):
        super().__init__("FuncNode", token)
        self.id = id
        self.args = args
        self.body = body
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return f"Node(type='{self.type}', id={self.id}, args={self.args}, body={self.body}, start={self.start}, end={self.end}, token={self.token}"
    
    def __repr__(self) -> str:
        return f"Node(type='{self.type}', id={self.id}, args={self.args}, body={self.body}, start={self.start}, end={self.end}, token={self.token}"