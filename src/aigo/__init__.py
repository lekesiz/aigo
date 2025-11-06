"""
AIGo Programming Language

A modern, AI-native programming language designed for high-performance computing,
edge computing, and artificial intelligence applications.
"""

__version__ = "1.0.0-beta"
__author__ = "AIGo Development Team"
__license__ = "MIT"

from .lexer import Lexer, Token, TokenType
from .parser import Parser, Program
from .interpreter import Interpreter, run_aigo_code

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__license__",

    # Lexer
    "Lexer",
    "Token",
    "TokenType",

    # Parser
    "Parser",
    "Program",

    # Interpreter
    "Interpreter",
    "run_aigo_code",
]
