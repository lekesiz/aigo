"""
AIGo Type System

Type checking and type inference system for AIGo.

Features:
- Static type checking
- Type inference
- Generic types (future)
- Type constraints
- Error reporting

Usage:
    from aigo.type_system import TypeChecker, Type

    checker = TypeChecker()
    checker.check_program(program)
"""

from enum import Enum
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass


class TypeKind(Enum):
    """Type categories."""

    INT = "int"
    FLOAT = "float"
    STRING = "string"
    BOOL = "bool"
    VOID = "void"
    ARRAY = "array"
    FUNCTION = "function"
    STRUCT = "struct"
    ENUM = "enum"
    GENERIC = "generic"
    UNION = "union"
    OPTIONAL = "optional"
    RESULT = "result"
    UNKNOWN = "unknown"


@dataclass
class Type:
    """Type representation."""

    kind: TypeKind
    name: str
    parameters: List["Type"] = None  # For generics like array<i32>
    return_type: Optional["Type"] = None  # For functions
    arg_types: List["Type"] = None  # For functions
    fields: Dict[str, "Type"] = None  # For structs
    variants: List[str] = None  # For enums

    def __post_init__(self):
        """Initialize empty lists and dicts."""
        if self.parameters is None:
            self.parameters = []
        if self.arg_types is None:
            self.arg_types = []
        if self.fields is None:
            self.fields = {}
        if self.variants is None:
            self.variants = []

    def __str__(self) -> str:
        """String representation of type."""
        if self.kind == TypeKind.ARRAY:
            elem_type = self.parameters[0] if self.parameters else Type.unknown()
            return f"array<{elem_type}>"
        elif self.kind == TypeKind.FUNCTION:
            args = ", ".join(str(t) for t in self.arg_types)
            return f"fn({args}) -> {self.return_type}"
        elif self.kind == TypeKind.OPTIONAL:
            inner = self.parameters[0] if self.parameters else Type.unknown()
            return f"Option<{inner}>"
        elif self.kind == TypeKind.RESULT:
            ok = self.parameters[0] if len(self.parameters) > 0 else Type.unknown()
            err = self.parameters[1] if len(self.parameters) > 1 else Type.unknown()
            return f"Result<{ok}, {err}>"
        else:
            return self.name

    def __eq__(self, other) -> bool:
        """Type equality check."""
        if not isinstance(other, Type):
            return False

        if self.kind != other.kind:
            return False

        if self.kind in [TypeKind.INT, TypeKind.FLOAT, TypeKind.STRING, TypeKind.BOOL, TypeKind.VOID]:
            return True

        if self.kind == TypeKind.ARRAY:
            if not self.parameters or not other.parameters:
                return False
            return self.parameters[0] == other.parameters[0]

        if self.kind == TypeKind.FUNCTION:
            if self.return_type != other.return_type:
                return False
            if len(self.arg_types) != len(other.arg_types):
                return False
            return all(a == b for a, b in zip(self.arg_types, other.arg_types))

        return self.name == other.name

    @staticmethod
    def i32() -> "Type":
        """Create i32 type."""
        return Type(TypeKind.INT, "i32")

    @staticmethod
    def i64() -> "Type":
        """Create i64 type."""
        return Type(TypeKind.INT, "i64")

    @staticmethod
    def f32() -> "Type":
        """Create f32 type."""
        return Type(TypeKind.FLOAT, "f32")

    @staticmethod
    def f64() -> "Type":
        """Create f64 type."""
        return Type(TypeKind.FLOAT, "f64")

    @staticmethod
    def string() -> "Type":
        """Create string type."""
        return Type(TypeKind.STRING, "string")

    @staticmethod
    def bool() -> "Type":
        """Create bool type."""
        return Type(TypeKind.BOOL, "bool")

    @staticmethod
    def void() -> "Type":
        """Create void type."""
        return Type(TypeKind.VOID, "void")

    @staticmethod
    def array(element_type: "Type") -> "Type":
        """Create array type."""
        return Type(TypeKind.ARRAY, f"array<{element_type}>", parameters=[element_type])

    @staticmethod
    def function(arg_types: List["Type"], return_type: "Type") -> "Type":
        """Create function type."""
        return Type(
            TypeKind.FUNCTION,
            "function",
            arg_types=arg_types,
            return_type=return_type
        )

    @staticmethod
    def optional(inner_type: "Type") -> "Type":
        """Create optional type."""
        return Type(TypeKind.OPTIONAL, f"Option<{inner_type}>", parameters=[inner_type])

    @staticmethod
    def result(ok_type: "Type", err_type: "Type") -> "Type":
        """Create result type."""
        return Type(TypeKind.RESULT, f"Result<{ok_type}, {err_type}>", parameters=[ok_type, err_type])

    @staticmethod
    def unknown() -> "Type":
        """Create unknown type."""
        return Type(TypeKind.UNKNOWN, "unknown")


class TypeError(Exception):
    """Type error exception."""

    def __init__(self, message: str, location: Optional[tuple] = None):
        """
        Initialize type error.

        Args:
            message: Error message
            location: Optional (line, column) tuple
        """
        self.message = message
        self.location = location
        super().__init__(message)


