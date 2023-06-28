from __future__ import annotations
from typing import Optional, List, Union, Any
from copy import deepcopy
from .tokens import (
    AddToken, SubToken, MulToken, DivToken,
    EqualToken, NotEqualToken, GreaterToken, 
    GreaterOrEqualToken, LessToken, LessOrEqualToken,
    AssignAddToken, AssignSubToken, AssignMulToken, AssignDivToken,
)
from .nodes import (
    BaseNode,
    NumberNode,
    StringNode,
    IDNode,
    BooleanNode,
    ListNode,
    ParamNode,
    CompareOpNode,
    AssignOpNode,
    BinaryOpNode,
    VarNode,
    ReturnNode,
    FuncNode,
    CallNode,
    ConditionsNode,
    PrintNode,
)
from .errors import (
    Error,
    InvalidSyntaxError,
    NotImplementedError,
    RunTimeError,
    ZeroDivisionError,
)

class Empty:
    """An empty value.

    Acts as a placeholder value,
    used within a 'Scope' instance.

    Attributes:
        node: Optional reference to an Identifier.
    """

    def __init__(self, node: Union[IDNode, ParamNode] = None) -> None:
        """Initialise the Empty value.

        Args:
            node: Optional reference to an Identifier. Defaults to None.
        """        
        self.node = node

    def __str__(self) -> str:
        return f"Empty()"

    def __repr__(self) -> str:
        return f"Empty(node={self.node!r})"
        
    def __add__(self, _) -> None:
        return None
    
    def __sub__(self, _) -> None:
        return None
    
    def __mul__(self, _) -> None:
        return None

    def __truediv__(self, _) -> None:
        return None   

    def __eq__(self, rhs: Union[Value, Function, Empty]) -> bool:
        return isinstance(rhs, Empty)
    
    def __ne__(self, rhs: Union[Value, Function, Empty]) -> bool:
        return not isinstance(rhs, Empty)

    def copy(self) -> Empty:
        """Return a copy of Empty.

        Returns:
            Copied Empty with same node reference.
        """
        return Empty(self.node)


class Value:
    """An program Value.

    Acts an actual value within the Program.

    Attributes:
        value: Initial Value of the node. 
        node: Optional reference to an Identifier.
    """
    
    def __init__(self, value, node):
        """Initialise the Value.

        Args:
            value: Initial Value of the node.
            node: Optional reference to an Identifier.
        """
        self.value = value
        self.node = node

    def __str__(self) -> str:
        return repr(self.value)   

    def __repr__(self) -> str:
        return f"Value(value={self.value!r}, node={self.node!r})"
    
    def __add__(self, rhs) -> Optional[Value]:
        if isinstance(rhs.node, type(self.node)):
            lhs = deepcopy(self)
            lhs.value = lhs.value + rhs.value
            return lhs

    def __sub__(self, rhs) -> Optional[Value]:
        if not isinstance(self.node, StringNode) and isinstance(rhs.node, type(self.node)):
            lhs = deepcopy(self)
            lhs.value = lhs.value - rhs.value
            return lhs

    def __mul__(self, rhs) -> Optional[Value]:
        if not isinstance(self.node, StringNode) and isinstance(rhs.node, type(self.node)):
            lhs = deepcopy(self)
            lhs.value = lhs.value * rhs.value
            return lhs

    def __truediv__(self, rhs) -> Optional[Value]:
        if not isinstance(self.node, StringNode) and isinstance(rhs.node, type(self.node)):
            lhs = deepcopy(self)
            lhs.value = lhs.value / rhs.value
            return lhs

    def __eq__(self, rhs: Union[Value, Function, Empty]) -> Optional[Value]:
        if isinstance(rhs, Value): return self.value == rhs.value
    
    def __ne__(self, rhs: Union[Value, Function, Empty]) -> Optional[Value]:
        if isinstance(rhs, Value): return self.value != rhs.value

    def __gt__(self, rhs: Union[Value, Function, Empty]) -> Optional[Value]:
        if isinstance(rhs, Value): return self.value > rhs.value
        
    def __gte__(self, rhs: Union[Value, Function, Empty]) -> Optional[Value]:
        if isinstance(rhs, Value): return self.value >= rhs.value

    def __lt__(self, rhs: Union[Value, Function, Empty]) -> Optional[Value]:
        if isinstance(rhs, Value): return self.value < rhs.value

    def __lte__(self, rhs: Union[Value, Function, Empty]) -> Optional[Value]:
        if isinstance(rhs, Value): return self.value <= rhs.value

    def copy(self) -> Value:
        """Return a copy of Empty.

        Returns:
            Copied Empty with same node reference.
        """
        return deepcopy(self)


