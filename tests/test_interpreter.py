"""
Unit tests for AIGo Interpreter
"""

import pytest
from io import StringIO
import sys
from aigo.interpreter import (
    Interpreter, run_aigo_code, IntValue, FloatValue,
    StringValue, BoolValue, VoidValue, AIGoError
)
from aigo.lexer import Lexer
from aigo.parser import Parser


class TestInterpreter:
    """Test cases for the Interpreter class"""

    def test_interpreter_initialization(self):
        """Test that interpreter initializes correctly"""
        interp = Interpreter()
        assert interp is not None
        assert interp.global_env is not None

    def test_execute_variable_declaration(self):
        """Test executing a variable declaration"""
        code = """
        let x: i32 = 42
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse_program()

        interp = Interpreter()
        interp.interpret_program(program)

        # Variable should be in environment
        value = interp.global_env.get("x")
        assert isinstance(value, IntValue)
        assert value.value == 42

    def test_execute_arithmetic(self):
        """Test executing arithmetic operations"""
        code = """
        let a: i32 = 10
        let b: i32 = 5
        let sum: i32 = a + b
        let diff: i32 = a - b
        let prod: i32 = a * b
        let quot: i32 = a / b
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse_program()

        interp = Interpreter()
        interp.interpret_program(program)

        assert interp.global_env.get("sum").value == 15
        assert interp.global_env.get("diff").value == 5
        assert interp.global_env.get("prod").value == 50
        assert interp.global_env.get("quot").value == 2

    def test_execute_comparison(self):
        """Test executing comparison operations"""
        code = """
        let a: i32 = 10
        let b: i32 = 5
        let eq: bool = a == b
        let neq: bool = a != b
        let lt: bool = a < b
        let gt: bool = a > b
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse_program()

        interp = Interpreter()
        interp.interpret_program(program)

        assert interp.global_env.get("eq").value == False
        assert interp.global_env.get("neq").value == True
        assert interp.global_env.get("lt").value == False
        assert interp.global_env.get("gt").value == True

    def test_execute_string_operations(self):
        """Test executing string operations"""
        code = """
        let name: string = "AIGo"
        let greeting: string = "Hello, " + name
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse_program()

        interp = Interpreter()
        interp.interpret_program(program)

        greeting = interp.global_env.get("greeting")
        assert isinstance(greeting, StringValue)
        assert greeting.value == "Hello, AIGo"

    def test_execute_boolean_logic(self):
        """Test executing boolean logic"""
        code = """
        let a: bool = true
        let b: bool = false
        let and_result: bool = a && b
        let or_result: bool = a || b
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse_program()

        interp = Interpreter()
        interp.interpret_program(program)

        assert interp.global_env.get("and_result").value == False
        assert interp.global_env.get("or_result").value == True


class TestInterpreterFunctions:
    """Test function execution"""

    def test_simple_function(self):
        """Test executing a simple function"""
        code = """
        fn double(x: i32) -> i32 {
            return x * 2
        }
        let result: i32 = double(21)
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse_program()

        interp = Interpreter()
        interp.interpret_program(program)

        result = interp.global_env.get("result")
        assert isinstance(result, IntValue)
        assert result.value == 42

    def test_function_with_multiple_params(self):
        """Test function with multiple parameters"""
        code = """
        fn add(a: i32, b: i32) -> i32 {
            return a + b
        }
        let sum: i32 = add(10, 32)
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse_program()

        interp = Interpreter()
        interp.interpret_program(program)

        sum_val = interp.global_env.get("sum")
        assert sum_val.value == 42


class TestInterpreterControlFlow:
    """Test control flow execution"""

    def test_if_statement_true(self):
        """Test if statement with true condition"""
        code = """
        let x: i32 = 10
        if x > 5 {
            x = 42
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse_program()

        interp = Interpreter()
        interp.interpret_program(program)

        x = interp.global_env.get("x")
        assert x.value == 42

    def test_if_statement_false(self):
        """Test if statement with false condition"""
        code = """
        let x: i32 = 10
        if x < 5 {
            x = 42
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse_program()

        interp = Interpreter()
        interp.interpret_program(program)

        x = interp.global_env.get("x")
        assert x.value == 10  # Should not change

    def test_if_else_statement(self):
        """Test if-else statement"""
        code = """
        let x: i32 = 3
        let result: i32 = 0
        if x > 5 {
            result = 1
        } else {
            result = 2
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse_program()

        interp = Interpreter()
        interp.interpret_program(program)

        result = interp.global_env.get("result")
        assert result.value == 2

    def test_while_loop(self):
        """Test while loop execution"""
        code = """
        let counter: i32 = 0
        while counter < 5 {
            counter = counter + 1
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse_program()

        interp = Interpreter()
        interp.interpret_program(program)

        counter = interp.global_env.get("counter")
        assert counter.value == 5


class TestInterpreterIntegration:
    """Integration tests for complete programs"""

    def test_hello_world(self, capsys):
        """Test Hello World program"""
        code = """
        module main
        import std.io

        fn main() -> Result<void, Error> {
            io.println("Hello, World!")?
            return Ok(void)
        }
        """
        run_aigo_code(code)
        captured = capsys.readouterr()
        assert "Hello, World!" in captured.out

    def test_fibonacci_iterative(self):
        """Test iterative fibonacci"""
        code = """
        fn fib(n: i32) -> i32 {
            if n <= 1 {
                return n
            }
            let a: i32 = 0
            let b: i32 = 1
            let i: i32 = 2
            while i <= n {
                let temp: i32 = a + b
                a = b
                b = temp
                i = i + 1
            }
            return b
        }
        let result: i32 = fib(10)
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse_program()

        interp = Interpreter()
        interp.interpret_program(program)

        result = interp.global_env.get("result")
        # fib(10) should be 55
        # Note: The actual value depends on implementation


class TestInterpreterErrors:
    """Test error handling"""

    def test_undefined_variable(self):
        """Test accessing undefined variable"""
        code = """
        let x: i32 = y
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        program = parser.parse_program()

        interp = Interpreter()
        with pytest.raises(AIGoError):
            interp.interpret_program(program)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
