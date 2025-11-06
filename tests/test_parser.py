"""
Unit tests for AIGo Parser
"""

import pytest
from aigo.lexer import Lexer
from aigo.parser import (
    Parser, Program, FunctionDeclaration, VariableDeclaration,
    IntegerLiteral, StringLiteral, BooleanLiteral, Identifier,
    BinaryOperation, ExpressionStatement, ReturnStatement, ParseError
)


class TestParser:
    """Test cases for the Parser class"""

    def test_parser_initialization(self):
        """Test that parser initializes correctly"""
        code = "let x = 42"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        assert parser is not None
        assert parser.position == 0

    def test_parse_variable_declaration(self):
        """Test parsing a variable declaration"""
        code = "let x: i32 = 42"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse_program()

        assert len(program.declarations) == 1
        decl = program.declarations[0]
        assert isinstance(decl, VariableDeclaration)
        assert decl.name == "x"
        assert isinstance(decl.value, IntegerLiteral)
        assert decl.value.value == 42

    def test_parse_function_declaration(self):
        """Test parsing a function declaration"""
        code = """
        fn add(a: i32, b: i32) -> i32 {
            return a + b
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse_program()

        assert len(program.declarations) == 1
        func = program.declarations[0]
        assert isinstance(func, FunctionDeclaration)
        assert func.name == "add"
        assert len(func.parameters) == 2
        assert func.parameters[0].name == "a"
        assert func.parameters[1].name == "b"

    def test_parse_module_declaration(self):
        """Test parsing a module declaration"""
        code = "module main"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse_program()

        assert program.module is not None
        assert program.module.name == "main"

    def test_parse_import_statement(self):
        """Test parsing import statements"""
        code = """
        module main
        import std.io
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse_program()

        assert len(program.imports) == 1
        assert program.imports[0].module_path == "std.io"

    def test_parse_binary_operation(self):
        """Test parsing binary operations"""
        code = "let result = 1 + 2"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse_program()

        decl = program.declarations[0]
        assert isinstance(decl.value, BinaryOperation)
        assert decl.value.operator == "+"
        assert isinstance(decl.value.left, IntegerLiteral)
        assert isinstance(decl.value.right, IntegerLiteral)

    def test_parse_string_literal(self):
        """Test parsing string literals"""
        code = 'let name = "AIGo"'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse_program()

        decl = program.declarations[0]
        assert isinstance(decl.value, StringLiteral)
        assert decl.value.value == "AIGo"

    def test_parse_boolean_literal(self):
        """Test parsing boolean literals"""
        code = "let flag = true"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse_program()

        decl = program.declarations[0]
        assert isinstance(decl.value, BooleanLiteral)
        assert decl.value.value == True

    def test_parse_complete_program(self):
        """Test parsing a complete program"""
        code = """
        module main

        import std.io

        fn main() -> Result<void, Error> {
            let x: i32 = 42
            return Ok(void)
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse_program()

        assert program.module is not None
        assert len(program.imports) == 1
        assert len(program.declarations) == 1
        assert isinstance(program.declarations[0], FunctionDeclaration)


class TestParserErrorHandling:
    """Test error handling in parser"""

    def test_unexpected_token(self):
        """Test parser error on unexpected token"""
        code = "let = 42"  # Missing identifier
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)

        with pytest.raises(ParseError):
            parser.parse_program()

    def test_missing_closing_brace(self):
        """Test parser error on missing closing brace"""
        code = "fn test() {"  # Missing closing brace
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)

        with pytest.raises(ParseError):
            parser.parse_program()


class TestParserComplexExpressions:
    """Test parsing complex expressions"""

    def test_nested_binary_operations(self):
        """Test parsing nested binary operations"""
        code = "let result = 1 + 2 * 3"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse_program()

        decl = program.declarations[0]
        assert isinstance(decl.value, BinaryOperation)
        # Should respect operator precedence

    def test_function_call_parsing(self):
        """Test parsing function calls"""
        code = "let result = add(1, 2)"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse_program()

        decl = program.declarations[0]
        # Function call should be parsed correctly


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
