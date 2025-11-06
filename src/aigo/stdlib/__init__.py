"""
AIGo Standard Library

This package contains the standard library modules for the AIGo programming language.

Available Modules:
    - math: Mathematical functions and constants
    - string: String manipulation utilities
    - collections: Collection data structures (list, map, set)
    - io: Input/output operations
    - fs: File system operations
    - json: JSON parsing and serialization
    - http: HTTP client
    - time: Time and date utilities

Usage:
    from aigo.stdlib import math, string, collections
"""

__version__ = "1.0.0-beta"
__author__ = "AIGo Development Team"

from typing import Dict, Any, Callable

# Registry of all standard library modules
_STDLIB_MODULES: Dict[str, Any] = {}


def register_module(name: str, module: Any) -> None:
    """
    Register a standard library module.

    Args:
        name: Module name
        module: Module object
    """
    _STDLIB_MODULES[name] = module


def get_module(name: str) -> Any:
    """
    Get a registered standard library module.

    Args:
        name: Module name

    Returns:
        Module object or None if not found
    """
    return _STDLIB_MODULES.get(name)


def list_modules() -> list[str]:
    """
    Get list of all registered modules.

    Returns:
        List of module names
    """
    return list(_STDLIB_MODULES.keys())


__all__ = [
    "__version__",
    "register_module",
    "get_module",
    "list_modules",
]
