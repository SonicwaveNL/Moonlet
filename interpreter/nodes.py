from typing import Optional, Union, List
from .tokens import (
    Token,
    IntegerToken, FloatToken, StringToken, IDToken,
    CommaToken, ColonToken, ParOpenToken, ParCloseToken,
    BracketOpenToken, BracketCloseToken, NewLineToken, EOFToken,
    AddToken, SubToken, MulToken, DivToken,
    EqualToken, GreaterToken, GreaterOrEqualToken, LessToken, LessOrEqualToken,
    AssignAddToken, AssignSubToken, AssignMulToken, AssignDivToken,
    VarToken, FuncToken, CodeBlockToken, CallToken, IfToken, ReturnToken,
)

# Base
class BaseNode:
    def __init__(self, token: Optional[Token] = None):
        self.token = token
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.token.value!r})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(token={self.token!r})"


# Data types
class NumberNode(BaseNode):
    def __init__(self, token: Union[IntegerToken, FloatToken]):
        super().__init__(token)

    @property
    def value(self):
        return self.token.value

class StringNode(BaseNode):
    def __init__(self, token: StringToken):
        super().__init__(token)

    @property
    def value(self):
        return self.token.value

class IDNode(BaseNode):
    def __init__(self, token: IDToken):
        super().__init__(token)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.token.value})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(token={self.token!r})"

    @property
    def value(self): 
        return self.token.value

class ListNode(BaseNode):
    def __init__(self, items: Optional[List[BaseNode]] = None, token: Optional[BaseNode] = None):
        super().__init__(token)
        self.items = items

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.items!r})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(items={self.items!r}, token={self.token!r})"

class ParamNode(BaseNode):
    def __init__(self, token: IDToken):
        super().__init__(token)

    @property
    def value(self): 
        return self.token.value

# Assignment Operations
class AssignOpNode(BaseNode):
    def __init__(self, id: IDNode, value: Optional[BaseNode], token: Union[AssignAddToken, AssignSubToken, AssignMulToken, AssignDivToken]):
        super().__init__(token)
        self.id = id
        self.value = value

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.token.value} {self.id.value} {self.value.value})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, value={self.value!r}, token={self.token!r})"


# Statements
class VarNode(BaseNode):
    def __init__(self, id: IDNode, value: Optional[BaseNode], token: VarToken):
        super().__init__(token)
        self.id = id
        self.value = value

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.token.value!r} {self.id.value}" + (f" {self.value.value!r})" if self.value is not None else ")")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, value={self.value!r}, token={self.token!r})"
    
    @property
    def name(self) -> str:
        return self.id.value

class ReturnNode(BaseNode):
    def __init__(self, return_value: Optional[BaseNode], token: ReturnToken):
        super().__init__(token)
        self.return_value = return_value
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.return_value.value})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(return_value={self.return_value!r}, token={self.token!r})"

class FuncNode(BaseNode):

    def __init__(self, id: IDNode, args: Optional[ListNode], body: ListNode, start: CodeBlockToken, end: BracketCloseToken, token: FuncToken):
        super().__init__(token)
        self.id = id
        self.args = args
        self.body = body
        self.start = start
        self.end = end
        
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name!r}({self.args}))"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, args={self.args!r}, body={self.body!r}, start={self.start!r}, end={self.end!r}, token={self.token!r})"

    @property
    def name(self) -> str:
        return self.id.value
    
class CallNode(BaseNode):

    def __init__(self, id: IDNode, args: Optional[ListNode], result: Optional[VarNode], token: CallToken):
        super().__init__(token)
        self.id = id
        self.args = args
        self.result = result

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name!r}({self.args}))"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, args={self.args!r}, result={self.result!r}, token={self.token!r})"
    
    @property
    def name(self) -> str:
        return self.id.value