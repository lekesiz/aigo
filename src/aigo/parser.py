#!/usr/bin/env python3
"""
AIGo Language Parser
Builds Abstract Syntax Tree (AST) from tokens
"""

from typing import List, Optional, Union, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
from .lexer import Token, TokenType, Lexer

# AST Node Base Classes
class ASTNode(ABC):
    pass

class Expression(ASTNode):
    pass

class Statement(ASTNode):
    pass

class Type(ASTNode):
    pass

# Type Nodes
@dataclass
class PrimitiveType(Type):
    name: str

@dataclass
class GenericType(Type):
    name: str
    type_args: List[Type]

# Expression Nodes
@dataclass
class IntegerLiteral(Expression):
    value: int

@dataclass
class FloatLiteral(Expression):
    value: float

@dataclass
class StringLiteral(Expression):
    value: str

@dataclass
class BooleanLiteral(Expression):
    value: bool

@dataclass
class Identifier(Expression):
    name: str

@dataclass
class BinaryOperation(Expression):
    left: Expression
    operator: str
    right: Expression

@dataclass
class UnaryOperation(Expression):
    operator: str
    operand: Expression

@dataclass
class FunctionCall(Expression):
    function: Expression
    arguments: List[Expression]

@dataclass
class FieldAccess(Expression):
    object: Expression
    field: str

# Statement Nodes
@dataclass
class VariableDeclaration(Statement):
    name: str
    type_annotation: Optional[Type]
    value: Optional[Expression]
    is_mutable: bool

@dataclass
class Assignment(Statement):
    target: Expression
    value: Expression

@dataclass
class ExpressionStatement(Statement):
    expression: Expression

@dataclass
class ReturnStatement(Statement):
    value: Optional[Expression]

@dataclass
class IfStatement(Statement):
    condition: Expression
    then_block: List[Statement]
    else_block: Optional[List[Statement]]

@dataclass
class WhileStatement(Statement):
    condition: Expression
    body: List[Statement]

@dataclass
class Block(Statement):
    statements: List[Statement]

# Function and Module Nodes
@dataclass
class Parameter:
    name: str
    type_annotation: Type

@dataclass
class FunctionDeclaration(Statement):
    name: str
    parameters: List[Parameter]
    return_type: Optional[Type]
    body: List[Statement]

@dataclass
class ImportStatement(Statement):
    module_path: str

@dataclass
class ModuleDeclaration(Statement):
    name: str

@dataclass
class Program(ASTNode):
    module: Optional[ModuleDeclaration]
    imports: List[ImportStatement]
    declarations: List[Statement]