class Function:
    """An Function definition.

    Acts a Functional definition within the program.

    Attributes:
        node: Reference to an Function node.
        body: Optional body of the Function.
        scope: Scope of the Function.
        name: Name of the Function.
        args: Arguments of the Function.
        params: Parameters of the Function.
    """

    def __init__(self, node: FuncNode, body: Optional[ListNode], scope: Scope):
        """Initialise the Function definition.

        Args:
            node: Reference to an Function node.
            body: Optional body of the Function.
            scope: Scope of the Function.
        """        
        self.node = node
        self.body = body
        self.scope = scope

    def __str__(self) -> str:
        return f"{self.name}({', '.join(self.params)})"

    def __repr__(self) -> str:
        return f"Function(name={self.name!r}, body={self.body!r}, scope={self.scope!r})"

    @property
    def name(self) -> str:
        return self.node.id.value
    
    @property
    def args(self):
        return self.node.args
    
    @property
    def params(self):
        if (
            not isinstance(self.node.args, ListNode)
            or self.node.args.items is None
        ):
            return list()

        return list(map(lambda x: x.value, self.node.args.items))

    def copy(self) -> Function:
        return deepcopy(self)


class Scope:
    """Scope definition.

    This could be the scope of the program,
    function or function call.

    Attributes:
        name: Name/Id of the scope.
        args: Arguments of the scope. Defaults to None.
        origin: Original node of the scope. Defaults to None.
        outer: Outer scope. Defaults to None.
    """    

    def __init__(self, name: str, args: Optional[dict] = None, origin: Optional[BaseNode] = None, outer: Optional[Scope] = None):
        """Initialise the Scope.

        Args:
            name: Name/Id of the scope.
            args: Arguments of the scope. Defaults to None.
            origin: Original node of the scope. Defaults to None.
            outer: Outer scope. Defaults to None.
        """        
        self.name = name
        self.args = dict() if args is None else args
        self.origin = origin
        self.result = None
        self.outer = outer
        self.depth = 0

    def __str__(self) -> str:
        return f"{self.name}"

    def __repr__(self) -> str:
        return f"Scope(name={self.name!r}, args={self.args!r}, origin={self.origin!r}, outer={self.outer!r})"

    def exist(self, key: str) -> bool:
        return (key in self.args)

    def set(self, key: str, value: Union[Value, Function, Empty]):
        self.args[key] = value

    def get(self, key: str) -> Union[Value, Function, Empty, None]:
        return deepcopy(self.args.get(key, None))

    def get_outer(self, key: str) -> Optional[Function]:
        if self.outer is not None:
            if self.outer.exist(key):
                result = deepcopy(self.outer.get(key))
                return result if isinstance(result, Function) else None
            
            else:
                return self.outer.get_outer(key)

    def remove(self, key: str) -> Union[Value, Function, Empty, None]:
        return self.args.pop(key, None)

    def format_args(self):
        return dict(
            zip(self.args.keys(), 
            map(lambda x: str(x), self.args.values()))
        )


