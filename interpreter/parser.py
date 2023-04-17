from typing import Optional, List, Tuple
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
from .nodes import (
    NumberNode,
    StringNode,
    IDNode,
    ListNode,
    ParamNode,
    AssignOpNode,
    VarNode,
    ReturnNode,
    FuncNode,
    CallNode,
)
from .errors import (
    Error,
    InvalidSyntaxError,
    NotImplementedError,
)

class ParseState:
    
    def __init__(self):
        self.node = None
        self.error = None

    def add(self, state):
        if state.error is not None:
            self.error = state.error
        return state.node
    
    def prev(self):
        pass

    def success(self, node):
        self.node = node
        return self
    
    def fail(self, error: Error):
        if self.error is None: self.error = error
        return self
    
    def failed(self) -> bool:
        return self.error is not None


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.current = None

    def set_current(self):
        if self.index >= 0 and self.index < len(self.tokens):
            self.current = self.tokens[self.index]

    def next(self):
        self.index += 1
        self.set_current()

        # print(f"NEXT[{self.index:>2}] {'>>': ^4} {self.current}")
        
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
            result = p_state.add(self.assign_oper())
            if p_state.failed(): return p_state
            return p_state.success(result)
        
        elif isinstance(self.current, FuncToken):
            result = p_state.add(self.func_expr())
            if p_state.failed(): return p_state
            return p_state.success(result)

        elif isinstance(self.current, ReturnToken):
            return_token = self.current
            
            self.next()

            result = p_state.add(self.atom())
            if p_state.failed(): return p_state
            return p_state.success(ReturnNode(result, return_token))
        
        elif isinstance(self.current, CallToken):
            result = p_state.add(self.func_call())
            if p_state.failed(): return p_state
            return p_state.success(result)
           
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
            return p_state.success(NumberNode(token))
        
        elif isinstance(self.current, StringToken):
            self.next()
            return p_state.success(StringNode(token))
        
        elif isinstance(self.current, IDToken):
            self.next()
            return p_state.success(IDNode(token))

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
            
            self.next()

            if not isinstance(self.current, NewLineToken):
                return p_state.fail(InvalidSyntaxError("Expected a 'Newline' after '={'"))
            
            self.next()
            
            body_nodes = p_state.add(self.func_body())
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

    def func_call(self):
        p_state = ParseState()
        base_token = self.current

        if isinstance(self.current, CallToken):
            self.next()

        # Look for the id/name of the function to call
        if not isinstance(self.current, IDToken):
            return p_state.fail(
                InvalidSyntaxError("Expected 'name' of function to call")
            )
        
        id_node = IDNode(self.current)
        self.next()

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
                token=base_token
            )
        )

    # ==========================================================

    def bin_oper(self, lhs, ops, rhs=None):
        p_state = ParseState()
        
        if rhs is None:
            rhs = lhs
        
        left = p_state.add(lhs())
        if p_state.failed(): return p_state

        return p_state.success(left)