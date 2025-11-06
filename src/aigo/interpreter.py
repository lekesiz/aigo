#!/usr/bin/env python3
"""
AIGo Language Interpreter
Simple interpreter for executing AIGo programs
"""

from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from .lexer import Lexer
from .parser import *

class AIGoValue:
    """Base class for AIGo runtime values"""
    pass

@dataclass
class IntValue(AIGoValue):
    value: int
    
    def __str__(self):
        return str(self.value)

@dataclass
class FloatValue(AIGoValue):
    value: float
    
    def __str__(self):
        return str(self.value)

@dataclass
class StringValue(AIGoValue):
    value: str
    
    def __str__(self):
        return self.value

@dataclass
class BoolValue(AIGoValue):
    value: bool
    
    def __str__(self):
        return "true" if self.value else "false"

@dataclass
class VoidValue(AIGoValue):
    def __str__(self):
        return "void"

@dataclass
class ResultValue(AIGoValue):
    is_ok: bool
    value: AIGoValue
    
    def __str__(self):
        if self.is_ok:
            return f"Ok({self.value})"
        else:
            return f"Err({self.value})"

class AIGoError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class Environment:
    """Environment for variable bindings"""
    def __init__(self, parent: Optional['Environment'] = None):
        self.parent = parent
        self.bindings: Dict[str, AIGoValue] = {}
    
    def define(self, name: str, value: AIGoValue):
        self.bindings[name] = value
    
    def get(self, name: str) -> AIGoValue:
        if name in self.bindings:
            return self.bindings[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise AIGoError(f"Undefined variable: {name}")
    
    def set(self, name: str, value: AIGoValue):
        if name in self.bindings:
            self.bindings[name] = value
        elif self.parent:
            self.parent.set(name, value)
        else:
            raise AIGoError(f"Undefined variable: {name}")

class ReturnException(Exception):
    """Exception used for return statement control flow"""
    def __init__(self, value: AIGoValue):
        self.value = value

@dataclass
class Function:
    name: str
    parameters: List[Parameter]
    body: List[Statement]
    closure: Environment

class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.current_env = self.global_env
        self.setup_builtins()
    
    def setup_builtins(self):
        """Setup built-in functions and values"""
        # Built-in functions will be implemented as Python functions
        self.global_env.define("println", self.builtin_println)
        self.global_env.define("Ok", self.builtin_ok)
        self.global_env.define("Err", self.builtin_err)
        self.global_env.define("void", VoidValue())
    
    def builtin_println(self, *args):
        """Built-in println function"""
        output = " ".join(str(arg) for arg in args)
        print(output)
        return ResultValue(True, VoidValue())
    
    def builtin_ok(self, value):
        """Built-in Ok constructor"""
        return ResultValue(True, value)
    
    def builtin_err(self, value):
        """Built-in Err constructor"""
        return ResultValue(False, value)
    
    def evaluate_expression(self, expr: Expression) -> AIGoValue:
        """Evaluate expressions"""
        if isinstance(expr, IntegerLiteral):
            return IntValue(expr.value)
        
        elif isinstance(expr, FloatLiteral):
            return FloatValue(expr.value)
        
        elif isinstance(expr, StringLiteral):
            return StringValue(expr.value)
        
        elif isinstance(expr, BooleanLiteral):
            return BoolValue(expr.value)
        
        elif isinstance(expr, Identifier):
            return self.current_env.get(expr.name)
        
        elif isinstance(expr, BinaryOperation):
            left = self.evaluate_expression(expr.left)
            right = self.evaluate_expression(expr.right)
            return self.evaluate_binary_operation(left, expr.operator, right)
        
        elif isinstance(expr, UnaryOperation):
            if expr.operator == "?":
                # Error propagation
                operand = self.evaluate_expression(expr.operand)
                if isinstance(operand, ResultValue) and not operand.is_ok:
                    raise ReturnException(operand)
                elif isinstance(operand, ResultValue):
                    return operand.value
                else:
                    return operand
            else:
                operand = self.evaluate_expression(expr.operand)
                return self.evaluate_unary_operation(expr.operator, operand)
        
        elif isinstance(expr, FunctionCall):
            function = self.evaluate_expression(expr.function)
            args = [self.evaluate_expression(arg) for arg in expr.arguments]
            return self.call_function(function, args)
        
        elif isinstance(expr, FieldAccess):
            # For now, treat field access as module access (e.g., io.println)
            obj = self.evaluate_expression(expr.object)
            if isinstance(obj, StringValue) and obj.value == "io":
                if expr.field == "println":
                    return self.global_env.get("println")
            raise AIGoError(f"Unknown field access: {expr.object}.{expr.field}")
        
        else:
            raise AIGoError(f"Unknown expression type: {type(expr)}")
    
    def evaluate_binary_operation(self, left: AIGoValue, operator: str, right: AIGoValue) -> AIGoValue:
        """Evaluate binary operations"""
        if operator == "+":
            if isinstance(left, IntValue) and isinstance(right, IntValue):
                return IntValue(left.value + right.value)
            elif isinstance(left, FloatValue) and isinstance(right, FloatValue):
                return FloatValue(left.value + right.value)
            elif isinstance(left, StringValue) and isinstance(right, StringValue):
                return StringValue(left.value + right.value)
        
        elif operator == "-":
            if isinstance(left, IntValue) and isinstance(right, IntValue):
                return IntValue(left.value - right.value)
            elif isinstance(left, FloatValue) and isinstance(right, FloatValue):
                return FloatValue(left.value - right.value)
        
        elif operator == "*":
            if isinstance(left, IntValue) and isinstance(right, IntValue):
                return IntValue(left.value * right.value)
            elif isinstance(left, FloatValue) and isinstance(right, FloatValue):
                return FloatValue(left.value * right.value)
        
        elif operator == "/":
            if isinstance(left, IntValue) and isinstance(right, IntValue):
                return IntValue(left.value // right.value)
            elif isinstance(left, FloatValue) and isinstance(right, FloatValue):
                return FloatValue(left.value / right.value)
        
        elif operator == "==":
            return BoolValue(self.values_equal(left, right))
        
        elif operator == "!=":
            return BoolValue(not self.values_equal(left, right))
        
        elif operator == "<":
            if isinstance(left, IntValue) and isinstance(right, IntValue):
                return BoolValue(left.value < right.value)
            elif isinstance(left, FloatValue) and isinstance(right, FloatValue):
                return BoolValue(left.value < right.value)
        
        elif operator == "<=":
            if isinstance(left, IntValue) and isinstance(right, IntValue):
                return BoolValue(left.value <= right.value)
            elif isinstance(left, FloatValue) and isinstance(right, FloatValue):
                return BoolValue(left.value <= right.value)
        
        elif operator == ">=":
            if isinstance(left, IntValue) and isinstance(right, IntValue):
                return BoolValue(left.value >= right.value)
            elif isinstance(left, FloatValue) and isinstance(right, FloatValue):
                return BoolValue(left.value >= right.value)
        
        elif operator == "&&":
            if isinstance(left, BoolValue) and isinstance(right, BoolValue):
                return BoolValue(left.value and right.value)
        
        elif operator == "||":
            if isinstance(left, BoolValue) and isinstance(right, BoolValue):
                return BoolValue(left.value or right.value)
        
        raise AIGoError(f"Unsupported binary operation: {left} {operator} {right}")
    
    def evaluate_unary_operation(self, operator: str, operand: AIGoValue) -> AIGoValue:
        """Evaluate unary operations"""
        if operator == "-":
            if isinstance(operand, IntValue):
                return IntValue(-operand.value)
            elif isinstance(operand, FloatValue):
                return FloatValue(-operand.value)
        
        elif operator == "!":
            if isinstance(operand, BoolValue):
                return BoolValue(not operand.value)
        
        raise AIGoError(f"Unsupported unary operation: {operator} {operand}")
    
    def values_equal(self, left: AIGoValue, right: AIGoValue) -> bool:
        """Check if two values are equal"""
        if type(left) != type(right):
            return False
        
        if isinstance(left, IntValue):
            return left.value == right.value
        elif isinstance(left, FloatValue):
            return left.value == right.value
        elif isinstance(left, StringValue):
            return left.value == right.value
        elif isinstance(left, BoolValue):
            return left.value == right.value
        elif isinstance(left, VoidValue):
            return True
        
        return False
    
    def call_function(self, function: Any, args: List[AIGoValue]) -> AIGoValue:
        """Call a function"""
        if callable(function):
            # Built-in function
            return function(*args)
        elif isinstance(function, Function):
            # User-defined function
            if len(args) != len(function.parameters):
                raise AIGoError(f"Function {function.name} expects {len(function.parameters)} arguments, got {len(args)}")
            
            # Create new environment for function execution
            func_env = Environment(function.closure)
            
            # Bind parameters
            for param, arg in zip(function.parameters, args):
                func_env.define(param.name, arg)
            
            # Execute function body
            old_env = self.current_env
            self.current_env = func_env
            
            try:
                for stmt in function.body:
                    self.execute_statement(stmt)
                # If no return statement, return void
                return VoidValue()
            except ReturnException as ret:
                return ret.value
            finally:
                self.current_env = old_env
        
        else:
            raise AIGoError(f"Cannot call non-function value: {function}")
    
    def execute_statement(self, stmt: Statement):
        """Execute statements"""
        if isinstance(stmt, VariableDeclaration):
            value = VoidValue()
            if stmt.value:
                value = self.evaluate_expression(stmt.value)
            self.current_env.define(stmt.name, value)
        
        elif isinstance(stmt, Assignment):
            value = self.evaluate_expression(stmt.value)
            if isinstance(stmt.target, Identifier):
                self.current_env.set(stmt.target.name, value)
            else:
                raise AIGoError("Complex assignment targets not supported yet")
        
        elif isinstance(stmt, ExpressionStatement):
            self.evaluate_expression(stmt.expression)
        
        elif isinstance(stmt, ReturnStatement):
            value = VoidValue()
            if stmt.value:
                value = self.evaluate_expression(stmt.value)
            raise ReturnException(value)
        
        elif isinstance(stmt, IfStatement):
            condition = self.evaluate_expression(stmt.condition)
            if isinstance(condition, BoolValue) and condition.value:
                for s in stmt.then_block:
                    self.execute_statement(s)
            elif stmt.else_block:
                for s in stmt.else_block:
                    self.execute_statement(s)
        
        elif isinstance(stmt, WhileStatement):
            while True:
                condition = self.evaluate_expression(stmt.condition)
                if not (isinstance(condition, BoolValue) and condition.value):
                    break
                for s in stmt.body:
                    self.execute_statement(s)
        
        elif isinstance(stmt, FunctionDeclaration):
            func = Function(stmt.name, stmt.parameters, stmt.body, self.current_env)
            self.current_env.define(stmt.name, func)
        
        elif isinstance(stmt, Block):
            for s in stmt.statements:
                self.execute_statement(s)
        
        else:
            raise AIGoError(f"Unknown statement type: {type(stmt)}")
    
    def interpret_program(self, program: Program):
        """Interpret a complete program"""
        # Handle imports (simplified)
        for imp in program.imports:
            if imp.module_path == "std.io":
                self.current_env.define("io", StringValue("io"))
        
        # Execute declarations
        for decl in program.declarations:
            self.execute_statement(decl)
        
        # Call main function if it exists
        try:
            main_func = self.current_env.get("main")
            if isinstance(main_func, Function):
                result = self.call_function(main_func, [])
                print(f"Program finished with result: {result}")
        except AIGoError as e:
            if "Undefined variable: main" not in str(e):
                raise

def run_aigo_code(source_code: str):
    """Run AIGo source code"""
    try:
        # Tokenize
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        # Parse
        parser = Parser(tokens)
        ast = parser.parse_program()
        
        # Interpret
        interpreter = Interpreter()
        interpreter.interpret_program(ast)
        
    except (ParseError, AIGoError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    # Test the interpreter
    test_code = '''
    module main
    
    import std.io
    
    fn main() -> Result<void, Error> {
        let x: i32 = 42
        let name: string = "AIGo"
        io.println("Hello from AIGo!")
        io.println("x =", x)
        io.println("name =", name)
        return Ok(void)
    }
    '''
    
    print("Running AIGo code:")
    print(test_code)
    print("\nOutput:")
    run_aigo_code(test_code)

