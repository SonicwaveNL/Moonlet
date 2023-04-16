from __future__ import annotations
from typing import Optional, List, Union
from functools import reduce
from .tokens import (
    Token,
    IntegerToken, FloatToken, StringToken, IDToken,
    CommaToken, ColonToken, ParOpenToken, ParCloseToken,
    BracketOpenToken, BracketCloseToken, NewLineToken, EOFToken,
    AddToken, SubToken, MulToken, DivToken,
    EqualToken, GreaterToken, GreaterOrEqualToken, LessToken, LessOrEqualToken,
    AssignAddToken, AssignSubToken, AssignMulToken, AssignDivToken,
    VarToken, FuncToken, CodeBlockToken, IfToken, ReturnToken,
)
from .nodes import (
    BaseNode,
    NumberNode,
    StringNode,
    IDNode,
    ListNode,
    ParamNode,
    AssignOpNode,
    VarNode,
    ReturnNode,
    FuncNode,
)
from .errors import (
    Error,
    InvalidSyntaxError,
    UnknownCharError,
    NotImplementedError,
    RunTimeError,
    ZeroDivisionError,
)

class Empty:
    """An empty value.

    Acts as a placeholder value,
    used within a 'Scope' instance.

    Attributes:
        node: Optional reference to a identifier.
    """

    def __init__(self, node: Union[IDNode, ParamNode] = None) -> None:
        self.node = node

    def __str__(self) -> str:
        return f"Empty()"

    def __repr__(self) -> str:
        return f"Empty(node={self.node!r})"
        
    def __add__(self, rhs):
        return None
    
    def __sub__(self, rhs):
        return None
    
    def __mul__(self, rhs):
        return None

    def __truediv__(self, rhs):
        return None   


class Value:
    
    def __init__(self, value, node):
        self.value = value
        self.node = node

    def __str__(self) -> str:
        return f"Value({self.value!r})"    

    def __repr__(self) -> str:
        return f"Value(values={self.value!r}, node={self.node!r})"
    
    def __add__(self, rhs):
        if isinstance(rhs.node, type(self.node)):
            return Value(self.node.value + rhs.node.value, self.node)

    def __sub__(self, rhs):
        if not isinstance(self.node, StringNode) and isinstance(rhs.node, type(self.node)):
            return Value(self.node.value - rhs.node.value, self.node)

    def __mul__(self, rhs):
        if not isinstance(self.node, StringNode) and isinstance(rhs.node, type(self.node)):
            return Value(self.node.value * rhs.node.value, self.node)

    def __truediv__(self, rhs):
        if not isinstance(self.node, StringNode) and isinstance(rhs.node, type(self.node)):
            return Value(self.node.value / rhs.node.value, self.node)        


class Function:
    
    def __init__(self, node: FuncNode, params: Optional[List], body: Optional[List], scope: Scope):
        self.node = node
        self.params = list() if params is None else params
        self.body = body
        self.scope = scope

    def __str__(self) -> str:
        return f"{self.name}({self.params})"

    def __repr__(self) -> str:
        return f"Function(name={self.name!r}, params={self.params!r}, scope={self.scope!r})"

    @property
    def name(self) -> str:
        return self.node.id.value
    
    @property
    def args(self):
        return self.node.args


class Scope:

    def __init__(self, name: str, args: Optional[dict] = None, origin: Optional[BaseNode] = None):
        self.name = name
        self.args = dict() if args is None else args
        self.origin = origin
        self.result = None

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"Scope(name={self.name!r}, args={self.args!r}, origin={self.origin!r})"

    def exist(self, key: str) -> bool:
        return (key in self.args)

    def set(self, key: str, value: Union[Value, Function]):
        self.args[key] = value

    def get(self, key: str) -> Union[Value, None]:
        return self.args.get(key, None)
    
    def remove(self, key: str) -> Union[Value, None]:
        return self.args.pop(key, None)

    def format_args(self):
        return dict(
            zip(self.args.keys(), 
            map(lambda x: str(x), self.args.values()))
        )