class ParseError(Exception):
    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        super().__init__(f"Parse error at line {token.line}, column {token.column}: {message}")

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def advance(self):
        if self.position < len(self.tokens) - 1:
            self.position += 1
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = Token(TokenType.EOF, "", 0, 0)
    
    def peek(self, offset: int = 1) -> Token:
        peek_pos = self.position + offset
        if peek_pos < len(self.tokens):
            return self.tokens[peek_pos]
        return Token(TokenType.EOF, "", 0, 0)
    
    def expect(self, token_type: TokenType) -> Token:
        if self.current_token.type != token_type:
            raise ParseError(f"Expected {token_type.value}, got {self.current_token.type.value}", 
                           self.current_token)
        token = self.current_token
        self.advance()
        return token
    
    def match(self, *token_types: TokenType) -> bool:
        return self.current_token.type in token_types
    
    def skip_newlines(self):
        while self.current_token.type == TokenType.NEWLINE:
            self.advance()
    
    def parse_type(self) -> Type:
        """Parse type annotations"""
        if self.match(TokenType.I32, TokenType.I64, TokenType.F32, TokenType.F64, 
                     TokenType.BOOL, TokenType.STRING_TYPE, TokenType.VOID):
            type_name = self.current_token.value
            self.advance()
            return PrimitiveType(type_name)
        elif self.current_token.type == TokenType.IDENTIFIER:
            type_name = self.current_token.value
            self.advance()
            
            # Check for generic types like Result<T, E>
            if self.current_token.type == TokenType.LESS_THAN:
                self.advance()
                type_args = []
                
                while not self.match(TokenType.GREATER_THAN):
                    type_args.append(self.parse_type())
                    if self.current_token.type == TokenType.COMMA:
                        self.advance()
                
                self.expect(TokenType.GREATER_THAN)
                return GenericType(type_name, type_args)
            else:
                return PrimitiveType(type_name)
        else:
            raise ParseError(f"Expected type, got {self.current_token.type.value}", self.current_token)
    
    def parse_primary_expression(self) -> Expression:
        """Parse primary expressions (literals, identifiers, parenthesized expressions)"""
        if self.current_token.type == TokenType.INTEGER:
            value = int(self.current_token.value)
            self.advance()
            return IntegerLiteral(value)
        
        elif self.current_token.type == TokenType.FLOAT:
            value = float(self.current_token.value)
            self.advance()
            return FloatLiteral(value)
        
        elif self.current_token.type == TokenType.STRING:
            value = self.current_token.value
            self.advance()
            return StringLiteral(value)
        
        elif self.current_token.type == TokenType.BOOLEAN:
            value = self.current_token.value == "true"
            self.advance()
            return BooleanLiteral(value)
        
        elif self.match(TokenType.IDENTIFIER, TokenType.VOID):
            name = self.current_token.value
            self.advance()
            return Identifier(name)
        
        elif self.current_token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        else:
            raise ParseError(f"Unexpected token in expression: {self.current_token.type.value}", 
                           self.current_token)
    
    def parse_postfix_expression(self) -> Expression:
        """Parse postfix expressions (function calls, field access, error propagation)"""
        expr = self.parse_primary_expression()
        
        while True:
            if self.current_token.type == TokenType.LPAREN:
                # Function call
                self.advance()
                arguments = []
                
                while not self.match(TokenType.RPAREN):
                    arguments.append(self.parse_expression())
                    if self.current_token.type == TokenType.COMMA:
                        self.advance()
                
                self.expect(TokenType.RPAREN)
                expr = FunctionCall(expr, arguments)
            
            elif self.current_token.type == TokenType.DOT:
                # Field access
                self.advance()
                field_name = self.expect(TokenType.IDENTIFIER).value
                expr = FieldAccess(expr, field_name)
            
            elif self.current_token.type == TokenType.QUESTION:
                # Error propagation operator
                self.advance()
                expr = UnaryOperation("?", expr)
            
            else:
                break
        
        return expr
    
    def parse_unary_expression(self) -> Expression:
        """Parse unary expressions"""
        if self.match(TokenType.NOT, TokenType.MINUS):
            operator = self.current_token.value
            self.advance()
            operand = self.parse_unary_expression()
            return UnaryOperation(operator, operand)
        
        return self.parse_postfix_expression()
    
    def parse_binary_expression(self, min_precedence: int = 0) -> Expression:
        """Parse binary expressions with operator precedence"""
        left = self.parse_unary_expression()
        
        while True:
            if not self.match(TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, 
                             TokenType.DIVIDE, TokenType.MODULO, TokenType.EQUAL,
                             TokenType.NOT_EQUAL, TokenType.LESS_THAN, TokenType.GREATER_THAN,
                             TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL, TokenType.AND, TokenType.OR):
                break
            
            operator = self.current_token.value
            precedence = self.get_operator_precedence(self.current_token.type)
            
            if precedence < min_precedence:
                break
            
            self.advance()
            right = self.parse_binary_expression(precedence + 1)
            left = BinaryOperation(left, operator, right)
        
        return left
    
    def get_operator_precedence(self, token_type: TokenType) -> int:
        """Get operator precedence for binary expressions"""
        precedence_map = {
            TokenType.OR: 1,
            TokenType.AND: 2,
            TokenType.EQUAL: 3,
            TokenType.NOT_EQUAL: 3,
            TokenType.LESS_THAN: 4,
            TokenType.GREATER_THAN: 4,
            TokenType.LESS_EQUAL: 4,
            TokenType.GREATER_EQUAL: 4,
            TokenType.PLUS: 5,
            TokenType.MINUS: 5,
            TokenType.MULTIPLY: 6,
            TokenType.DIVIDE: 6,
            TokenType.MODULO: 6,
        }
        return precedence_map.get(token_type, 0)
    
    def parse_expression(self) -> Expression:
        """Parse expressions"""
        return self.parse_binary_expression()
    
    def parse_variable_declaration(self) -> VariableDeclaration:
        """Parse variable declarations (let/const)"""
        is_const = self.current_token.type == TokenType.CONST
        self.advance()  # Skip 'let' or 'const'
        
        is_mutable = False
        if self.current_token.type == TokenType.MUT:
            is_mutable = True
            self.advance()
        
        name = self.expect(TokenType.IDENTIFIER).value
        
        type_annotation = None
        if self.current_token.type == TokenType.COLON:
            self.advance()
            type_annotation = self.parse_type()
        
        value = None
        if self.current_token.type == TokenType.ASSIGN:
            self.advance()
            value = self.parse_expression()
        
        return VariableDeclaration(name, type_annotation, value, is_mutable and not is_const)
    
    def parse_return_statement(self) -> ReturnStatement:
        """Parse return statements"""
        self.expect(TokenType.RETURN)
        
        value = None
        if not self.match(TokenType.NEWLINE, TokenType.RBRACE, TokenType.EOF):
            value = self.parse_expression()
        
        return ReturnStatement(value)
    
    def parse_if_statement(self) -> IfStatement:
        """Parse if statements"""
        self.expect(TokenType.IF)
        condition = self.parse_expression()
        self.expect(TokenType.LBRACE)
        self.skip_newlines()
        
        then_block = []
        while not self.match(TokenType.RBRACE):
            then_block.append(self.parse_statement())
            self.skip_newlines()
        
        self.expect(TokenType.RBRACE)
        
        else_block = None
        if self.current_token.type == TokenType.ELSE:
            self.advance()
            self.expect(TokenType.LBRACE)
            self.skip_newlines()
            
            else_block = []
            while not self.match(TokenType.RBRACE):
                else_block.append(self.parse_statement())
                self.skip_newlines()
            
            self.expect(TokenType.RBRACE)
        
        return IfStatement(condition, then_block, else_block)
    
    def parse_while_statement(self) -> WhileStatement:
        """Parse while statements"""
        self.expect(TokenType.WHILE)
        condition = self.parse_expression()
        self.expect(TokenType.LBRACE)
        self.skip_newlines()
        
        body = []
        while not self.match(TokenType.RBRACE):
            body.append(self.parse_statement())
            self.skip_newlines()
        
        self.expect(TokenType.RBRACE)
        return WhileStatement(condition, body)
    
    def parse_function_declaration(self) -> FunctionDeclaration:
        """Parse function declarations"""
        self.expect(TokenType.FN)
        name = self.expect(TokenType.IDENTIFIER).value
        
        self.expect(TokenType.LPAREN)
        parameters = []
        
        while not self.match(TokenType.RPAREN):
            param_name = self.expect(TokenType.IDENTIFIER).value
            self.expect(TokenType.COLON)
            param_type = self.parse_type()
            parameters.append(Parameter(param_name, param_type))
            
            if self.current_token.type == TokenType.COMMA:
                self.advance()
        
        self.expect(TokenType.RPAREN)
        
        return_type = None
        if self.current_token.type == TokenType.ARROW:
            self.advance()
            return_type = self.parse_type()
        
        self.expect(TokenType.LBRACE)
        self.skip_newlines()
        
        body = []
        while not self.match(TokenType.RBRACE):
            body.append(self.parse_statement())
            self.skip_newlines()
        
        self.expect(TokenType.RBRACE)
        return FunctionDeclaration(name, parameters, return_type, body)
    
    def parse_statement(self) -> Statement:
        """Parse statements"""
        if self.match(TokenType.LET, TokenType.CONST):
            return self.parse_variable_declaration()
        elif self.current_token.type == TokenType.RETURN:
            return self.parse_return_statement()
        elif self.current_token.type == TokenType.IF:
            return self.parse_if_statement()
        elif self.current_token.type == TokenType.WHILE:
            return self.parse_while_statement()
        elif self.current_token.type == TokenType.FN:
            return self.parse_function_declaration()
        else:
            # Expression statement or assignment
            expr = self.parse_expression()
            
            if self.current_token.type == TokenType.ASSIGN:
                self.advance()
                value = self.parse_expression()
                return Assignment(expr, value)
            else:
                return ExpressionStatement(expr)
    
    def parse_import_statement(self) -> ImportStatement:
        """Parse import statements"""
        self.expect(TokenType.IMPORT)
        
        module_path = ""
        module_path += self.expect(TokenType.IDENTIFIER).value
        
        while self.current_token.type == TokenType.DOT:
            self.advance()
            module_path += "." + self.expect(TokenType.IDENTIFIER).value
        
        return ImportStatement(module_path)
    
    def parse_module_declaration(self) -> ModuleDeclaration:
        """Parse module declarations"""
        self.expect(TokenType.MODULE)
        name = self.expect(TokenType.IDENTIFIER).value
        return ModuleDeclaration(name)
    
    def parse_program(self) -> Program:
        """Parse the entire program"""
        self.skip_newlines()
        
        module = None
        if self.current_token.type == TokenType.MODULE:
            module = self.parse_module_declaration()
            self.skip_newlines()
        
        imports = []
        while self.current_token.type == TokenType.IMPORT:
            imports.append(self.parse_import_statement())
            self.skip_newlines()
        
        declarations = []
        while not self.match(TokenType.EOF):
            if self.current_token.type == TokenType.COMMENT:
                self.advance()
                continue
            declarations.append(self.parse_statement())
            self.skip_newlines()
        
        return Program(module, imports, declarations)

