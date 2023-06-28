from __future__ import annotations
from typing import Optional, Union, List

from interpreter.tokens import Token
from .tokens import (
    Token,
    IntegerToken,
    FloatToken,
    StringToken,
    IDToken,
    BooleanToken,
    BracketCloseToken,
    AddToken,
    SubToken,
    MulToken,
    DivToken,
    EqualToken,
    NotEqualToken,
    GreaterToken,
    GreaterOrEqualToken,
    LessToken,
    LessOrEqualToken,
    AssignAddToken,
    AssignSubToken,
    AssignMulToken,
    AssignDivToken,
    VarToken,
    FuncToken,
    CodeBlockToken,
    CallToken,
    IfToken,
    ReturnToken,
    PrintToken,
)


class BaseNode:
    """Default base node.

    Attributes:
        token: Initial token reference.
    """

    def __init__(self, token: Optional[Token] = None):
        """Initialise the node.

        Args:
            token: Initial token reference. Defaults to None.
        """
        self.token = token

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.token.value!r})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(token={self.token!r})"


class NumberNode(BaseNode):
    """Node representing a Number value.

    Attributes:
        token: Initial token reference.
        value: Value of the node.
    """

    def __init__(self, token: Union[IntegerToken, FloatToken]):
        """Initialise the node.

        Args:
            token: Initial token reference.
        """
        super().__init__(token)

    @property
    def value(self):
        return self.token.value


class StringNode(BaseNode):
    """Node representing a String value.

    Attributes:
        token: Initial token reference.
        value: Value of the node.
    """

    def __init__(self, token: StringToken):
        """Initialise the node.

        Args:
            token: Initial token reference.
        """
        super().__init__(token)

    @property
    def value(self):
        return self.token.value


class IDNode(BaseNode):
    """Node representing a Identifier of a variable.

    Attributes:
        token: Initial token reference.
        value: Value of the node.
    """

    def __init__(self, token: IDToken):
        """Initialise the node.

        Args:
            token: Initial token reference.
        """
        super().__init__(token)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.token.value})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(token={self.token!r})"

    @property
    def value(self):
        return self.token.value


class BooleanNode(BaseNode):
    """Node representing a Boolean value.

    Attributes:
        token: Initial token reference.
        value: Value of the node.
    """

    def __init__(self, token: BooleanToken):
        """Initialise the node.

        Args:
            token: Initial token reference.
        """
        super().__init__(token)

    @property
    def value(self):
        return self.token.value


class ListNode(BaseNode):
    """Node representing a List of node operations.

    This is mainly used for iterating over
    a list of nodes.

    Attributes:
        token: Initial token reference.
        items: Nodes/Items of the list.
    """

    def __init__(
        self, items: Optional[List[BaseNode]] = None, token: Optional[BaseNode] = None
    ):
        """Initialise the node.

        Args:
            items: Nodes/Items of the list.
            token: Initial token reference.
        """
        super().__init__(token)
        self.items = items

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.items!r})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(items={self.items!r}, token={self.token!r})"


class ParamNode(BaseNode):
    """Node representing a Function parameter.

    Attributes:
        token: Initial token reference.
        value: Value of the node.

    Example:
        ```
        (x, y)
        ```
    """

    def __init__(self, token: IDToken):
        """Initialise the node.

        Args:
            token: Initial token reference.
        """
        super().__init__(token)

    @property
    def value(self):
        return self.token.value


class CompareOpNode(BaseNode):
    """Node representing a Comperation Operation.

    Attributes:
        lhs: The Left-hand side.
        rhs: The Right-hand side.
        token: Initial token reference.

    Example:
        ```
        x == y
        ```
    """

    def __init__(
        self,
        lhs: Optional[BaseNode],
        rhs: Optional[BaseNode],
        token: Union[
            EqualToken,
            NotEqualToken,
            GreaterToken,
            GreaterOrEqualToken,
            LessToken,
            LessOrEqualToken,
        ],
    ):
        """Initialise the node.

        Args:
            lhs: The Left-hand side.
            rhs: The Right-hand side.
            token: Initial token reference.
        """
        super().__init__(token)
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.lhs.value} {self.token.value} {self.rhs.value})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(lhs={self.lhs!r}, rhs={self.rhs!r}, token={self.token!r})"


class AssignOpNode(BaseNode):
    """Node representing a Assignment Operation.

    Attributes:
        token: Initial token reference.
        value: Value of the node.

    Example:
        ```
        =+ x 10
        ```
    """

    def __init__(
        self,
        id: IDNode,
        value: Optional[BaseNode],
        token: Union[AssignAddToken, AssignSubToken, AssignMulToken, AssignDivToken],
    ):
        """Initialise the node.

        Args:
            id: Identifier of the node.
            value: Value of the node.
            token: Initial token reference.
        """
        super().__init__(token)
        self.id = id
        self.value = value

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.token.value} {self.id.value} {self.value.value})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, value={self.value!r}, token={self.token!r})"


class BinaryOpNode(BaseNode):
    """Node representing a Binary Operation.

    Attributes:
        lhs: The Left-hand side.
        rhs: The Right-hand side.
        token: Initial token reference.

    Example:
        ```
        =: x + y
        ```
    """

    def __init__(
        self,
        lhs: Optional[BaseNode],
        rhs: Optional[BaseNode],
        token: Union[AddToken, SubToken, MulToken, DivToken],
    ):
        """Initialise the node.

        Args:
            lhs: The Left-hand side.
            rhs: The Right-hand side.
            token: Initial token reference.
        """
        super().__init__(token)
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.lhs.value} {self.token.value} {self.rhs.value})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(lhs={self.lhs!r}, rhs={self.rhs!r}, token={self.token!r})"


