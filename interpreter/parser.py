from __future__ import annotations
from typing import Optional, List, Any, Union
from copy import deepcopy
from .tokens import (
    IntegerToken, FloatToken, StringToken, IDToken, BooleanToken,
    CommaToken, ColonToken, ParOpenToken, ParCloseToken,
    BracketCloseToken, NewLineToken, EOFToken,
    AddToken, SubToken, MulToken, DivToken,
    EqualToken, NotEqualToken, GreaterToken, 
    GreaterOrEqualToken, LessToken, LessOrEqualToken,
    AssignAddToken, AssignSubToken, AssignMulToken, AssignDivToken,
    VarToken, FuncToken, CodeBlockToken, CallToken, IfToken, ReturnToken,
    PrintToken,
)
from .nodes import (
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
)

class ParseState:

    def __init__(
        self,
        node: Optional[Any] = None, 
        error: Union[ParseState, Error, None] = None
    ) -> None:
        self.node = node
        self.error = error

    def __str__(self) -> str:
        if self.error is not None:
            return f"ParseState({self.error})"
        
        return f"ParseState({self.node})"

    def __repr__(self) -> str:
        return f"ParseState(node={self.node!r}, error={self.error!r})"

    def add(self, state):
        if state.error is not None:
            self.error = state.error
        return deepcopy(state.node)
    
    def success(self, node):
        self.node = deepcopy(node)
        return self
    
    def fail(self, error: Error):
        if self.error is None: self.error = error
        return self
    
    def failed(self) -> bool:
        return self.error is not None

    def run(self, state):
        node = self.add(state)
        if self.failed(): return self
        return self.success(node)


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.previous_index = -2
        self.current = None
        self.previous = None

    def set_current(self):
        if self.index >= 0 and self.index < len(self.tokens):
            self.current = self.tokens[self.index]
            self.previous = self.tokens[self.previous_index]

    def next(self):
        self.index += 1
        self.previous_index += 1
        self.set_current()

        print(f"NEXT[{self.index:>2}] {'>>': ^4} {self.current}")
        
        return self.current

    # ==========================================================

    def parse(self) -> ParseState:
        p_state = ParseState()

        if len(self.tokens) == 0: 
            return p_state.fail(Error("Parse Error", "Can't parse with 0 tokens"))

        self.next()

        if self.current is None:
            return p_state.fail(Error("Parse Error", "No current token was specified"))

        nodes = p_state.add(self.build_nodes())
        if p_state.error: return p_state
        return p_state.success(ListNode(nodes))
    
    def build_nodes(self, nodes: Optional[List] = None):
        p_state = ParseState()
        nodes = list() if nodes is None else nodes

        if isinstance(self.current, EOFToken):
            return p_state.success(nodes)
        
        elif self.index >= len(self.tokens):
            return p_state.fail(Error('NoEOF', "No 'End Of File'"))
        
        if isinstance(self.current, NewLineToken):
            self.next()
            return self.build_nodes(nodes)
        
        statement = p_state.add(self.statement())
        if p_state.failed(): return p_state
        return self.build_nodes(nodes + [statement])
    
    # ==========================================================

    def statement(self):
        p_state = ParseState()
        # pos_start = self.current.pos.start
        
        if isinstance(self.current, (VarToken, AssignAddToken, AssignSubToken, AssignMulToken, AssignDivToken)):
            return p_state.run(self.assign_oper())
        
        elif isinstance(self.current, FuncToken):
            return p_state.run(self.func_expr())

        elif isinstance(self.current, ReturnToken):
            return p_state.run(self.func_return())
        
        elif isinstance(self.current, CallToken):
            return p_state.run(self.func_call())
        
        elif isinstance(self.current, PrintToken):
            return p_state.run(self.print_expr())
        
        elif isinstance(self.current, IfToken):
            return p_state.run(self.if_statement())
        
        # elif isinstance(self.current, (EqualToken, NotEqualToken, GreaterToken, GreaterOrEqualToken, LessToken, LessOrEqualToken)):
        #     return p_state.run(self.if_statement())
        
        return p_state.fail(NotImplementedError(f"'{self.current}' Statement is not implemented"))
            
    def expr(self):
        p_state = ParseState()

        if isinstance(self.current, ParOpenToken):
            self.next()
            
            expr = p_state.add(self.expr())
            if p_state.failed(): return p_state

            if not isinstance(self.current, ParCloseToken):
                return p_state.fail(InvalidSyntaxError("Expected ')'"))
            
            self.next()
            return p_state.success(expr)
        
        node = p_state.add(self.atom())
        if p_state.failed(): return p_state
        return p_state.success(node)

    def atom(self):
        p_state = ParseState()
        token = self.current

        if isinstance(self.current, IntegerToken) or isinstance(self.current, FloatToken):
            self.next()
            return p_state.run(self.bin_oper(NumberNode(token)))
        
        elif isinstance(self.current, StringToken):
            self.next()
            return p_state.run(self.bin_oper(StringNode(token)))
        
        elif isinstance(self.current, IDToken):
            self.next()
            return p_state.run(self.bin_oper(IDNode(token)))
        
        elif isinstance(self.current, BooleanToken):
            self.next()
            return p_state.run(self.bin_oper(BooleanNode(token)))

        return p_state.fail(NotImplementedError(f"'{self.current}' Atomic value is not implemented"))

    # ==========================================================

    def assign_oper(self):
        p_state = ParseState()
        # pos_start = self.current.pos.start

        # Check if the current token is a
        # 'Variable' or 'Assign Operation'
        # Otherwise return a 'fail' state
        if isinstance(self.current, (VarToken, AssignAddToken, AssignSubToken, AssignMulToken, AssignDivToken)):
            base_token = self.current
            self.next()
        
            if not isinstance(self.current, IDToken):
                return p_state.fail(
                    InvalidSyntaxError("No 'Identifier' was specified")
                )
            
            id_node = IDNode(self.current)
            self.next()

            # Check for a 'binary operation'
            if isinstance(self.current, (AddToken, SubToken, MulToken, DivToken)):
                expr = p_state.add(self.bin_oper(id_node))
                if p_state.failed(): return p_state

            else:
                expr = p_state.add(self.expr())
                if p_state.failed(): return p_state

            self.next()

            if isinstance(base_token, VarToken):
                return p_state.success(VarNode(id_node, expr, base_token))
            
            return p_state.success(AssignOpNode(id_node, expr, base_token))

        return p_state.fail(InvalidSyntaxError("Expected '=:', '=+', '=-', '=*', '=/'"))
    
    def func_expr(self):
        p_state = ParseState()

        if isinstance(self.current, FuncToken):
            base_token = self.current
            self.next()

            if not isinstance(self.current, IDToken):
                return p_state.fail(
                    InvalidSyntaxError("No 'IDToken' was specified")
                )
            
            id_node = IDNode(self.current)
            self.next()

            if not isinstance(self.current, ParOpenToken):
                return p_state.fail(InvalidSyntaxError("Expected '('"))

            self.next()
            
            arg_nodes = p_state.add(self.func_params())
            if p_state.failed(): return p_state

            if not isinstance(self.current, ParCloseToken):
                return p_state.fail(InvalidSyntaxError("Expected ')'"))

            self.next()

            if not isinstance(self.current, CodeBlockToken):
                return p_state.fail(InvalidSyntaxError("Expected '={'"))
            
            start_block = self.current
            
            # self.next()

            # if not isinstance(self.current, NewLineToken):
            #     return p_state.fail(InvalidSyntaxError("Expected a 'Newline' after '={'"))
            
            self.next()
            
            # body_nodes = p_state.add(self.func_body())
            body_nodes = p_state.add(self.code_block())
            if p_state.failed(): return p_state
            
            if not isinstance(self.current, BracketCloseToken):
                return p_state.fail(InvalidSyntaxError("Expected '}'"))
            
            end_block = self.current

            self.next()

            return p_state.success(
                FuncNode(id_node, arg_nodes, body_nodes, start_block, end_block, base_token)
            )

        return p_state.fail(InvalidSyntaxError("Expected '=|'"))
    
    def func_params(self, params: Optional[List] = None):
        p_state = ParseState()
        params = list() if params is None else params

        if isinstance(self.current, IDToken):
            params += [ParamNode(self.current)]
            self.next()

            if isinstance(self.current, IDToken):
                return p_state.fail(InvalidSyntaxError("Expected ','"))

            return self.func_params(params)
        
        elif isinstance(self.current, CommaToken):
            self.next()

            if not isinstance(self.current, IDToken):
                return p_state.fail(
                    InvalidSyntaxError("Expected 'parameter identifier' after ','")
                )

            return self.func_params(params)

        return p_state.success(ListNode(params))
    
    def func_body(self, nodes: Optional[List] = None):
        p_state = ParseState()
        nodes = list() if nodes is None else nodes

        if (
            isinstance(self.current, BracketCloseToken) 
            or isinstance(self.current, EOFToken) 
            or self.index >= len(self.tokens)
        ):
            return p_state.fail(InvalidSyntaxError("Expected '=>'"))

        elif isinstance(self.current, NewLineToken):
            self.next()
            return self.func_body(nodes)

        elif isinstance(self.current, ReturnToken):
            statement = p_state.add(self.statement())
            if p_state.failed(): return p_state

            self.next()


            return p_state.success(ListNode(nodes + [statement]))

        statement = p_state.add(self.statement())
        if p_state.failed(): return p_state

        return self.func_body(nodes + [statement])

    def func_args(self, args: Optional[List] = None):
        p_state = ParseState()
        args = list() if args is None else args

        if isinstance(self.current, (IntegerToken, FloatToken, StringToken, IDToken)):
            arg = p_state.add(self.atom())
            if p_state.failed(): return p_state

            args += [arg]

            if not isinstance(self.current, (CommaToken, ParCloseToken)):
                return p_state.fail(InvalidSyntaxError("Expected ')', ','"))

            return self.func_args(args)
        
        elif isinstance(self.current, CommaToken):
            self.next()

            if isinstance(self.current, CommaToken):
                return p_state.fail(
                    InvalidSyntaxError("Expected 'value' after ','")
                )

            return self.func_args(args)

        return p_state.success(ListNode(args))

    def func_call(self, id_node: Optional[IDNode] = None):
        p_state = ParseState()
        base_token = self.current
        is_inline = False

        if isinstance(self.current, CallToken):
            self.next()

        # Look for the id/name of the function to call
        if id_node is None and not isinstance(self.current, IDToken):
            return p_state.fail(
                InvalidSyntaxError("Expected 'name' of function to call")
            )
        
        elif id_node is None:
            id_node = IDNode(self.current)
            self.next()

        else:
            base_token = id_node.token
            is_inline = True

        if not isinstance(self.current, ParOpenToken):
            return p_state.fail(InvalidSyntaxError("Expected '('"))

        self.next()
        
        # Process the 'function arguments'
        arg_nodes = p_state.add(self.func_args())
        if p_state.failed(): return p_state

        if not isinstance(self.current, ParCloseToken):
            return p_state.fail(InvalidSyntaxError("Expected ')'"))

        self.next()

        # If any specification, about were to
        # store the 'returned result' of the 'call',
        # is specified, then continue the parsing
        if not isinstance(self.current, VarToken):
            return p_state.success(
                CallNode(
                    id=id_node,
                    args=arg_nodes,
                    result=None,
                    inline=is_inline,
                    token=base_token
                )
            )
        
        var_token = self.current
        
        self.next()

        if not isinstance(self.current, IDToken):
            return p_state.fail(
                InvalidSyntaxError(
                    "Expected 'Identifier' to store the returned value of the function in"
                )
            )
        
        result_node = IDNode(self.current)

        self.next()

        if not isinstance(self.current, (NewLineToken, EOFToken)):
            return p_state.fail(
                InvalidSyntaxError(f"Can't put '{self.current}' after function call")
            )
        
        return p_state.success(
            CallNode(
                id=id_node, 
                args=arg_nodes, 
                result=VarNode(id=result_node, value=None, token=var_token),
                inline=is_inline,
                token=base_token
            )
        )

    def func_return(self):
        p_state = ParseState()
        base_token = self.current

        self.next()

        result = p_state.add(self.atom())
        if p_state.failed(): return p_state

        if isinstance(self.current, ParOpenToken):
            result = p_state.add(self.func_call(result))
            if p_state.failed(): return p_state

        return p_state.success(ReturnNode(result, base_token))

    # ==========================================================

    def code_block(self, nodes: Optional[List] = None):
        p_state = ParseState()
        nodes = list() if nodes is None else nodes

        if ( 
            isinstance(self.current, EOFToken) 
            or self.index >= len(self.tokens)
        ):
            return p_state.fail(InvalidSyntaxError("Expected '}'"))

        elif isinstance(self.current, NewLineToken):
            self.next()
            return self.code_block(nodes)
        
        elif isinstance(self.current, BracketCloseToken):
            return p_state.success(ListNode(nodes))

        statement = p_state.add(self.statement())
        if p_state.failed(): return p_state

        return self.code_block(nodes + [statement])

    # ==========================================================

    def if_statement(self):
        p_state = ParseState()

        if isinstance(self.current, IfToken):
            base_token = self.current
            
            self.next()

            # Build conditions
            condition = p_state.add(self.condition())
            if p_state.failed(): return p_state

            # Build the 'result' of the conditions 
            # (when the conditions are True)
            result_token = self.current
            result_node = None

            # If the 'result' should be stored
            # within a 'variable', then parse
            # the rest while building the 'VarNode'
            if isinstance(self.current, VarToken):
                self.next()
                
                if not isinstance(self.current, IDToken):
                    return p_state.fail(
                        InvalidSyntaxError(
                            "Expected 'Identifier' to store the result of the if-statement in"
                        )
                    )
                
                id_node = IDNode(self.current)
                result_node = VarNode(id=id_node, value=None, token=result_token)
                self.next()

            # Or if the 'result' defines a 'code block',
            # then parse the 'body' of the 'result'
            # as a 'ListNode' (list of seperate nodes)
            elif isinstance(self.current, CodeBlockToken):
                self.next()
                result_node = p_state.add(self.code_block())
                if p_state.failed(): return p_state
                self.next()

            else:
                result_node = p_state.add(self.statement())
                if p_state.failed(): return p_state
            
            # Build the 'other' of the conditions
            # (when the conditions are False),
            # when it's defined after the 'result'
            # as a ':' (colon symbol)
            if isinstance(self.current, ColonToken):
                self.next()

                if isinstance(self.current, NewLineToken):
                    return p_state.fail(
                        InvalidSyntaxError(
                            f"No 'False' or 'right-hand side' action was specified for if-statement"
                        )
                    )
                
                other_node = p_state.add(self.statement())
                if p_state.failed(): return p_state
                
                return p_state.success(ConditionsNode(
                        condition,
                        result_node,
                        other_node,
                        base_token
                    )
                )

            return p_state.success(ConditionsNode(
                    condition,
                    result_node,
                    None, 
                    base_token
                )
            )

        return p_state.fail(
            InvalidSyntaxError(f"Expected '=?'")
        )
    
    def condition(self):
        p_state = ParseState()
        found_par_open = False

        # Check if the current token is 
        # a '(', which means that their 
        # must be a ')' at the end
        if isinstance(self.current, ParOpenToken):
            found_par_open = True
            self.next()

        # Build the 'Left-hand side'
        lhs = None

        # First check if the current token 
        # is a '(', which indicated a nested expression,
        # or check if it's an atomic value,
        # or else return a 'failed' state
        if isinstance(self.current, ParOpenToken):
            lhs = p_state.add(self.condition())
        
        elif isinstance(self.current, (IntegerToken, FloatToken, StringToken, IDToken)):
            lhs = p_state.add(self.atom())

        else:
            return p_state.fail(
                InvalidSyntaxError(f"Expected 'int', 'float', 'string', 'variable'")
            )
        
        if p_state.failed(): return p_state
        # self.next()

        # Build the 'Operation'
        if not isinstance(self.current, (EqualToken, NotEqualToken, GreaterToken, GreaterOrEqualToken, LessToken, LessOrEqualToken)):
            return p_state.fail(
                InvalidSyntaxError(f"Expected '==', '!=', '>', '>=', '<', '<='")
            )
        
        expr = self.current
        self.next()

        # Build the 'Right-hand side'
        rhs = None

        # Again, first check if the current token 
        # is a '(', which indicated a nested expression,
        # or check if it's an atomic value,
        # or else return a 'failed' state
        if isinstance(self.current, ParOpenToken):
            rhs = p_state.add(self.condition())
        
        elif isinstance(self.current, (IntegerToken, FloatToken, StringToken, IDToken)):
            rhs = p_state.add(self.atom())

        else:
            return p_state.fail(
                InvalidSyntaxError(f"Expected 'int', 'float', 'string', 'variable'")
            )

        # Look for a ')' when previously
        # a '(' was found at the beginning
        if found_par_open and not isinstance(self.current, ParCloseToken):
            return p_state.fail(InvalidSyntaxError(f"Expected ')'"))
        
        elif found_par_open and isinstance(self.current, ParCloseToken):
            self.next()
        
        return p_state.success(CompareOpNode(lhs, rhs, expr))

    # ==========================================================

    def print_expr(self):
        p_state = ParseState()

        if isinstance(self.current, PrintToken):
            base_token = self.current

            self.next()

            if not isinstance(self.current, (IntegerToken, FloatToken, StringToken, IDToken)):
                return p_state.fail(
                    InvalidSyntaxError(f"Expected 'int', 'float', 'string', 'variable'")
                )
            
            to_print_node = p_state.add(self.expr())
            if p_state.failed(): return p_state
            
            # if not isinstance(self.current, (NewLineToken, EOFToken)):
            #     return p_state.fail(
            #         InvalidSyntaxError(f"Expected 'newline', 'EOF'")
            #     )
            
            return p_state.success(PrintNode(to_print_node, base_token))

        return p_state.fail(
            InvalidSyntaxError(f"Expected '=!'")
        )

    # ==========================================================

    def bin_oper(self, lhs: Union[NumberNode, StringNode, IDNode, BooleanNode]):
        p_state = ParseState()
        oper_token = self.current

        if isinstance(self.current, (AddToken, SubToken, MulToken, DivToken)):
            self.next()
            rhs = p_state.add(self.atom())
            if p_state.failed(): return p_state
            return p_state.success(BinaryOpNode(lhs, rhs, oper_token))

        return p_state.success(lhs)
    
    # ==========================================================