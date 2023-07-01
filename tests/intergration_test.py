import unittest
from interpreter import tokens, lexer, nodes, parser, program, position


class IntergrationTest(unittest.TestCase):
    def test_intergration(self):
        test_lexer = lexer.Lexer("=: x 10")
        lexer_tokens, lexer_error = test_lexer.run()

        # Validate if Lexer didn't caused an Error
        self.assertEqual(
            lexer_error, None, "Lexer caused an Error during it's processing"
        )

        # Validate Token Creation
        expected_tokens = [
            tokens.VarToken("=:", position.Position(0, 0, 1)),
            tokens.IDToken("x", position.Position(0, 3, 3)),
            tokens.IntegerToken(10, position.Position(0, 5, 6)),
            tokens.EOFToken(None, tokens.Position(1, 0, 0)),
        ]
        self.assertEqual(lexer_tokens, expected_tokens, "Invalid Variable Creation!")

        test_parser = parser.Parser(lexer_tokens)
        ats = test_parser.parse()

        # Validate if Parser didn't caused an Error
        self.assertEqual(
            ats.error, None, "Parser caused an Error during it's processing"
        )

        # Validate Nodes Creation
        expected_list_node = nodes.ListNode(
            [
                nodes.VarNode(
                    id=nodes.IDNode(
                        token=tokens.IDToken(
                            value="x", pos=position.Position(line=0, start=3, end=3)
                        )
                    ),
                    value=nodes.NumberNode(
                        token=tokens.IntegerToken(
                            value=10, pos=position.Position(line=0, start=5, end=6)
                        )
                    ),
                    token=tokens.VarToken(
                        value="=:", pos=position.Position(line=0, start=0, end=1)
                    ),
                )
            ]
        )

        self.assertEqual(
            ats.node,
            expected_list_node,
            "Root Node of ATS has an Invalid value",
        )
        self.assertEqual(
            ats.node.items,
            expected_list_node.items,
            "Parsed Nodes have an Invalid ATS",
        )

        test_program = program.Program()
        program_scope = program.Scope(name="<Program>", origin=ats.node)
        program_result = test_program.exec(ats.node, program_scope)

        # Validate if Program didn't caused an Error
        self.assertEqual(
            program_result.error, None, "Program caused an Error during it's processing"
        )

        # Validate Program Scope
        expected_scope_args = {"x": "10"}

        self.assertEqual(
            str(program_scope.format_args()),
            str(expected_scope_args),
            "Program caused an Error during it's processing",
        )


if __name__ == "__main__":
    unittest.main()
