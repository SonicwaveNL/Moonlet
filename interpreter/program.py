from typing import Optional, List, Union

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
from .nodes import (
    BaseNode,
    NumberNode,
    StringNode,
    IDNode,
    ListNode,
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
)


class Value:
    
    def __init__(self, value, node):
        self.value = value
        self.node = node

    @property
    def value_format(self):
        return f"'{self.value}'" if isinstance(self.value, str) else self.value

    def __str__(self) -> str:
        return f"{type(self.node.token).__name__}({self.value_format})"    

    def __repr__(self) -> str:
        return f"{type(self.node.token).__name__}({self.value_format})"
    
    def __add__(self, rhs):
        if isinstance(rhs.node, type(self.node)):
            return Value(self.node.value + rhs.node.value, self.node)

    def __sub__(self, rhs):
        if not isinstance(self.node, StringNode) and isinstance(rhs.node, type(self.node)):
            return Value(self.node.value + rhs.node.value, self.node)

    def __mul__(self, rhs):
        if not isinstance(self.node, StringNode) and isinstance(rhs.node, type(self.node)):
            return Value(self.node.value + rhs.node.value, self.node)

    def __dev__(self, rhs):
        if not isinstance(self.node, StringNode) and isinstance(rhs.node, type(self.node)):
            return Value(self.node.value + rhs.node.value, self.node)        

class Scope:

    def __init__(self, name: str, args: Optional[dict] = None, origin: Optional[BaseNode] = None):
        self.name = name
        self.args = dict() if args is None else args
        self.origin = origin

    def set(self, key: str, value: Value):
        self.args[key] = value

    def get(self, key: str) -> Union[Value, None]:
        return self.args.get(key, None)
    
    def remove(self, key: str) -> Union[Value, None]:
        return self.args.pop(key, None)

    def __str__(self) -> str:
        return f"Scope(name='{self.name}', args={self.args}, origin={self.origin})"

    def __repr__(self) -> str:
        return f"Scope(name='{self.name}', args={self.args}, origin={self.origin})"


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

    def exec(self, node: BaseNode, scope: Scope):
        p_state = ProgramState()

        print(f"{scope.name: <15} {node.type: <15} {scope.args}")

        if isinstance(node, ListNode):
            return p_state.run(self.exec_list_node(node, scope))
        
        elif isinstance(node, NumberNode):
            return p_state.run(self.exec_number_node(node, scope))
        
        elif isinstance(node, StringNode):
            return p_state.run(self.exec_string_node(node, scope))
        
        elif isinstance(node, AssignOpNode):
            return p_state.run(self.exec_assign_op_node(node, scope))
        
        elif isinstance(node, VarNode):
            return p_state.run(self.exec_var_node(node, scope))

        return p_state.fail(NotImplementedError(f"Method for function '{type(node).__name__}' is not implemented", node.token.pos))

    def iter(self, items: List[BaseNode], scope: Scope):
        p_state = ProgramState()

        if len(items) <= 0:
            return p_state.success('Done')
        
        result = p_state.add(self.exec(items[0], scope))
        if p_state.failed(): return p_state
        return self.iter(items[1:], scope)

    # ==========================================================

    def exec_number_node(self, node: NumberNode, scope: Scope) -> ProgramState:
        return ProgramState().success(Value(node.token.value, node))
    
    def exec_string_node(self, node: StringNode, scope: Scope) -> ProgramState:
        return ProgramState().success(Value(node.token.value, node))
    
    def exec_id_node(self, node: IDNode, scope: Scope) -> ProgramState:
        p_state = ProgramState()

        value = scope.get(node.value)

        if value is None:
            return p_state.fail(RunTimeError(f"'{node.value}' doesn't exist within scope"))
        
        return p_state.success(value)

    # ==========================================================

    def exec_list_node(self, node: ListNode, scope: Scope) -> ProgramState:
        p_state = ProgramState()

        if not isinstance(node.items, list):
            return p_state.fail(RunTimeError("Couldn't iterate over an empty 'ListNode'", node.token.pos))

        result = p_state.add(self.iter(node.items, scope))
        if p_state.failed(): return p_state
        return p_state.success(result)

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

        result = None

        # Perform the operation, based on the oper Token
        if isinstance(node.token, AssignAdd):
            result = lhs + rhs
            
        else:
            return p_state.fail(InvalidSyntaxError("Expected '=+', '=-', '=*', '=/'"))
        
        # Return an error if the operation was not performed
        if result is None:
            return p_state.fail(InvalidSyntaxError(""))

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