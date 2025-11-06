"""
AIGo Standard Library

This package contains the standard library modules for the AIGo programming language.

Available Modules:
    - math: Mathematical functions and constants (50+ functions)
    - string: String manipulation utilities (40+ functions)
    - collections: Collection data structures (40+ functions)
    - json: JSON parsing and serialization (20+ functions)
    - time: Time and date utilities (40+ functions)
    - fs: File system operations (40+ functions)
    - io: Input/output operations (Coming Soon)
    - http: HTTP client (Coming Soon)

Usage:
    from aigo.stdlib import math, string, collections, json, time, fs
    from aigo.stdlib.math import math_module
    from aigo.stdlib.string import string_module
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


# Auto-register available modules
try:
    from .math import math_module
    register_module("math", math_module)
except ImportError:
    pass

try:
    from .string import string_module
    register_module("string", string_module)
except ImportError:
    pass

try:
    from .collections import collections_module
    register_module("collections", collections_module)
except ImportError:
    pass

try:
    from .json import json_module
    register_module("json", json_module)
except ImportError:
    pass

try:
    from .time import time_module
    register_module("time", time_module)
except ImportError:
    pass

try:
    from .fs import fs_module
    register_module("fs", fs_module)
except ImportError:
    pass


__all__ = [
    "__version__",
    "register_module",
    "get_module",
    "list_modules",
]
