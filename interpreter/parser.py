from typing import Optional, List, Tuple

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

        # print(f"NEXT[{self.index}] >> {self.current}")
        
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

        if isinstance(self.current, EndOfFile):
            return p_state.success(nodes)
        
        elif self.index >= len(self.tokens):
            return p_state.fail(Error('NoEOF', "No 'End Of File'"))
        
        if isinstance(self.current, NewLine):
            self.next()
            return self.build_nodes(nodes)
        
        statement = p_state.add(self.statement())
        if p_state.failed(): return p_state
        return self.build_nodes(nodes + [statement])
    
    # ==========================================================

    def statement(self):
        p_state = ParseState()
        # pos_start = self.current.pos.start
        
        if isinstance(self.current, (Variable, AssignAdd, AssignSub, AssignMul, AssignDev)):
            result = p_state.add(self.assign_oper())
            if p_state.failed(): return p_state
            return p_state.success(result)
        
        elif isinstance(self.current, Func):
            result = p_state.add(self.func_expr())
            if p_state.failed(): return p_state
            return p_state.success(result)

        elif isinstance(self.current, Return):
            return_token = self.current
            
            self.next()

            result = p_state.add(self.atom())
            if p_state.failed(): return p_state
            return p_state.success(ReturnNode(result, return_token))
           
        return p_state.fail(NotImplementedError(f"'{self.current.type}' Statement is not implemented"))
            
    def expr(self):
        p_state = ParseState()

        if isinstance(self.current, ParOpen):
            self.next()
            
            expr = p_state.add(self.expr())
            if p_state.failed(): return p_state

            if not isinstance(self.current, ParClose):
                return p_state.fail(InvalidSyntaxError("Expected ')'"))
            
            self.next()
            return p_state.success(expr)
        
        node = p_state.add(self.atom())
        if p_state.failed(): return p_state

        return p_state.success(node)

    def atom(self):
        p_state = ParseState()
        token = self.current

        if isinstance(self.current, Integer) or isinstance(self.current, Float):
            self.next()
            return p_state.success(NumberNode(token))
        
        elif isinstance(self.current, String):
            self.next()
            return p_state.success(StringNode(token))
        
        elif isinstance(self.current, Identifier):
            self.next()
            return p_state.success(IDNode(token))

        return p_state.fail(NotImplementedError(f"'{self.current.type}' Atomic value is not implemented"))

    # ==========================================================

    def assign_oper(self):
        p_state = ParseState()
        # pos_start = self.current.pos.start

        # Check if the current token is a 'Variable'
        # Otherwise return a 'fail' state
        if isinstance(self.current, (Variable, AssignAdd, AssignSub, AssignMul, AssignDev)):
            base_token = self.current
            self.next()
        
            if not isinstance(self.current, Identifier):
                return p_state.fail(
                    InvalidSyntaxError("No 'Identifier' was specified")
                )
            
            id_node = IDNode(self.current)
            self.next()

            expr = p_state.add(self.expr())
            if p_state.failed(): return p_state

            self.next()

            if isinstance(base_token, Variable):
                return p_state.success(VarNode(id_node, expr, base_token))
            
            return p_state.success(AssignOpNode(id_node, expr, base_token))

        return p_state.fail(InvalidSyntaxError("Expected '=:', '=+', '=-', '=*', '=/'"))
    
    def func_expr(self):
        p_state = ParseState()

        if isinstance(self.current, Func):
            base_token = self.current
            self.next()

            if not isinstance(self.current, Identifier):
                return p_state.fail(
                    InvalidSyntaxError("No 'Identifier' was specified")
                )
            
            id_node = IDNode(self.current)
            self.next()

            if not isinstance(self.current, ParOpen):
                return p_state.fail(InvalidSyntaxError("Expected '('"))

            self.next()
            
            arg_nodes = p_state.add(self.func_args())
            if p_state.failed(): return p_state

            if not isinstance(self.current, ParClose):
                return p_state.fail(InvalidSyntaxError("Expected ')'"))

            self.next()

            if not isinstance(self.current, CodeBlock):
                return p_state.fail(InvalidSyntaxError("Expected '={'"))
            
            start_block = self.current
            
            self.next()

            if not isinstance(self.current, NewLine):
                return p_state.fail(InvalidSyntaxError("Expected a 'Newline' after '={'"))
            
            self.next()
            
            body_nodes = p_state.add(self.func_body())
            if p_state.failed(): return p_state
            
            if not isinstance(self.current, BracketClose):
                return p_state.fail(InvalidSyntaxError("Expected '}'"))
            
            end_block = self.current

            self.next()

            return p_state.success(FuncNode(id_node, arg_nodes, body_nodes, start_block, end_block, base_token))

        return p_state.fail(InvalidSyntaxError("Expected '=|'"))
    
    def func_args(self, args: Optional[List] = None):
        p_state = ParseState()
        args = list() if args is None else args

        if isinstance(self.current, Identifier):
            args += [IDNode(self.current)]
            self.next()
            return self.func_args(args)
        
        elif isinstance(self.current, Comma):
            self.next()
            return self.func_args(args)

        return p_state.success(args)
    
    def func_body(self, nodes: Optional[List] = None):
        p_state = ParseState()
        nodes = list() if nodes is None else nodes

        if isinstance(self.current, EndOfFile) or self.index >= len(self.tokens):
            return p_state.fail(InvalidSyntaxError("Expected '=>'"))

        elif isinstance(self.current, NewLine):
            self.next()
            return self.func_body(nodes)

        elif isinstance(self.current, Return):
            statement = p_state.add(self.statement())
            if p_state.failed(): return p_state

            self.next()

            return p_state.success(nodes + [statement])

        statement = p_state.add(self.statement())
        if p_state.failed(): return p_state

        return self.func_body(nodes + [statement])

    # ==========================================================

    def bin_oper(self, lhs, ops, rhs=None):
        p_state = ParseState()
        
        if rhs is None:
            rhs = lhs
        
        left = p_state.add(lhs())
        if p_state.failed(): return p_state

        return p_state.success(left)