class ProgramState:
    """Represents a state within the Program.

    Attributes:
        result: Result of the ran Program state. Defaults to None.
        error: Optional causes Error. Defaults to None.
    """    
    
    def __init__(
        self,
        result: Optional[Any] = None, 
        error: Union[ProgramState, Error, None] = None
    ) -> None:
        """Initialise the Program state.

        Args:
            result: Result of the ran Program state. Defaults to None.
            error: Optional causes Error. Defaults to None.
        """        
        self.result = result
        self.error = error

    def __str__(self) -> str:
        if self.error is not None:
            return f"ProgramState({self.error})"
        
        return f"ProgramState({self.result})"

    def __repr__(self) -> str:
        return f"ProgramState(result={self.result!r}, error={self.error!r})"

    def add(self, state):
        if state.error is not None:
            self.error = state.error
        return state.result
    
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
    """Reperesentation of a Moonlet Program."""

    def __init__(self) -> None:
        """Initialise the Program."""    

    def __show(self, node: BaseNode, scope: Scope):
        """Show the current execution of an expression.

        This is a private function.

        Args:
            node: Node that is been executed.
            scope: Scope of the Program.
        """        
        if node.token is None:
            print(f"{' '*11} {scope!s: <20} {node.__class__.__name__: <15} {str(scope.format_args()): <20}")
        
        else:
            print(f" {node.token.value: ^10} {scope!s: <20} {node.__class__.__name__: <15} {str(scope.format_args()): <20}")

    def exec(self, node: BaseNode, scope: Scope) -> ProgramState:
        """Execute the given node.

        Args:
            node: Node to execute the operation on.
            scope: Current Program scope.

        Returns:
            ProgramState containing either the Result on successfull
            executing of the Program state, or an 'NotImplementedError'
            if the given node was not implemented or registered.
        """
        p_state = ProgramState()

        self.__show(node, scope)

        if isinstance(node, NumberNode):
            return p_state.run(self.exec_number_node(node))
        
        elif isinstance(node, StringNode):
            return p_state.run(self.exec_string_node(node))
        
        elif isinstance(node, IDNode):
            return p_state.run(self.exec_id_node(node, scope))
        
        elif isinstance(node, BooleanNode):
            return p_state.run(self.exec_bool_node(node))
        
        elif isinstance(node, ListNode):
            return p_state.run(self.exec_list_node(node, scope))
        
        elif isinstance(node, ParamNode):
            return p_state.run(self.exec_param_node(node, scope))

        elif isinstance(node, AssignOpNode):
            return p_state.run(self.exec_assign_op_node(node, scope))

        elif isinstance(node, VarNode):
            return p_state.run(self.exec_var_node(node, scope))        

        elif isinstance(node, ReturnNode):
            return p_state.run(self.exec_return_node(node, scope))

        elif isinstance(node, FuncNode):
            return p_state.run(self.exec_func_node(node, scope))

        elif isinstance(node, CallNode):
            return p_state.run(self.exec_call_node(node, scope))

        elif isinstance(node, ConditionsNode):
            return p_state.run(self.exec_condition_node(node, scope))
        
        elif isinstance(node, CompareOpNode):
            return p_state.run(self.exec_compare_op_node(node, scope))

        elif isinstance(node, BinaryOpNode):
            return p_state.run(self.exec_binary_op_node(node, scope))

        elif isinstance(node, PrintNode):
            return p_state.run(self.exec_print_node(node, scope))

        return p_state.fail(
            NotImplementedError(
                f"Method for function '{type(node).__name__}' is not implemented",
                node.token.pos
            )
        )

    def iter(self, items: List[BaseNode], scope: Scope, output: Optional[List] = None) -> ProgramState:
        """Iterate recursively over given nodes.

        Args:
            items: List of nodes to iterate over.
            scope: Current Program scope.
            output: Optional list of outputs. Defaults to None.

        Returns:
            ProgramState containing either the Result on successfull
            executing of the Program state, or an Error if the Program
            state failed while executing the Program state.
        """        
        p_state = ProgramState()
        output = list() if output is None else output

        if len(items) <= 0:
            return p_state.success(output)
        
        result = p_state.add(self.exec(items[0], scope))
        if p_state.failed(): return p_state

        # Check if the result of the nodes
        # is already determined, because for
        # example an 'early return' or 'break'
        if scope.result is not None:
            return p_state.success(output)

        return self.iter(items[1:], scope, output + [result])

    def exec_number_node(self, node: NumberNode) -> ProgramState:
        """Execute a Number node.

        Turn the given NumberNode into a Program Value.

        Args:
            node: NumberNode to execute.

        Returns:
            ProgramState containing the generated Value.
        """        
        return ProgramState().success(Value(node.token.value, node))
    
    def exec_string_node(self, node: StringNode) -> ProgramState:
        """Execute a StringNode.

        Turn the given StringNode into a Program Value.

        Args:
            node: StringNode to execute.

        Returns:
            ProgramState containing the generated Value.
        """ 
        return ProgramState().success(Value(node.token.value, node))
    
    def exec_id_node(self, node: IDNode, scope: Scope) -> ProgramState:
        """Execute an IDNode.

        Get the a Variable value from the current
        ProgramState, and return it's Value if found,
        while using the given IDNode as an Identifier.

        Args:
            node: IDNode to execute.

        Returns:
            ProgramState containing the generated Value,
            or a RunTimeError if the variable couldn't be found
            within the current ProgramState.
        """ 
        p_state = ProgramState()

        if not scope.exist(node.value):
            return p_state.fail(
                RunTimeError(
                    f"'{node.value}' doesn't exist within scope '{scope.name}'",
                    node.token.pos
                )
            )
        
        value = scope.get(node.value)
        return p_state.success(value)
    
    def exec_bool_node(self, node: BooleanNode) -> ProgramState:
        """Execute a BooleanNode.

        Turn the given BooleanNode into a Program Value.

        Args:
            node: BooleanNode to execute.

        Returns:
            ProgramState containing the generated Value,
            or a RunTimeError if the given node contains
            an invalid Boolean Value (not True/False).
        """ 
        p_state = ProgramState()

        if node.value == 'true':
            return p_state.success(Value(True, node))
        
        elif node.value == 'false':
            return p_state.success(Value(False, node))
        
        else:

            return p_state.fail(
                RunTimeError(
                    f"'{node.value}' isn't a valid boolean value",
                    node.token.pos
                )
            )

    def exec_list_node(self, node: ListNode, scope: Scope) -> ProgramState:
        """Execute a ListNode.

        Execute a ListNode by iterating over
        the items within the ListNode.

        Args:
            node: ListNode to execute.

        Returns:
            ProgramState containing the generated results,
            or a RunTimeError if the given node was empty
            or not an instance of a list.
        """
        p_state = ProgramState()

        if not isinstance(node.items, list):
            return p_state.fail(RunTimeError("Couldn't iterate over an empty 'ListNode'", node.token.pos))

        result = p_state.add(self.iter(node.items, scope))
        if p_state.failed(): return p_state
        return p_state.success(result)

    def exec_param_node(self, node: ParamNode, scope: Scope) -> ProgramState:
        """Execute a ParamNode.

        Execute a ParamNode to set any params
        within the current function definition.

        This is done by setting any created parameters
        as a 'Empty' Value, to skip any operations performed
        during the definition of the function creation.

        Args:
            node: ParamNode to execute.

        Returns:
            ProgramState containing the generated parameter,
            or a RunTimeError if the given parameter node
            was already defined within the current scope.
        """
        p_state = ProgramState()

        if scope.exist(node.value):
            return p_state.fail(RunTimeError(f"'{node.value}' is already defined within scope '{scope.name}'"))

        param = Empty(node)
        scope.set(node.value, param)
        return p_state.success(param)

    def exec_assign_op_node(self, node: AssignOpNode, scope: Scope) -> ProgramState:
        """Execute an AssignOpNode.

        Perform an Assign Operation based
        on the token stored within.
            
        Args:
            node: AssignOpNode to execute.

        Example:
            ```
            =+ — Adding Left to Right.
            =- — Substracting Left from Right.
            =* — Multiplying Left with Right.
            =/ — Dividing Left from Right.
            ```

        Returns:
            ProgramState containing the generated results,
            or a InvalidSyntaxError if the given syntax
            of the Assign Operation isn't a valid or known.
        """
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
            if not isinstance(result, Value): 
                return p_state.fail(InvalidSyntaxError(f"Can't add {lhs} to {rhs}"))

        elif isinstance(node.token, AssignSubToken):
            result = lhs - rhs
            if not isinstance(result, Value): 
                return p_state.fail(InvalidSyntaxError(f"Can't substract {lhs} from {rhs}"))
        
        elif isinstance(node.token, AssignMulToken):
            result = lhs * rhs
            if not isinstance(result, Value): 
                return p_state.fail(InvalidSyntaxError(f"Can't multiply {lhs} by {rhs}"))
        
        elif isinstance(node.token, AssignDivToken):

            # Validate the 'Right-hand side' 
            # on 'Zero-division' before
            # performing the division operation
            if rhs.value == 0:
                return p_state.fail(
                    ZeroDivisionError(
                        f"Can't divide the 'Left-hand side' with zero",
                        node.token.pos
                    )
                )

            result = lhs / rhs
            if not isinstance(result, Value): 
                return p_state.fail(InvalidSyntaxError(f"Can't devide {lhs} from {rhs}"))

        else:
            return p_state.fail(InvalidSyntaxError("Expected '=+', '=-', '=*', '=/'"))

        # Store the result within the given 'scope'
        scope.set(node.id.value, result)
        
        return p_state.success(result)

    # ==========================================================

    def exec_var_node(self, node: VarNode, scope: Scope) -> ProgramState:
        """Execute an VarNode.

        Assign a variable with the given value.
            
        Args:
            node: VarNode to execute.

        Returns:
            ProgramState containing the generated results,
            or a InvalidSyntaxError if the given syntax
            of the Assign Operation isn't a valid or known.
        """
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

        func_scope = Scope(name=f"<Function: '{node.name}'>", origin=node, outer=scope)

        if isinstance(node.args, ListNode) and node.args.items is not None:
            _ = p_state.add(self.exec_list_node(node.args, func_scope))
            if p_state.failed(): return p_state

        _ = p_state.add(self.exec_list_node(node.body, func_scope))
        if p_state.failed(): return p_state

        func = Function(node, node.body, func_scope)

        scope.set(node.name, func)

        self.__show(node, func_scope)

        return p_state.success(func)
    
    def exec_call_node(self, node: CallNode, scope: Scope) -> ProgramState:
        p_state = ProgramState()
        func = None

        # Check if the 'function' is
        # defined within the given 'scope'
        if not scope.exist(node.name):

            # Check if the 'function' is
            # not inline and not available at all
            if not node.inline:
                return p_state.fail(
                    RunTimeError(f"Function with name '{node.name}' isn't defined")
                )

            # Check if the 'function' is
            # inline and not avaiable just yet
            func = scope.get_outer(node.name)

            if node.inline and func is None:
                return p_state.success(None)
        
        # Else retrieve the definition
        else:
            func = scope.get(node.name)       

        # Check if the definition
        # within the given 'scope'
        # is an actual 'function'
        if not isinstance(func, Function):
            return p_state.fail(
                RunTimeError(f"Can't call '{node.name}' as it isn't a function")
            )
                
        # Check if both the arguments
        # of the 'call' and the 'function'
        # are equal in size/amount
        if node.args is None and len(func.params) > 0:
            return p_state.fail(
                RunTimeError(f"Missing '{len(func.params)}' arguments for function '{func.name}', got '0'")
            )
        
        elif len(node.args.items) != len(func.params):
            return p_state.fail(
                RunTimeError(f"Missing '{len(func.params)}' arguments for function '{func.name}', got '{len(node.args.items)}'")
            )

        # Execute the expressions of
        # the param arguments of the
        # 'call', to build the input
        # params of the 'function'
        call_args = p_state.add(self.exec_list_node(node.args, scope))
        if p_state.failed(): return p_state

        # Stich everything back togeter
        # to define the input params
        func_args = dict(zip(func.params, call_args))

        # Define a new 'scope' for this
        # instance of the 'function call'
        call_scope = Scope(name=f"<Call ({scope.depth}): '{node.name}'>", args=func_args, origin=node, outer=scope)
        call_scope.depth += 1

        # Run the body of the 'function'
        _ = p_state.add(self.exec_list_node(func.body, call_scope))
        if p_state.failed(): return p_state

        # self.__show(node, call_scope)
        
        # If any specification, about were to
        # store the 'returned result' of the 'call',
        # is specified, then store it within outer
        # 'scope', at the same level as the 'call'
        if isinstance(node.result, VarNode):

            # Check if the function even has
            # a 'returned value' specified
            if call_scope.result is None:
                return p_state.fail(
                    RunTimeError(f"Function '{node.name}' doesn't have a return value")
                )
            
            # Before setting the 'scope' arg,
            # prevent any overwrite of anything
            # that is not a 'value' (like a 'function')
            if scope.exist(node.result.name):
                value = scope.get(node.result.name)

                if value is not None and not isinstance(value, (Value, Empty)):
                    return p_state.fail(
                        RunTimeError(f"Can't override '{value.__class__.__name__}'")
                    )
                
            scope.set(node.result.name, call_scope.result)

        return p_state.success(call_scope.result)
    
    # ==========================================================

    def exec_condition_node(self, node: ConditionsNode, scope: Scope) -> ProgramState:
        p_state = ProgramState()

        if not isinstance(node.conditions, (CompareOpNode, ListNode)):
            return p_state.fail(
                InvalidSyntaxError(f"Invalid conditions ({node.conditions})", node.token.pos)
            )
        
        result = p_state.add(self.exec(node.conditions, scope))
        if p_state.failed(): return p_state

        # Validate if the Result isn't 'None'
        if result is None:
            return p_state.fail(
                RunTimeError(f"Condition {node} caused an invalid result: '{result}'")
            ) 

        # Validate if the 'True' action is available
        # otherwise give back a 'failed' state
        if node.result is None:
            return p_state.fail(
                InvalidSyntaxError(
                    f"No 'True' or 'left-hand side' action was specified for if-statement",
                    node.token.pos
                )
            )

        # Check if the 'result' of the action
        # needs to be used/stored somewhere
        # instead of performing an action based on the result
        if isinstance(node.result, VarNode):
            
            # Before setting the 'scope' arg,
            # prevent any overwrite of anything
            # that is not a 'value' (like a 'function')
            if scope.exist(node.result.name):
                value = scope.get(node.result.name)

                if value is not None and not isinstance(value, (Value, Empty)):
                    return p_state.fail(
                        RunTimeError(f"Can't override '{value.__class__.__name__}'")
                    )
                
            scope.set(node.result.name, result)
            return p_state.success(result)

        # Perform 'left-hand' action if condition was 'True'
        if result:
            return p_state.run(self.exec(node.result, scope))

        # Otherwise perform the 'right-hand' action
        # if the condition was 'False' and not 'None'        
        elif not result and node.other is not None:
            return p_state.run(self.exec(node.other, scope))

        return p_state.success(result)

    def exec_compare_op_node(self, node: CompareOpNode, scope: Scope) -> ProgramState:
        p_state = ProgramState()

        # Execute the 'left-hand side'
        if node.lhs is None:
            return p_state.fail(RunTimeError(f"Can't compare ({node.lhs})", node.token.pos))
        
        lhs = p_state.add(self.exec(node.lhs, scope))
        if p_state.failed(): return p_state

        # Execute the 'right-hand side'
        if node.rhs is None:
            return p_state.fail(RunTimeError(f"Can't compare ({node.rhs})", node.token.pos))
        
        rhs = p_state.add(self.exec(node.rhs, scope))
        if p_state.failed(): return p_state

        # If either 'lhs' or 'rhs'
        # are an instance of 'Empty',
        # then stop the operation, as this
        # indicates that the value acts as
        # a param/placeholder for a function
        if isinstance(lhs, Empty) or isinstance(rhs, Empty):
            return p_state.success(lhs)

        # Validate if the results from
        # both sides are the same data type,
        # before making an comparation
        if isinstance(lhs, Value) and not isinstance(rhs, Value):
            return p_state.fail(
                RunTimeError(f"Can't compare a 'Value' to '{type(rhs).__name__}'")
            ) 

        elif not isinstance(lhs, Value) and isinstance(rhs, Value):
            return p_state.fail(
                RunTimeError(f"Can't compare a '{type(lhs).__name__}' to 'Value'")
            ) 

        # Peform the operation, based on the Token
        if isinstance(node.token, EqualToken):
            result = lhs == rhs
            if result is not None: return p_state.success(result)
        
        elif isinstance(node.token, NotEqualToken):
            result = lhs != rhs
            if result is not None: return p_state.success(result)
        
        elif isinstance(node.token, GreaterToken):
            result = lhs > rhs
            if result is not None: return p_state.success(result)
        
        elif isinstance(node.token, GreaterOrEqualToken):
            result = lhs >= rhs
            if result is not None: return p_state.success(result)
        
        elif isinstance(node.token, LessToken):
            result = lhs < rhs
            if result is not None: return p_state.success(result)
        
        elif isinstance(node.token, LessOrEqualToken):
            result = lhs <= rhs
            if result is not None: return p_state.success(result)
        
        else:
            return p_state.fail(
                InvalidSyntaxError(
                    f"'{node.token.value}' isn't a valid comparetion operator",
                    node.token.pos
                )
            )
        
        return p_state.fail(
                InvalidSyntaxError(
                    f"Can't compare '{lhs}' to '{rhs}'",
                    node.token.pos
                )
            )

    # ==========================================================

    def exec_binary_op_node(self, node: BinaryOpNode, scope: Scope) -> ProgramState:
        p_state = ProgramState()

        # Execute the 'left-hand side'
        if node.lhs is None:
            return p_state.fail(RunTimeError(f"Can't compare ({node.lhs})", node.token.pos))
        
        lhs = p_state.add(self.exec(node.lhs, scope))
        if p_state.failed(): return p_state

        # Execute the 'right-hand side'
        if node.rhs is None:
            return p_state.fail(RunTimeError(f"Can't compare ({node.rhs})", node.token.pos))
        
        rhs = p_state.add(self.exec(node.rhs, scope))
        if p_state.failed(): return p_state

        # If either 'lhs' or 'rhs'
        # are an instance of 'Empty',
        # then stop the operation, as this
        # indicates that the value acts as
        # a param/placeholder for a function
        if isinstance(lhs, Empty) or isinstance(rhs, Empty):
            return p_state.success(lhs)
        
        # Validate if the results from
        # both sides are the same data type,
        # before making an calculation operations
        if isinstance(lhs, Value) and not isinstance(rhs, Value):
            return p_state.fail(
                RunTimeError(f"Can't calculate a 'Value' with a '{type(rhs).__name__}'")
            ) 

        elif not isinstance(lhs, Value) and isinstance(rhs, Value):
            return p_state.fail(
                RunTimeError(f"Can't calculate a '{type(lhs).__name__}' with a 'Value'")
            )
        
        # Peform the operation, based on the Token
        if isinstance(node.token, AddToken):
            result = lhs + rhs
            if result is not None: return p_state.success(result)
        
        elif isinstance(node.token, SubToken):
            result = lhs - rhs
            if result is not None: return p_state.success(result)
        
        elif isinstance(node.token, MulToken):
            result = lhs * rhs
            if result is not None: return p_state.success(result)
        
        elif isinstance(node.token, DivToken):

            # Validate the 'Right-hand side' 
            # on 'Zero-division' before
            # performing the division operation
            if rhs.value == 0:
                return p_state.fail(
                    ZeroDivisionError(
                        f"Can't divide the 'Left-hand side' with zero",
                        node.token.pos
                    )
                )

            result = lhs / rhs
            if result is not None: return p_state.success(result)

        return p_state.fail(
            NotImplementedError(
                f"No 'Binary Operation' is implemented for '{type(node.token).__name__}'",
                node.token.pos
            )
        )

    # ==========================================================

    def exec_print_node(self, node: PrintNode, scope: Scope) -> ProgramState:
        p_state = ProgramState()

        if not isinstance(node.to_print, (NumberNode, StringNode, IDNode)):
            return p_state.fail(
                RunTimeError(f"Can't print '{node.to_print.value}'", node.token.pos)
            )
        
        print_value = p_state.add(self.exec(node.to_print, scope))
        if p_state.failed(): return p_state

        if not isinstance(print_value, (Value, Empty)):
            if hasattr(print_value, 'token'):
                return p_state.fail(
                    RunTimeError(f"Can't print '{print_value.value}'", print_value.token.pos)
                )
            
            return p_state.fail(
                RunTimeError(
                    f"Can't print '{print_value.value}'", 
                    print_value.node.token.pos
                )
            )
        
        elif isinstance(print_value, Value):
            print(print_value)

        return p_state.success(print_value)