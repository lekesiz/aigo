"""
AIGo Standard Library - JSON Module

JSON parsing and serialization for AIGo programs.

This module provides JSON operations including:
- JSON parsing (string to object)
- JSON serialization (object to string)
- Pretty printing
- Schema validation (basic)

Usage in AIGo:
    import std.json

    let data: string = json.stringify(obj)
    let obj = json.parse(json_string)
"""

import json as py_json
from typing import Any, Dict, List, Union, Optional


JSONValue = Union[Dict[str, Any], List[Any], str, int, float, bool, None]


class JSONModule:
    """AIGo JSON standard library module."""

    @staticmethod
    def parse(json_string: str) -> JSONValue:
        """
        Parse JSON string to object.

        Args:
            json_string: JSON string to parse

        Returns:
            Parsed object (dict, list, or primitive)

        Raises:
            ValueError: If JSON is invalid
        """
        try:
            return py_json.loads(json_string)
        except py_json.JSONDecodeError as e:
            raise ValueError(f"json.parse: invalid JSON - {e}")

    @staticmethod
    def stringify(obj: JSONValue, indent: Optional[int] = None) -> str:
        """
        Convert object to JSON string.

        Args:
            obj: Object to serialize
            indent: Indentation spaces for pretty print (default: None)

        Returns:
            JSON string

        Raises:
            ValueError: If object is not JSON serializable
        """
        try:
            return py_json.dumps(obj, indent=indent)
        except (TypeError, ValueError) as e:
            raise ValueError(f"json.stringify: not serializable - {e}")

    @staticmethod
    def pretty(obj: JSONValue, indent: int = 2) -> str:
        """
        Convert object to pretty-printed JSON string.

        Args:
            obj: Object to serialize
            indent: Indentation spaces (default: 2)

        Returns:
            Pretty-printed JSON string
        """
        return JSONModule.stringify(obj, indent=indent)

    @staticmethod
    def parse_file(filepath: str) -> JSONValue:
        """
        Parse JSON from file.

        Args:
            filepath: Path to JSON file

        Returns:
            Parsed object

        Raises:
            ValueError: If file not found or invalid JSON
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return py_json.load(f)
        except FileNotFoundError:
            raise ValueError(f"json.parse_file: file not found - {filepath}")
        except py_json.JSONDecodeError as e:
            raise ValueError(f"json.parse_file: invalid JSON in {filepath} - {e}")

    @staticmethod
    def stringify_file(obj: JSONValue, filepath: str, indent: Optional[int] = 2) -> None:
        """
        Write object to JSON file.

        Args:
            obj: Object to serialize
            filepath: Output file path
            indent: Indentation spaces (default: 2)

        Raises:
            ValueError: If object not serializable or file error
        """
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                py_json.dump(obj, f, indent=indent)
        except (TypeError, ValueError) as e:
            raise ValueError(f"json.stringify_file: not serializable - {e}")
        except IOError as e:
            raise ValueError(f"json.stringify_file: file error - {e}")

    @staticmethod
    def validate(json_string: str) -> bool:
        """
        Check if string is valid JSON.

        Args:
            json_string: String to validate

        Returns:
            True if valid JSON, False otherwise
        """
        try:
            py_json.loads(json_string)
            return True
        except (py_json.JSONDecodeError, TypeError):
            return False

    @staticmethod
    def merge(obj1: Dict[str, Any], obj2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge two JSON objects (shallow merge).

        Args:
            obj1: First object
            obj2: Second object (takes precedence)

        Returns:
            Merged object
        """
        result = obj1.copy()
        result.update(obj2)
        return result

    @staticmethod
    def deep_merge(obj1: Dict[str, Any], obj2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deep merge two JSON objects.

        Args:
            obj1: First object
            obj2: Second object (takes precedence)

        Returns:
            Deep merged object
        """
        result = obj1.copy()

        for key, value in obj2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = JSONModule.deep_merge(result[key], value)
            else:
                result[key] = value

        return result

    @staticmethod
    def get(obj: Dict[str, Any], path: str, default: Any = None) -> Any:
        """
        Get value from nested object using dot notation.

        Args:
            obj: Object to query
            path: Dot-separated path (e.g., "user.name")
            default: Default value if not found

        Returns:
            Value at path or default

        Example:
            get({"user": {"name": "Alice"}}, "user.name") -> "Alice"
        """
        keys = path.split(".")
        current = obj

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default

        return current

    @staticmethod
    def set(obj: Dict[str, Any], path: str, value: Any) -> Dict[str, Any]:
        """
        Set value in nested object using dot notation.

        Args:
            obj: Object to modify
            path: Dot-separated path (e.g., "user.name")
            value: Value to set

        Returns:
            Modified object

        Example:
            set({}, "user.name", "Alice") -> {"user": {"name": "Alice"}}
        """
        keys = path.split(".")
        current = obj

        for i, key in enumerate(keys[:-1]):
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]

        current[keys[-1]] = value
        return obj

    @staticmethod
    def has(obj: Dict[str, Any], path: str) -> bool:
        """
        Check if path exists in nested object.

        Args:
            obj: Object to query
            path: Dot-separated path

        Returns:
            True if path exists, False otherwise
        """
        keys = path.split(".")
        current = obj

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return False

        return True

    @staticmethod
    def delete(obj: Dict[str, Any], path: str) -> Dict[str, Any]:
        """
        Delete value from nested object using dot notation.

        Args:
            obj: Object to modify
            path: Dot-separated path

        Returns:
            Modified object
        """
        keys = path.split(".")
        current = obj

        for key in keys[:-1]:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return obj

        if isinstance(current, dict) and keys[-1] in current:
            del current[keys[-1]]

        return obj

    @staticmethod
    def flatten(obj: Dict[str, Any], separator: str = ".") -> Dict[str, Any]:
        """
        Flatten nested object to single level.

        Args:
            obj: Object to flatten
            separator: Key separator (default: ".")

        Returns:
            Flattened object

        Example:
            flatten({"a": {"b": 1}}) -> {"a.b": 1}
        """
        result = {}

        def _flatten(current: Any, prefix: str = ""):
            if isinstance(current, dict):
                for key, value in current.items():
                    new_key = f"{prefix}{separator}{key}" if prefix else key
                    _flatten(value, new_key)
            else:
                result[prefix] = current

        _flatten(obj)
        return result

    @staticmethod
    def unflatten(obj: Dict[str, Any], separator: str = ".") -> Dict[str, Any]:
        """
        Unflatten single-level object to nested structure.

        Args:
            obj: Flattened object
            separator: Key separator (default: ".")

        Returns:
            Nested object

        Example:
            unflatten({"a.b": 1}) -> {"a": {"b": 1}}
        """
        result: Dict[str, Any] = {}

        for key, value in obj.items():
            JSONModule.set(result, key.replace(separator, "."), value)

        return result

    @staticmethod
    def filter_keys(obj: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
        """
        Filter object to only include specified keys.

        Args:
            obj: Object to filter
            keys: Keys to include

        Returns:
            Filtered object
        """
        return {k: v for k, v in obj.items() if k in keys}

    @staticmethod
    def exclude_keys(obj: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
        """
        Filter object to exclude specified keys.

        Args:
            obj: Object to filter
            keys: Keys to exclude

        Returns:
            Filtered object
        """
        return {k: v for k, v in obj.items() if k not in keys}

    @staticmethod
    def map_values(obj: Dict[str, Any], func: callable) -> Dict[str, Any]:
        """
        Map function over object values.

        Args:
            obj: Object to map
            func: Function to apply to each value

        Returns:
            Object with mapped values
        """
        return {k: func(v) for k, v in obj.items()}

    @staticmethod
    def map_keys(obj: Dict[str, Any], func: callable) -> Dict[str, Any]:
        """
        Map function over object keys.

        Args:
            obj: Object to map
            func: Function to apply to each key

        Returns:
            Object with mapped keys
        """
        return {func(k): v for k, v in obj.items()}


# Create module instance
json_module = JSONModule()

__all__ = ["JSONModule", "json_module", "JSONValue"]
