import unittest
from interpreter import lexer, tokens, position, parser, nodes


class TestTextToToken(unittest.TestCase):
    """Test Text to a valid Token."""

    def test_valid_vartoken_tokenization(self):
        lexial = lexer.Lexer()
        token = lexial.tokenize("=:")
        expected = tokens.VarToken("=:", position.Position(0, 0, 1))
        self.assertEqual(token[0], expected, "Invalid Tokenization, expected 'VarNode'")

    def test_valid_id_tokenization(self):
        lexial = lexer.Lexer()
        token = lexial.tokenize("abcdef")
        expected = tokens.IDToken("abcdef", position.Position(0, 0, 5))
        self.assertEqual(token[0], expected, "Invalid Tokenization, expected 'IDToken'")

    def test_valid_int_tokenization(self):
        lexial = lexer.Lexer()
        token = lexial.tokenize("10")
        expected = tokens.IntegerToken(10, position.Position(0, 0, 1))
        self.assertEqual(
            token[0], expected, "Invalid Tokenization, expected 'IntegerToken'"
        )

    def test_valid_float_tokenization(self):
        lexial = lexer.Lexer()
        token = lexial.tokenize("13.3")
        expected = tokens.FloatToken(13.3, position.Position(0, 0, 3))
        self.assertEqual(
            token[0], expected, "Invalid Tokenization, expected 'FloatToken'"
        )


class TestVariableTokenCreation(unittest.TestCase):
    """Test the Creation of a Variable Token."""

    def test_variable_token_creation(self):
        lexial = lexer.Lexer("=: x 10")
        result, _ = lexial.run()
        expected = [
            tokens.VarToken("=:", position.Position(0, 0, 1)),
            tokens.IDToken("x", position.Position(0, 3, 3)),
            tokens.IntegerToken(10, position.Position(0, 5, 6)),
            tokens.EOFToken(None, tokens.Position(1, 0, 0)),
        ]
        self.assertEqual(result, expected, "Invalid Variable Creation!")

    def test_variable_failing(self):
        lexial = lexer.Lexer("==: x 10")
        result = lexial.run()
        expected = [
            tokens.VarToken("=:", position.Position(0, 0, 1)),
            tokens.IDToken("x", position.Position(0, 3, 3)),
            tokens.IntegerToken(10, position.Position(0, 5, 6)),
            tokens.EOFToken(None, tokens.Position(1, 0, 0)),
        ]
        self.assertNotEqual(result, expected, "Must not be a Variable Token!")


class TestVariableNodeCreation(unittest.TestCase):
    """Test the Creation of a Variable Node."""

    def test_variable_node_creation(self):
        input_tokens = [
            tokens.VarToken("=:", position.Position(0, 0, 1)),
            tokens.IDToken("x", position.Position(0, 3, 3)),
            tokens.IntegerToken(10, position.Position(0, 5, 6)),
            tokens.EOFToken(None, tokens.Position(1, 0, 0)),
        ]

        test_parser = parser.Parser(input_tokens)
        ats = test_parser.parse()

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


if __name__ == "__main__":
    unittest.main()
