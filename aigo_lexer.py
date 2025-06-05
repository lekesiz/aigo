#!/usr/bin/env python3
"""
AIGo Language Interpreter Prototype
A simple interpreter for the AIGo programming language
"""

import re
import enum
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass

class TokenType(enum.Enum):
    # Literals
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    
    # Identifiers and Keywords
    IDENTIFIER = "IDENTIFIER"
    MODULE = "MODULE"
    IMPORT = "IMPORT"
    FN = "FN"
    LET = "LET"
    MUT = "MUT"
    CONST = "CONST"
    STRUCT = "STRUCT"
    ENUM = "ENUM"
    MATCH = "MATCH"
    IF = "IF"
    ELSE = "ELSE"
    FOR = "FOR"
    WHILE = "WHILE"
    RETURN = "RETURN"
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"
    
    # Types
    I32 = "I32"
    I64 = "I64"
    F32 = "F32"
    F64 = "F64"
    BOOL = "BOOL"
    STRING_TYPE = "STRING_TYPE"
    VOID = "VOID"
    
    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    MODULO = "MODULO"
    ASSIGN = "ASSIGN"
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN = "GREATER_THAN"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER_EQUAL = "GREATER_EQUAL"
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    
    # Delimiters
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    DOT = "DOT"
    COLON = "COLON"
    ARROW = "ARROW"
    QUESTION = "QUESTION"
    
    # Brackets
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    
    # Special
    NEWLINE = "NEWLINE"
    EOF = "EOF"
    COMMENT = "COMMENT"

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        
        # Keywords mapping
        self.keywords = {
            'module': TokenType.MODULE,
            'import': TokenType.IMPORT,
            'fn': TokenType.FN,
            'let': TokenType.LET,
            'mut': TokenType.MUT,
            'const': TokenType.CONST,
            'struct': TokenType.STRUCT,
            'enum': TokenType.ENUM,
            'match': TokenType.MATCH,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'for': TokenType.FOR,
            'while': TokenType.WHILE,
            'return': TokenType.RETURN,
            'break': TokenType.BREAK,
            'continue': TokenType.CONTINUE,
            'i32': TokenType.I32,
            'i64': TokenType.I64,
            'f32': TokenType.F32,
            'f64': TokenType.F64,
            'bool': TokenType.BOOL,
            'string': TokenType.STRING_TYPE,
            'void': TokenType.VOID,
            'true': TokenType.BOOLEAN,
            'false': TokenType.BOOLEAN,
        }
    
    def current_char(self) -> Optional[str]:
        if self.position >= len(self.source):
            return None
        return self.source[self.position]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        peek_pos = self.position + offset
        if peek_pos >= len(self.source):
            return None
        return self.source[peek_pos]
    
    def advance(self):
        if self.position < len(self.source) and self.source[self.position] == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.position += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def read_number(self) -> Token:
        start_line, start_column = self.line, self.column
        number_str = ""
        is_float = False
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if is_float:  # Second dot found
                    break
                is_float = True
            number_str += self.current_char()
            self.advance()
        
        token_type = TokenType.FLOAT if is_float else TokenType.INTEGER
        return Token(token_type, number_str, start_line, start_column)
    
    def read_string(self) -> Token:
        start_line, start_column = self.line, self.column
        quote_char = self.current_char()
        self.advance()  # Skip opening quote
        
        string_value = ""
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\':
                self.advance()
                if self.current_char() == 'n':
                    string_value += '\n'
                elif self.current_char() == 't':
                    string_value += '\t'
                elif self.current_char() == 'r':
                    string_value += '\r'
                elif self.current_char() == '\\':
                    string_value += '\\'
                elif self.current_char() == quote_char:
                    string_value += quote_char
                else:
                    string_value += self.current_char()
            else:
                string_value += self.current_char()
            self.advance()
        
        if self.current_char() == quote_char:
            self.advance()  # Skip closing quote
        
        return Token(TokenType.STRING, string_value, start_line, start_column)
    
    def read_identifier(self) -> Token:
        start_line, start_column = self.line, self.column
        identifier = ""
        
        while (self.current_char() and 
               (self.current_char().isalnum() or self.current_char() == '_')):
            identifier += self.current_char()
            self.advance()
        
        token_type = self.keywords.get(identifier, TokenType.IDENTIFIER)
        return Token(token_type, identifier, start_line, start_column)
    
    def read_comment(self) -> Token:
        start_line, start_column = self.line, self.column
        comment = ""
        
        # Skip //
        self.advance()
        self.advance()
        
        while self.current_char() and self.current_char() != '\n':
            comment += self.current_char()
            self.advance()
        
        return Token(TokenType.COMMENT, comment, start_line, start_column)
    
    def tokenize(self) -> List[Token]:
        while self.position < len(self.source):
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            char = self.current_char()
            line, column = self.line, self.column
            
            # Numbers
            if char.isdigit():
                self.tokens.append(self.read_number())
            
            # Strings
            elif char in '"\'':
                self.tokens.append(self.read_string())
            
            # Identifiers and keywords
            elif char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
            
            # Comments
            elif char == '/' and self.peek_char() == '/':
                self.tokens.append(self.read_comment())
            
            # Two-character operators
            elif char == '=' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.EQUAL, "==", line, column))
                self.advance()
                self.advance()
            elif char == '!' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.NOT_EQUAL, "!=", line, column))
                self.advance()
                self.advance()
            elif char == '<' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.LESS_EQUAL, "<=", line, column))
                self.advance()
                self.advance()
            elif char == '>' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.GREATER_EQUAL, ">=", line, column))
                self.advance()
                self.advance()
            elif char == '-' and self.peek_char() == '>':
                self.tokens.append(Token(TokenType.ARROW, "->", line, column))
                self.advance()
                self.advance()
            elif char == '&' and self.peek_char() == '&':
                self.tokens.append(Token(TokenType.AND, "&&", line, column))
                self.advance()
                self.advance()
            elif char == '|' and self.peek_char() == '|':
                self.tokens.append(Token(TokenType.OR, "||", line, column))
                self.advance()
                self.advance()
            
            # Single-character operators and delimiters
            elif char == '+':
                self.tokens.append(Token(TokenType.PLUS, char, line, column))
                self.advance()
            elif char == '-':
                self.tokens.append(Token(TokenType.MINUS, char, line, column))
                self.advance()
            elif char == '*':
                self.tokens.append(Token(TokenType.MULTIPLY, char, line, column))
                self.advance()
            elif char == '/':
                self.tokens.append(Token(TokenType.DIVIDE, char, line, column))
                self.advance()
            elif char == '%':
                self.tokens.append(Token(TokenType.MODULO, char, line, column))
                self.advance()
            elif char == '=':
                self.tokens.append(Token(TokenType.ASSIGN, char, line, column))
                self.advance()
            elif char == '<':
                self.tokens.append(Token(TokenType.LESS_THAN, char, line, column))
                self.advance()
            elif char == '>':
                self.tokens.append(Token(TokenType.GREATER_THAN, char, line, column))
                self.advance()
            elif char == '!':
                self.tokens.append(Token(TokenType.NOT, char, line, column))
                self.advance()
            elif char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, char, line, column))
                self.advance()
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, char, line, column))
                self.advance()
            elif char == '.':
                self.tokens.append(Token(TokenType.DOT, char, line, column))
                self.advance()
            elif char == ':':
                self.tokens.append(Token(TokenType.COLON, char, line, column))
                self.advance()
            elif char == '?':
                self.tokens.append(Token(TokenType.QUESTION, char, line, column))
                self.advance()
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, char, line, column))
                self.advance()
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, char, line, column))
                self.advance()
            elif char == '{':
                self.tokens.append(Token(TokenType.LBRACE, char, line, column))
                self.advance()
            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, char, line, column))
                self.advance()
            elif char == '[':
                self.tokens.append(Token(TokenType.LBRACKET, char, line, column))
                self.advance()
            elif char == ']':
                self.tokens.append(Token(TokenType.RBRACKET, char, line, column))
                self.advance()
            elif char == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, char, line, column))
                self.advance()
            else:
                # Unknown character, skip it
                self.advance()
        
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens

if __name__ == "__main__":
    # Test the lexer
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
    
    print("Tokens:")
    for token in tokens:
        if token.type != TokenType.NEWLINE and token.type != TokenType.COMMENT:
            print(f"{token.type.value:15} | {token.value:20} | Line {token.line}, Col {token.column}")

