from __future__ import annotations
from typing import Optional, List, Any, Union
from copy import deepcopy
from interpreter.tokens import (
    Token,
    IntegerToken,
    FloatToken,
    StringToken,
    IDToken,
    BooleanToken,
    CommaToken,
    ColonToken,
    ParOpenToken,
    ParCloseToken,
    BracketCloseToken,
    NewLineToken,
    EOFToken,
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
from interpreter.nodes import (
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
from interpreter.errors import (
    Error,
    InvalidSyntaxError,
    NotImplementedError,
)
from interpreter.utils import debug_log


class ParseState:
    """Parser State.

    Attributes:
        node: Initial node of the state.
        error: Optional error to display.
    """

    def __init__(
        self, node: Optional[Any] = None, error: Union[ParseState, Error, None] = None
    ) -> None:
        """Initialise the Parse state.

        Args:
            node: Initial node of the state. Defaults to None.
            error: Optional error to display. Defaults to None.
        """
        self.node = node
        self.error = error

    def __str__(self) -> str:
        if self.error is not None:
            return f"ParseState({self.error})"

        return f"ParseState({self.node})"

    def __repr__(self) -> str:
        return f"ParseState(node={self.node!r}, error={self.error!r})"

    def add(self, state) -> BaseNode:
        """Add Node to state.

        Args:
            state: State to add the node to.

        Returns:
            The added Note.
        """
        if state.error is not None:
            self.error = state.error
        return deepcopy(state.node)

    def success(self, node):
        """Add Node to state.

        Args:
            state: State to add the node to.

        Returns:
            The added Note.
        """
        self.node = deepcopy(node)
        return self

    def fail(self, error: Error):
        """Let the state fail with given Error message.

        Args:
            error: Error to display.

        Returns:
            ParseState containing the Error message.
        """
        if self.error is None:
            self.error = error
        return self

    def failed(self) -> bool:
        """Check if state has failed and has an Error.

        Returns:
            True/False if state has failed.
        """
        return self.error is not None

    def run(self, state):
        """Run the given state.

        Args:
            state: State to run.

        Returns:
            Either the result or the State containing an Error.
        """
        node = self.add(state)
        if self.failed():
            return self
        return self.success(node)


class Parser:
    """Reperesentation of the Moonlet Parser.

    Attributes:
        tokens: Tokens to parse.
        index: Current index of the Parser.
        previous_index: Previous index of the Parser.
        debug_mode: If 'debug mode' is enabled. Defaults to False.
    """

    def __init__(self, tokens: List[Token], debug_mode: bool = False):
        """Initialise the Parser.

        Args:
            tokens: Tokens to parse.
            debug_mode: If 'debug mode' is enabled. Defaults to False.
        """
        self.tokens = tokens
        self.index = -1
        self.previous_index = -2
        self.current = None
        self.previous = None
        self.debug_mode = debug_mode

    def __str__(self) -> str:
        return f"Parser({self.debug_mode})"

    def __repr__(self) -> str:
        return f"Parser(debug_mode={self.debug_mode!r})"

    @debug_log("Parser.set_current")
    def set_current(self):
        """Set the Current Token"""
        if self.index >= 0 and self.index < len(self.tokens):
            self.current = self.tokens[self.index]
            self.previous = self.tokens[self.previous_index]

    @debug_log("Parser.next")
    def next(self):
        """Set the next index and return the current Token.

        Returns:
            Current set Token.
        """
        self.index += 1
        self.previous_index += 1
        self.set_current()
        return self.current

    @debug_log("Parser.parse")
    def parse(self) -> ParseState:
        """Parse the Current set of Tokens.

        Returns:
            ListNode containing the parsed Tokens,
            which are parsed into Nodes.
        """
        p_state = ParseState()

        if len(self.tokens) == 0:
            return p_state.fail(Error("Parse Error", "Can't parse with 0 tokens"))

        self.next()

        if self.current is None:
            return p_state.fail(Error("Parse Error", "No current token was specified"))

        nodes = p_state.add(self.build_nodes())
        if p_state.error:
            return p_state
        return p_state.success(ListNode(nodes))

    @debug_log("Parser.build_nodes")
    def build_nodes(self, nodes: Optional[List] = None):
        """Build the Nodes

        Args:
            nodes: Nodes to build. Defaults to None.

        Returns:
            A list containing the build Nodes.
        """
        p_state = ParseState()
        nodes = list() if nodes is None else nodes

        if isinstance(self.current, EOFToken):
            return p_state.success(nodes)

        elif self.index >= len(self.tokens):
            return p_state.fail(Error("NoEOF", "No 'End Of File'"))

        if isinstance(self.current, NewLineToken):
            self.next()
            return self.build_nodes(nodes)

        statement = p_state.add(self.statement())
        if p_state.failed():
            return p_state
        return self.build_nodes(nodes + [statement])

    @debug_log("Parser.statement")
    def statement(self):
        """Parse a Statement.

        Returns:
            Parsed Node.
        """
        p_state = ParseState()

        if isinstance(
            self.current,
            (VarToken, AssignAddToken, AssignSubToken, AssignMulToken, AssignDivToken),
        ):
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

        return p_state.fail(
            NotImplementedError(f"'{self.current}' Statement is not implemented")
        )

    @debug_log("Parser.expr")
    def expr(self):
        """Parse an Expression.

        Returns:
            Parsed Node.
        """
        p_state = ParseState()

        if isinstance(self.current, ParOpenToken):
            self.next()

            expr = p_state.add(self.expr())
            if p_state.failed():
                return p_state

            if not isinstance(self.current, ParCloseToken):
                return p_state.fail(InvalidSyntaxError("Expected ')'"))

            self.next()
            return p_state.success(expr)

        node = p_state.add(self.atom())
        if p_state.failed():
            return p_state
        return p_state.success(node)

    @debug_log("Parser.atom")
    def atom(self):
        """Parse an Atomic value.

        Returns:
            Parsed Node.
        """
        p_state = ParseState()
        token = self.current

        if isinstance(self.current, IntegerToken) or isinstance(
            self.current, FloatToken
        ):
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

        return p_state.fail(
            NotImplementedError(f"'{self.current}' Atomic value is not implemented")
        )

    @debug_log("Parser.assign_oper")
    def assign_oper(self):
        """Parse an Assign Operator.

        Returns:
            Parsed Node.
        """
        p_state = ParseState()
        # pos_start = self.current.pos.start

        # Check if the current token is a
        # 'Variable' or 'Assign Operation'
        # Otherwise return a 'fail' state
        if isinstance(
            self.current,
            (VarToken, AssignAddToken, AssignSubToken, AssignMulToken, AssignDivToken),
        ):
            base_token = self.current
            self.next()

            if not isinstance(self.current, IDToken):
                return p_state.fail(InvalidSyntaxError("No 'Identifier' was specified"))

            id_node = IDNode(self.current)
            self.next()

            # Check for a 'binary operation'
            if isinstance(self.current, (AddToken, SubToken, MulToken, DivToken)):
                expr = p_state.add(self.bin_oper(id_node))
                if p_state.failed():
                    return p_state

            else:
                expr = p_state.add(self.expr())
                if p_state.failed():
                    return p_state

            self.next()

            if isinstance(base_token, VarToken):
                return p_state.success(VarNode(id_node, expr, base_token))

            return p_state.success(AssignOpNode(id_node, expr, base_token))

        return p_state.fail(InvalidSyntaxError("Expected '=:', '=+', '=-', '=*', '=/'"))

    @debug_log("Parser.func_expr")
    def func_expr(self):
        """Parse a Function expression.

        Returns:
            Parsed Node.
        """
        p_state = ParseState()

        if isinstance(self.current, FuncToken):
            base_token = self.current
            self.next()

            if not isinstance(self.current, IDToken):
                return p_state.fail(InvalidSyntaxError("No 'IDToken' was specified"))

            id_node = IDNode(self.current)
            self.next()

            if not isinstance(self.current, ParOpenToken):
                return p_state.fail(InvalidSyntaxError("Expected '('"))

            self.next()

            arg_nodes = p_state.add(self.func_params())
            if p_state.failed():
                return p_state

            if not isinstance(self.current, ParCloseToken):
                return p_state.fail(InvalidSyntaxError("Expected ')'"))

            self.next()

            if not isinstance(self.current, CodeBlockToken):
                return p_state.fail(InvalidSyntaxError("Expected '={'"))

            start_block = self.current

            self.next()

            body_nodes = p_state.add(self.code_block())
            if p_state.failed():
                return p_state

            if not isinstance(self.current, BracketCloseToken):
                return p_state.fail(InvalidSyntaxError("Expected '}'"))

            end_block = self.current

            self.next()

            return p_state.success(
                FuncNode(
                    id_node, arg_nodes, body_nodes, start_block, end_block, base_token
                )
            )

        return p_state.fail(InvalidSyntaxError("Expected '=|'"))

    @debug_log("Parser.func_params")
    def func_params(self, params: Optional[List] = None):
        """Parse the Function parameters.

        Args:
            params: Parameters to construct.

        Returns:
            Parsed Nodes.
        """
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

    @debug_log("Parser.func_body")
    def func_body(self, nodes: Optional[List] = None):
        """Parse the body of a Function.

        Args:
            nodes: Nodes to construct the body with.

        Returns:
            Parsed Nodes.
        """
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
            if p_state.failed():
                return p_state

            self.next()

            return p_state.success(ListNode(nodes + [statement]))

        statement = p_state.add(self.statement())
        if p_state.failed():
            return p_state

        return self.func_body(nodes + [statement])

    @debug_log("Parser.func_args")
    def func_args(self, args: Optional[List] = None):
        """Parse the Arguments of a Function.

        Args:
            args: The arguments to create.

        Returns:
            Parsed Nodes.
        """
        p_state = ParseState()
        args = list() if args is None else args

        if isinstance(self.current, (IntegerToken, FloatToken, StringToken, IDToken)):
            arg = p_state.add(self.atom())
            if p_state.failed():
                return p_state

            args += [arg]

            if not isinstance(self.current, (CommaToken, ParCloseToken)):
                return p_state.fail(InvalidSyntaxError("Expected ')', ','"))

            return self.func_args(args)

        elif isinstance(self.current, CommaToken):
            self.next()

            if isinstance(self.current, CommaToken):
                return p_state.fail(InvalidSyntaxError("Expected 'value' after ','"))

            return self.func_args(args)

        return p_state.success(ListNode(args))

    @debug_log("Parser.func_call")
    def func_call(self, id_node: Optional[IDNode] = None):
        """Parse a Function Call.

        Args:
            id_node: Identifier of the Call.

        Returns:
            Parsed Node.
        """
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
        if p_state.failed():
            return p_state

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
                    token=base_token,
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
                token=base_token,
            )
        )

    @debug_log("Parser.func_return")
    def func_return(self):
        """Parse a statement.

        Returns:
            Parsed Node.
        """
        p_state = ParseState()
        base_token = self.current

        self.next()

        result = p_state.add(self.atom())
        if p_state.failed():
            return p_state

        if isinstance(self.current, ParOpenToken):
            result = p_state.add(self.func_call(result))
            if p_state.failed():
                return p_state

        return p_state.success(ReturnNode(result, base_token))

    @debug_log("Parser.code_block")
    def code_block(self, nodes: Optional[List] = None):
        """Parse a Code Block from a Function.

        Args:
            nodes: Nodes to construct the code block with.

        Returns:
            Parsed Nodes.
        """
        p_state = ParseState()
        nodes = list() if nodes is None else nodes

        if isinstance(self.current, EOFToken) or self.index >= len(self.tokens):
            return p_state.fail(InvalidSyntaxError("Expected '}'"))

        elif isinstance(self.current, NewLineToken):
            self.next()
            return self.code_block(nodes)

        elif isinstance(self.current, BracketCloseToken):
            return p_state.success(ListNode(nodes))

        statement = p_state.add(self.statement())
        if p_state.failed():
            return p_state

        return self.code_block(nodes + [statement])

    @debug_log("Parser.if_statement")
    def if_statement(self):
        """Parse an If-statement.

        Returns:
            Parsed Node.
        """
        p_state = ParseState()

        if isinstance(self.current, IfToken):
            base_token = self.current

            self.next()

            # Build conditions
            condition = p_state.add(self.condition())
            if p_state.failed():
                return p_state

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
                if p_state.failed():
                    return p_state
                self.next()

            else:
                result_node = p_state.add(self.statement())
                if p_state.failed():
                    return p_state

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
                if p_state.failed():
                    return p_state

                return p_state.success(
                    ConditionsNode(condition, result_node, other_node, base_token)
                )

            return p_state.success(
                ConditionsNode(condition, result_node, None, base_token)
            )

        return p_state.fail(InvalidSyntaxError(f"Expected '=?'"))

    @debug_log("Parser.condition")
    def condition(self):
        """Parse a Conditional statement.

        Returns:
            Parsed Node.
        """
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

        if p_state.failed():
            return p_state
        # self.next()

        # Build the 'Operation'
        if not isinstance(
            self.current,
            (
                EqualToken,
                NotEqualToken,
                GreaterToken,
                GreaterOrEqualToken,
                LessToken,
                LessOrEqualToken,
            ),
        ):
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

    @debug_log("Parser.print_expr")
    def print_expr(self):
        """Parse a Printable expression.

        Returns:
            Parsed Node.
        """
        p_state = ParseState()

        if isinstance(self.current, PrintToken):
            base_token = self.current

            self.next()

            if not isinstance(
                self.current, (IntegerToken, FloatToken, StringToken, IDToken)
            ):
                return p_state.fail(
                    InvalidSyntaxError(f"Expected 'int', 'float', 'string', 'variable'")
                )

            to_print_node = p_state.add(self.expr())
            if p_state.failed():
                return p_state

            return p_state.success(PrintNode(to_print_node, base_token))

        return p_state.fail(InvalidSyntaxError(f"Expected '=!'"))

    # ==========================================================

    @debug_log("Parser.bin_oper")
    def bin_oper(self, lhs: Union[NumberNode, StringNode, IDNode, BooleanNode]):
        """Parse a Binary Operation.

        Returns:
            Parsed Node.
        """
        p_state = ParseState()
        oper_token = self.current

        if isinstance(self.current, (AddToken, SubToken, MulToken, DivToken)):
            self.next()
            rhs = p_state.add(self.atom())
            if p_state.failed():
                return p_state
            return p_state.success(BinaryOpNode(lhs, rhs, oper_token))

        return p_state.success(lhs)
