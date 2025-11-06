"""
Unit tests for AIGo Lexer
"""

import pytest
from aigo.lexer import Lexer, TokenType


class TestLexer:
    """Test cases for the Lexer class"""

    def test_lexer_initialization(self):
        """Test that lexer initializes correctly"""
        code = "let x = 42"
        lexer = Lexer(code)
        assert lexer.source == code
        assert lexer.position == 0
        assert lexer.line == 1
        assert lexer.column == 1

    def test_tokenize_simple_variable(self):
        """Test tokenizing a simple variable declaration"""
        code = "let x: i32 = 42"
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        expected_types = [
            TokenType.LET,
            TokenType.IDENTIFIER,
            TokenType.COLON,
            TokenType.I32,
            TokenType.ASSIGN,
            TokenType.INTEGER,
            TokenType.EOF
        ]

        for i, expected_type in enumerate(expected_types):
            assert tokens[i].type == expected_type, \
                f"Token {i} should be {expected_type}, got {tokens[i].type}"

    def test_tokenize_keywords(self):
        """Test that keywords are recognized correctly"""
        code = "fn if else while return"
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        expected_types = [
            TokenType.FN,
            TokenType.IF,
            TokenType.ELSE,
            TokenType.WHILE,
            TokenType.RETURN,
            TokenType.EOF
        ]

        for i, expected_type in enumerate(expected_types):
            assert tokens[i].type == expected_type

    def test_tokenize_numbers(self):
        """Test tokenizing integers and floats"""
        code = "42 3.14"
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        assert tokens[0].type == TokenType.INTEGER
        assert tokens[0].value == "42"
        assert tokens[1].type == TokenType.FLOAT
        assert tokens[1].value == "3.14"

    def test_tokenize_strings(self):
        """Test tokenizing string literals"""
        code = '"Hello, World!"'
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        assert tokens[0].type == TokenType.STRING
        assert tokens[0].value == "Hello, World!"

    def test_tokenize_operators(self):
        """Test tokenizing operators"""
        code = "+ - * / == != < > <= >= && ||"
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        expected_types = [
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
            TokenType.EQUAL,
            TokenType.NOT_EQUAL,
            TokenType.LESS_THAN,
            TokenType.GREATER_THAN,
            TokenType.LESS_EQUAL,
            TokenType.GREATER_EQUAL,
            TokenType.AND,
            TokenType.OR,
            TokenType.EOF
        ]

        for i, expected_type in enumerate(expected_types):
            assert tokens[i].type == expected_type

    def test_tokenize_comment(self):
        """Test that comments are tokenized"""
        code = "// This is a comment"
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        assert tokens[0].type == TokenType.COMMENT

    def test_line_and_column_tracking(self):
        """Test that line and column numbers are tracked correctly"""
        code = "let\nx"
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        # 'let' should be on line 1
        assert tokens[0].line == 1

        # 'x' should be on line 2
        assert tokens[2].line == 2


class TestLexerEdgeCases:
    """Test edge cases and error conditions"""

    def test_empty_string(self):
        """Test tokenizing an empty string"""
        lexer = Lexer("")
        tokens = lexer.tokenize()
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF

    def test_whitespace_only(self):
        """Test tokenizing whitespace"""
        lexer = Lexer("   \t  \n  ")
        tokens = lexer.tokenize()
        # Should skip whitespace and return only EOF
        assert tokens[0].type == TokenType.NEWLINE
        assert tokens[1].type == TokenType.EOF

    def test_string_with_escape_sequences(self):
        """Test strings with escape sequences"""
        code = r'"Hello\nWorld\t!"'
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        assert tokens[0].type == TokenType.STRING
        assert "\n" in tokens[0].value
        assert "\t" in tokens[0].value


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