class TypeEnvironment:
    """Type environment for variables and functions."""

    def __init__(self, parent: Optional["TypeEnvironment"] = None):
        """
        Initialize type environment.

        Args:
            parent: Parent environment for nested scopes
        """
        self.parent = parent
        self.types: Dict[str, Type] = {}

    def define(self, name: str, typ: Type) -> None:
        """
        Define a variable or function type.

        Args:
            name: Variable/function name
            typ: Type

        Raises:
            TypeError: If name already defined in this scope
        """
        if name in self.types:
            raise TypeError(f"'{name}' is already defined in this scope")
        self.types[name] = typ

    def lookup(self, name: str) -> Optional[Type]:
        """
        Look up a variable or function type.

        Args:
            name: Variable/function name

        Returns:
            Type if found, None otherwise
        """
        if name in self.types:
            return self.types[name]
        if self.parent:
            return self.parent.lookup(name)
        return None

    def set(self, name: str, typ: Type) -> None:
        """
        Set a variable type (for reassignment).

        Args:
            name: Variable name
            typ: New type

        Raises:
            TypeError: If variable not defined
        """
        if name in self.types:
            self.types[name] = typ
        elif self.parent:
            self.parent.set(name, typ)
        else:
            raise TypeError(f"Undefined variable '{name}'")


class TypeChecker:
    """Type checker for AIGo programs."""

    def __init__(self):
        """Initialize type checker."""
        self.env = TypeEnvironment()
        self.errors: List[TypeError] = []
        self._init_builtins()

    def _init_builtins(self):
        """Initialize built-in types and functions."""
        # Built-in types are already handled by Type class

        # Built-in functions (when we have them)
        # self.env.define("println", Type.function([Type.string()], Type.void()))
        pass

    def add_error(self, message: str, location: Optional[tuple] = None):
        """
        Add a type error.

        Args:
            message: Error message
            location: Optional (line, column) tuple
        """
        self.errors.append(TypeError(message, location))

    def check_compatible(self, expected: Type, actual: Type) -> bool:
        """
        Check if actual type is compatible with expected type.

        Args:
            expected: Expected type
            actual: Actual type

        Returns:
            True if compatible
        """
        # Direct equality
        if expected == actual:
            return True

        # Unknown type is compatible with everything (for gradual typing)
        if expected.kind == TypeKind.UNKNOWN or actual.kind == TypeKind.UNKNOWN:
            return True

        # Numeric type widening (i32 -> i64, i32 -> f64, etc.)
        if expected.kind == TypeKind.INT and actual.kind == TypeKind.INT:
            # Allow i32 -> i64
            if expected.name == "i64" and actual.name == "i32":
                return True

        if expected.kind == TypeKind.FLOAT and actual.kind in [TypeKind.INT, TypeKind.FLOAT]:
            # Allow int -> float
            return True

        return False

    def infer_type(self, expr: Any) -> Type:
        """
        Infer type of an expression.

        Args:
            expr: Expression to infer type for

        Returns:
            Inferred type
        """
        # This would be implemented based on the actual AST structure
        # For now, return unknown
        return Type.unknown()

    def check_program(self, program: Any) -> bool:
        """
        Type check a program.

        Args:
            program: Program to check

        Returns:
            True if type checking succeeded, False otherwise
        """
        self.errors = []

        # Type checking logic would go here
        # For now, just return True
        return len(self.errors) == 0

    def get_errors(self) -> List[TypeError]:
        """
        Get list of type errors.

        Returns:
            List of type errors
        """
        return self.errors

    def format_errors(self) -> str:
        """
        Format all type errors as a string.

        Returns:
            Formatted error messages
        """
        if not self.errors:
            return "No type errors"

        lines = []
        for error in self.errors:
            if error.location:
                line, col = error.location
                lines.append(f"Type error at line {line}, column {col}: {error.message}")
            else:
                lines.append(f"Type error: {error.message}")

        return "\n".join(lines)


# Utility functions

def parse_type(type_str: str) -> Type:
    """
    Parse type string to Type object.

    Args:
        type_str: Type string (e.g., "i32", "array<i32>", "Result<i32, string>")

    Returns:
        Type object

    Example:
        parse_type("i32") -> Type.i32()
        parse_type("array<i32>") -> Type.array(Type.i32())
    """
    type_str = type_str.strip()

    # Simple types
    type_map = {
        "i32": Type.i32(),
        "i64": Type.i64(),
        "f32": Type.f32(),
        "f64": Type.f64(),
        "string": Type.string(),
        "bool": Type.bool(),
        "void": Type.void(),
    }

    if type_str in type_map:
        return type_map[type_str]

    # Generic types (simplified parsing)
    if type_str.startswith("array<") and type_str.endswith(">"):
        inner = type_str[6:-1]
        return Type.array(parse_type(inner))

    if type_str.startswith("Option<") and type_str.endswith(">"):
        inner = type_str[7:-1]
        return Type.optional(parse_type(inner))

    if type_str.startswith("Result<") and type_str.endswith(">"):
        # Simplified: just extract the two types
        inner = type_str[7:-1]
        parts = inner.split(",", 1)
        if len(parts) == 2:
            ok_type = parse_type(parts[0].strip())
            err_type = parse_type(parts[1].strip())
            return Type.result(ok_type, err_type)

    # Unknown type
    return Type.unknown()


__all__ = [
    "Type",
    "TypeKind",
    "TypeError",
    "TypeEnvironment",
    "TypeChecker",
    "parse_type",
]