def print_ast(node: ASTNode, indent: int = 0) -> str:
    """Pretty print AST for debugging"""
    prefix = "  " * indent
    
    if isinstance(node, Program):
        result = f"{prefix}Program:\n"
        if node.module:
            result += print_ast(node.module, indent + 1)
        for imp in node.imports:
            result += print_ast(imp, indent + 1)
        for decl in node.declarations:
            result += print_ast(decl, indent + 1)
        return result
    
    elif isinstance(node, ModuleDeclaration):
        return f"{prefix}Module: {node.name}\n"
    
    elif isinstance(node, ImportStatement):
        return f"{prefix}Import: {node.module_path}\n"
    
    elif isinstance(node, FunctionDeclaration):
        result = f"{prefix}Function: {node.name}\n"
        result += f"{prefix}  Parameters:\n"
        for param in node.parameters:
            result += f"{prefix}    {param.name}: {param.type_annotation}\n"
        if node.return_type:
            result += f"{prefix}  Returns: {node.return_type}\n"
        result += f"{prefix}  Body:\n"
        for stmt in node.body:
            result += print_ast(stmt, indent + 2)
        return result
    
    elif isinstance(node, VariableDeclaration):
        mut_str = "mut " if node.is_mutable else ""
        type_str = f": {node.type_annotation}" if node.type_annotation else ""
        value_str = f" = {node.value}" if node.value else ""
        return f"{prefix}VarDecl: {mut_str}{node.name}{type_str}{value_str}\n"
    
    elif isinstance(node, ReturnStatement):
        value_str = f" {node.value}" if node.value else ""
        return f"{prefix}Return:{value_str}\n"
    
    elif isinstance(node, ExpressionStatement):
        return f"{prefix}ExprStmt: {node.expression}\n"
    
    else:
        return f"{prefix}{type(node).__name__}: {node}\n"

if __name__ == "__main__":
    # Test the parser
    test_code = '''
    module main
    
    import std.io
    
    fn main() -> Result<void, Error> {
        let x: i32 = 42
        let name: string = "AIGo"
        io.println("Hello, World!")?
        return Ok(void)
    }
    '''
    
    lexer = Lexer(test_code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse_program()
    
    print("Abstract Syntax Tree:")
    print(print_ast(ast))