class VarNode(BaseNode):
    """Node representing a Variable Assignment.

    Attributes:
        token: Initial token reference.
        value: Value of the node.

    Example:
        ```
        =: x
        ```
    """

    def __init__(self, id: IDNode, value: Optional[BaseNode], token: VarToken):
        """Initialise the node.

        Args:
            id: Identifier of the node.
            value: Value of the node.
            token: Initial token reference.
        """
        super().__init__(token)
        self.id = id
        self.value = value

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.token.value!r} {self.id.value}" + (
            f" {self.value.value!r})" if self.value is not None else ")"
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, value={self.value!r}, token={self.token!r})"

    @property
    def name(self) -> str:
        return self.id.value


class ReturnNode(BaseNode):
    """Node representing a Return statement.

    Attributes:
        return_value: The value that will be returned.
        token: Initial token reference.

    Example:
        ```
        => x
        ```
    """

    def __init__(self, return_value: Optional[BaseNode], token: ReturnToken):
        """Initialise the node.

        Args:
            return_value: The value that will be returned.
            token: Initial token reference.
        """
        super().__init__(token)
        self.return_value = return_value

    def __str__(self) -> str:
        if not isinstance(self.return_value, (NumberNode, StringNode, IDNode)):
            return f"{self.__class__.__name__}({self.return_value!r})"

        else:
            return f"{self.__class__.__name__}({self.return_value.value})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(return_value={self.return_value!r}, token={self.token!r})"


class FuncNode(BaseNode):
    """Node representing a Function definition.

    Attributes:
        id: Identifier of the function.
        args: Arguments of the function.
        body: Code body of the function.
        start: Start token/position of the Code body.
        end: End token/position of the Code body.
        token: Initial token reference.

    Example:
        ```
        =| sum (x, y) ={
            =+ x y
            => x
        }
        ```
    """

    def __init__(
        self,
        id: IDNode,
        args: Optional[ListNode],
        body: ListNode,
        start: CodeBlockToken,
        end: BracketCloseToken,
        token: FuncToken,
    ):
        """Initialise the node.

        Args:
            id: Identifier of the function.
            args: Optional arguments of the function.
            body: Code body of the function.
            start: Start token/position of the Code body.
            end: End token/position of the Code body.
            token: Initial token reference.
        """
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
    """Node representing a Function Call.

    Attributes:
        id: Identifier of the function to call.
        args: Optional arguments of the function to call.
        result: Optional place to store the result of the function to call.
        inline: True/False if the function to call is inline.
        token: Initial token reference.

    Example:
        ```
        =@ func (x, y)
        ```
    """

    def __init__(
        self,
        id: IDNode,
        args: Optional[ListNode],
        result: Optional[VarNode],
        inline: Optional[bool],
        token: CallToken,
    ):
        """Initialise the node.

        Args:
            id: Identifier of the function to call.
            args: Optional arguments of the function to call.
            result: Optional place to store the result of the function to call.
            inline: True/False if the function to call is inline.
            token: Initial token reference.
        """
        super().__init__(token)
        self.id = id
        self.args = args
        self.result = result
        self.inline = inline if inline is not None else False

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name!r}({self.args}))"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, args={self.args!r}, result={self.result!r}, inline={self.inline!r}, token={self.token!r})"

    @property
    def name(self) -> str:
        return self.id.value


class ConditionsNode(BaseNode):
    """Node representing a Conditional comperations.

    Attributes:
        conditions: Conditions to make any comperations with.
        result: Operation to perform if the statement is True.
        other: Optional else operation to perform if the statement is False.
        token: Initial token reference.

    Example:
        ```
        =? x != y
        ```
    """

    def __init__(
        self,
        conditions: Union[CompareOpNode, ListNode],
        result: Union[VarNode, ListNode, ReturnNode, None],
        other: Union[VarNode, ListNode, ReturnNode, None],
        token: IfToken,
    ):
        """Initialise the node.

        Args:
            conditions: Conditions to make any comperations with.
            result: Operation to perform if the statement is True.
            other: Optional else operation to perform if the statement is False.
            token: Initial token reference.
        """
        super().__init__(token)
        self.conditions = conditions
        self.result = result
        self.other = other

    def __str__(self) -> str:
        value = f"{self.__class__.__name__}({self.conditions}"
        value += f" ? {self.result}" if self.result else " ? ..."
        value += f" : {self.other}" if self.other else ""
        return value + "+)"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(conditions={self.conditions!r}, result={self.result!r}, other={self.other!r}, token={self.token!r})"


class PrintNode(BaseNode):
    """Node representing a Print Operation.

    Attributes:
        to_print: Node to print.
        token: Initial token reference.

    Example:
        ```
        =| 'Printing this!'
        ```
    """

    def __init__(
        self, to_print: Union[NumberNode, StringNode, IDNode], token: PrintToken
    ):
        """Initialise the node.

        Args:
            to_print: Node to print.
            token: Initial token reference.
        """
        super().__init__(token)
        self.to_print = to_print

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.value!r})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(to_print={self.to_print!r}, token={self.token!r})"

    @property
    def value(self):
        return self.to_print.value