class ProgramState:
    
    def __init__(self):
        self.result = None
        self.error = None

    def add(self, state):
        if state.error is not None:
            self.error = state.error
        return state.result
    
    def prev(self):
        pass

    def success(self, result):
        self.result = result
        return self
    
    def fail(self, error: Error):
        if self.error is None: self.error = error
        return self
    
    def failed(self) -> bool:
        return self.error is not None

    def run(self, state):
        result = self.add(state)
        if self.failed(): return self
        return self.success(result)


class Program:

    def __show(self, node: BaseNode, scope: Scope):
        print(f"{scope!s: <20} {node.__class__.__name__: <15} {str(scope.format_args()): <20}")

    def exec(self, node: BaseNode, scope: Scope):
        p_state = ProgramState()

        self.__show(node, scope)

        # ======================================================
        
        if isinstance(node, NumberNode):
            return p_state.run(self.exec_number_node(node, scope))
        
        elif isinstance(node, StringNode):
            return p_state.run(self.exec_string_node(node, scope))
        
        elif isinstance(node, IDNode):
            return p_state.run(self.exec_id_node(node, scope))
        
        # ======================================================
        
        elif isinstance(node, ListNode):
            return p_state.run(self.exec_list_node(node, scope))
        
        elif isinstance(node, ParamNode):
            return p_state.run(self.exec_param_node(node, scope))

        # ======================================================

        elif isinstance(node, AssignOpNode):
            return p_state.run(self.exec_assign_op_node(node, scope))
        
        # ======================================================

        elif isinstance(node, VarNode):
            return p_state.run(self.exec_var_node(node, scope))        

        elif isinstance(node, ReturnNode):
            return p_state.run(self.exec_return_node(node, scope))

        elif isinstance(node, FuncNode):
            return p_state.run(self.exec_func_node(node, scope))

        return p_state.fail(NotImplementedError(f"Method for function '{type(node).__name__}' is not implemented", node.token.pos))

    def iter(self, items: List[BaseNode], scope: Scope):
        p_state = ProgramState()

        if len(items) <= 0:
            return p_state.fail(RunTimeError(f"Can't perform iteration on empty list"))
    
        elif len(items) == 1:
            return p_state.run(self.exec(items[0], scope))

        _ = p_state.add(self.exec(items[0], scope))
        if p_state.failed(): return p_state
        return self.iter(items[1:], scope)

    # ==========================================================

    def exec_number_node(self, node: NumberNode, scope: Scope) -> ProgramState:
        return ProgramState().success(Value(node.token.value, node))
    
    def exec_string_node(self, node: StringNode, scope: Scope) -> ProgramState:
        return ProgramState().success(Value(node.token.value, node))
    
    def exec_id_node(self, node: IDNode, scope: Scope) -> ProgramState:
        p_state = ProgramState()

        if not scope.exist(node.value):
            return p_state.fail(RunTimeError(f"'{node.value}' doesn't exist within scope '{scope.name}'"))
        
        return p_state.success(scope.get(node.value))

    # ==========================================================

    def exec_list_node(self, node: ListNode, scope: Scope) -> ProgramState:
        p_state = ProgramState()

        if not isinstance(node.items, list):
            return p_state.fail(RunTimeError("Couldn't iterate over an empty 'ListNode'", node.token.pos))

        result = p_state.add(self.iter(node.items, scope))
        if p_state.failed(): return p_state
        return p_state.success(result)

    def exec_param_node(self, node: ParamNode, scope: Scope) -> ProgramState:
        p_state = ProgramState()

        if scope.exist(node.value):
            return p_state.fail(RunTimeError(f"'{node.value}' is already defined within scope '{scope.name}'"))

        param = Empty(node)
        scope.set(node.value, param)
        return p_state.success(param)

    # ==========================================================

    def exec_bin_op_node(self, node: BaseNode, scope: Scope) -> ProgramState:
        return ProgramState.fail(
            NotImplementedError(f"Method for function '{type(node).__name__}' is not implemented", node.token.pos)
        )

    def exec_assign_op_node(self, node: AssignOpNode, scope: Scope) -> ProgramState:
        p_state = ProgramState()

        # Try to retrieve initial 'value' of
        # set 'variable' with the given 'IDNode'
        lhs = p_state.add(self.exec_id_node(node.id, scope))
        if p_state.failed(): return p_state
    
        # Execute the expression, stored within
        # the 'value' field of the given 'AssignOpNode',
        # to generate the rhs of this expression
        rhs = p_state.add(self.exec(node.value, scope))
        if p_state.failed(): return p_state

        # If either 'lhs' or 'rhs'
        # are an instance of 'Empty',
        # then stop the operation, as this
        # indicates that the value acts as
        # a param/placeholder for a function
        if isinstance(lhs, Empty) or isinstance(rhs, Empty):
            return p_state.success(lhs)

        result = None

        # Perform the operation, based on the oper Token
        if isinstance(node.token, AssignAddToken):
            result = lhs + rhs
            if result is None: 
                return p_state.fail(InvalidSyntaxError(f"Can't add {lhs} to {rhs}"))

        elif isinstance(node.token, AssignSubToken):
            result = lhs - rhs    
            if result is None: 
                return p_state.fail(InvalidSyntaxError(f"Can't substract {lhs} from {rhs}"))
        
        elif isinstance(node.token, AssignMulToken):
            result = lhs * rhs
            if result is None: 
                return p_state.fail(InvalidSyntaxError(f"Can't multiply {lhs} by {rhs}"))
        
        elif isinstance(node.token, AssignDivToken):
            result = lhs / rhs
            if result is None: 
                return p_state.fail(InvalidSyntaxError(f"Can't devide {lhs} from {rhs}"))

        else:
            return p_state.fail(InvalidSyntaxError("Expected '=+', '=-', '=*', '=/'"))

        # Store the result within the given 'scope'
        scope.set(node.id.value, result)
        
        return p_state.success(result)

    # ==========================================================

    def exec_var_node(self, node: VarNode, scope: Scope) -> ProgramState:
        p_state = ProgramState()
    
        # Execute the expression, stored within
        # the 'value' field of the given 'VarNode',
        # to generate the result of this expression
        value = p_state.add(self.exec(node.value, scope))
        if p_state.failed(): return p_state
        
        # Store the variable within the given 'scope'
        scope.set(node.id.value, value)
        
        return p_state.success(value)
    
    def exec_return_node(self, node: ReturnNode, scope: Scope) -> ProgramState:
        p_state = ProgramState()

        # Execute the expression, stored within
        # the 'return_value' field of the given 'ReturnNode',
        # to generate the 'return_value' of this expression
        return_value = p_state.add(self.exec(node.return_value, scope))
        if p_state.failed(): return p_state

        scope.result = return_value
        return p_state.success(return_value)
    
    # ==========================================================

    def exec_func_node(self, node: FuncNode, scope: Scope) -> ProgramState:
        p_state = ProgramState()
        
        # Check if 'function' is already exist
        # within the given 'scope', as their
        # shouldn't be multiple definitions
        if scope.exist(node.name):
            return p_state.fail(
                RunTimeError(f"Function with name '{node.name}' already exist")
            )

        func_scope = Scope(name=f"<Function: '{node.name}'>", origin=node)
        
        func_args = p_state.add(self.exec_list_node(node.args, func_scope))
        if p_state.failed(): return p_state

        func_body = p_state.add(self.exec_list_node(node.body, func_scope))
        if p_state.failed(): return p_state

        func = Function(node, func_args, func_body, func_scope)

        scope.set(node.name, func)

        self.__show(node, func_scope)

        return p_state.success(func)