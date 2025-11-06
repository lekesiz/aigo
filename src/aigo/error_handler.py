"""
AIGo Enhanced Error Handler

Provides helpful, Rust-like error messages with:
- Clear error descriptions
- Source code context with line numbers
- Helpful suggestions and hints
- Color-coded output for better readability

Features:
- Syntax error highlighting
- Type error suggestions
- Common mistake detection
- Context-aware hints
"""

from typing import Optional, List, Tuple
from dataclasses import dataclass


# ANSI color codes
class ErrorColors:
    """ANSI color codes for error messages."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    DIM = "\033[2m"


@dataclass
class SourceLocation:
    """Location in source code."""

    line: int
    column: int
    length: int = 1


@dataclass
class ErrorContext:
    """Context information for an error."""

    message: str
    location: SourceLocation
    source_lines: List[str]
    error_type: str
    suggestions: List[str]
    file_path: Optional[str] = None


class EnhancedErrorHandler:
    """Enhanced error handler with helpful messages."""

    def __init__(self, use_colors: bool = True):
        """
        Initialize error handler.

        Args:
            use_colors: Enable colored output (default: True)
        """
        self.use_colors = use_colors

    def _colorize(self, text: str, color: str) -> str:
        """
        Colorize text if colors enabled.

        Args:
            text: Text to colorize
            color: Color code

        Returns:
            Colorized text
        """
        if not self.use_colors:
            return text
        return f"{color}{text}{ErrorColors.RESET}"

    def format_error(self, context: ErrorContext) -> str:
        """
        Format error message with context.

        Args:
            context: Error context information

        Returns:
            Formatted error message
        """
        lines = []

        # Error header
        error_label = self._colorize("error", ErrorColors.BOLD + ErrorColors.RED)
        lines.append(f"{error_label}: {context.message}")

        # File location
        if context.file_path:
            location_info = f"{context.file_path}:{context.location.line}:{context.location.column}"
        else:
            location_info = f"line {context.location.line}, column {context.location.column}"

        location_label = self._colorize("-->", ErrorColors.BLUE)
        lines.append(f" {location_label} {location_info}")
        lines.append("")

        # Source code context
        line_num = context.location.line
        line_col = context.location.column
        length = context.location.length

        # Show 2 lines before and after if available
        start_line = max(1, line_num - 2)
        end_line = min(len(context.source_lines), line_num + 2)

        # Calculate max line number width for alignment
        max_line_width = len(str(end_line))

        for i in range(start_line - 1, end_line):
            current_line_num = i + 1
            source_line = context.source_lines[i] if i < len(context.source_lines) else ""

            # Line number
            line_num_str = str(current_line_num).rjust(max_line_width)

            if current_line_num == line_num:
                # Error line - highlight it
                line_num_colored = self._colorize(line_num_str, ErrorColors.BLUE + ErrorColors.BOLD)
                separator = self._colorize("|", ErrorColors.BLUE + ErrorColors.BOLD)
                lines.append(f" {line_num_colored} {separator} {source_line}")

                # Error indicator (^^^)
                spaces = " " * (line_col - 1)
                indicators = self._colorize("^" * max(1, length), ErrorColors.RED + ErrorColors.BOLD)
                empty_line_num = " " * max_line_width
                lines.append(f" {empty_line_num} {separator} {spaces}{indicators}")
            else:
                # Context line
                line_num_colored = self._colorize(line_num_str, ErrorColors.BLUE)
                separator = self._colorize("|", ErrorColors.BLUE)
                lines.append(f" {line_num_colored} {separator} {source_line}")

        lines.append("")

        # Suggestions
        if context.suggestions:
            help_label = self._colorize("help", ErrorColors.BOLD + ErrorColors.CYAN)
            lines.append(f"{help_label}: {context.suggestions[0]}")

            for suggestion in context.suggestions[1:]:
                lines.append(f"      {suggestion}")

            lines.append("")

        return "\n".join(lines)

    def suggest_for_syntax_error(self, error_msg: str) -> List[str]:
        """
        Generate suggestions for syntax errors.

        Args:
            error_msg: Error message

        Returns:
            List of suggestions
        """
        suggestions = []

        msg_lower = error_msg.lower()

        if "unexpected" in msg_lower and "token" in msg_lower:
            suggestions.append("Check for missing semicolons, braces, or parentheses")
            suggestions.append("Ensure all brackets are properly closed")

        if "expected" in msg_lower:
            if ";" in error_msg:
                suggestions.append("Add a semicolon at the end of the statement")
            elif "{" in error_msg or "}" in error_msg:
                suggestions.append("Check that all braces are balanced")
            elif ")" in error_msg or "(" in error_msg:
                suggestions.append("Ensure all parentheses are matched")

        if "identifier" in msg_lower:
            suggestions.append("Variable names must start with a letter or underscore")
            suggestions.append("Avoid using reserved keywords as variable names")

        if not suggestions:
            suggestions.append("Check the syntax near this location")

        return suggestions

    def suggest_for_type_error(self, error_msg: str) -> List[str]:
        """
        Generate suggestions for type errors.

        Args:
            error_msg: Error message

        Returns:
            List of suggestions
        """
        suggestions = []

        msg_lower = error_msg.lower()

        if "cannot assign" in msg_lower or "type mismatch" in msg_lower:
            suggestions.append("Ensure the value type matches the variable type")
            suggestions.append("Consider explicit type conversion if needed")

        if "undefined" in msg_lower or "not defined" in msg_lower:
            suggestions.append("Check that the variable is declared before use")
            suggestions.append("Verify the variable name spelling")

        if "expected" in msg_lower and "found" in msg_lower:
            suggestions.append("The types don't match - check your type annotations")

        if not suggestions:
            suggestions.append("Review the type declarations in this code")

        return suggestions

    def suggest_for_runtime_error(self, error_msg: str) -> List[str]:
        """
        Generate suggestions for runtime errors.

        Args:
            error_msg: Error message

        Returns:
            List of suggestions
        """
        suggestions = []

        msg_lower = error_msg.lower()

        if "division by zero" in msg_lower or "divide by zero" in msg_lower:
            suggestions.append("Add a check to ensure the divisor is not zero")
            suggestions.append("Example: if divisor != 0 { result = a / divisor }")

        if "index out of" in msg_lower or "out of bounds" in msg_lower:
            suggestions.append("Check that the index is within the array bounds")
            suggestions.append("Array indices start at 0 and end at length-1")

        if "null" in msg_lower or "none" in msg_lower:
            suggestions.append("Ensure the value is initialized before use")
            suggestions.append("Use option types to handle potentially missing values")

        if "overflow" in msg_lower:
            suggestions.append("The number is too large for this type")
            suggestions.append("Consider using a larger integer type (i64) or floating point")

        if not suggestions:
            suggestions.append("Check the values at runtime near this location")

        return suggestions

    def create_syntax_error(
        self,
        message: str,
        source: str,
        line: int,
        column: int,
        length: int = 1,
        file_path: Optional[str] = None,
    ) -> str:
        """
        Create a formatted syntax error message.

        Args:
            message: Error message
            source: Full source code
            line: Line number (1-indexed)
            column: Column number (1-indexed)
            length: Length of the error span
            file_path: Optional file path

        Returns:
            Formatted error message
        """
        source_lines = source.split("\n")
        location = SourceLocation(line, column, length)
        suggestions = self.suggest_for_syntax_error(message)

        context = ErrorContext(
            message=message,
            location=location,
            source_lines=source_lines,
            error_type="SyntaxError",
            suggestions=suggestions,
            file_path=file_path,
        )

        return self.format_error(context)

    def create_type_error(
        self,
        message: str,
        source: str,
        line: int,
        column: int,
        length: int = 1,
        file_path: Optional[str] = None,
    ) -> str:
        """
        Create a formatted type error message.

        Args:
            message: Error message
            source: Full source code
            line: Line number (1-indexed)
            column: Column number (1-indexed)
            length: Length of the error span
            file_path: Optional file path

        Returns:
            Formatted error message
        """
        source_lines = source.split("\n")
        location = SourceLocation(line, column, length)
        suggestions = self.suggest_for_type_error(message)

        context = ErrorContext(
            message=message,
            location=location,
            source_lines=source_lines,
            error_type="TypeError",
            suggestions=suggestions,
            file_path=file_path,
        )

        return self.format_error(context)

    def create_runtime_error(
        self,
        message: str,
        source: str,
        line: int,
        column: int,
        length: int = 1,
        file_path: Optional[str] = None,
    ) -> str:
        """
        Create a formatted runtime error message.

        Args:
            message: Error message
            source: Full source code
            line: Line number (1-indexed)
            column: Column number (1-indexed)
            length: Length of the error span
            file_path: Optional file path

        Returns:
            Formatted error message
        """
        source_lines = source.split("\n")
        location = SourceLocation(line, column, length)
        suggestions = self.suggest_for_runtime_error(message)

        context = ErrorContext(
            message=message,
            location=location,
            source_lines=source_lines,
            error_type="RuntimeError",
            suggestions=suggestions,
            file_path=file_path,
        )

        return self.format_error(context)


# Global error handler instance
_global_error_handler = EnhancedErrorHandler()


def format_syntax_error(
    message: str,
    source: str,
    line: int,
    column: int,
    length: int = 1,
    file_path: Optional[str] = None,
) -> str:
    """
    Format a syntax error with helpful context.

    Args:
        message: Error message
        source: Full source code
        line: Line number (1-indexed)
        column: Column number (1-indexed)
        length: Length of the error span
        file_path: Optional file path

    Returns:
        Formatted error message
    """
    return _global_error_handler.create_syntax_error(
        message, source, line, column, length, file_path
    )


def format_type_error(
    message: str,
    source: str,
    line: int,
    column: int,
    length: int = 1,
    file_path: Optional[str] = None,
) -> str:
    """
    Format a type error with helpful context.

    Args:
        message: Error message
        source: Full source code
        line: Line number (1-indexed)
        column: Column number (1-indexed)
        length: Length of the error span
        file_path: Optional file path

    Returns:
        Formatted error message
    """
    return _global_error_handler.create_type_error(
        message, source, line, column, length, file_path
    )


def format_runtime_error(
    message: str,
    source: str,
    line: int,
    column: int,
    length: int = 1,
    file_path: Optional[str] = None,
) -> str:
    """
    Format a runtime error with helpful context.

    Args:
        message: Error message
        source: Full source code
        line: Line number (1-indexed)
        column: Column number (1-indexed)
        length: Length of the error span
        file_path: Optional file path

    Returns:
        Formatted error message
    """
    return _global_error_handler.create_runtime_error(
        message, source, line, column, length, file_path
    )


__all__ = [
    "EnhancedErrorHandler",
    "ErrorContext",
    "SourceLocation",
    "format_syntax_error",
    "format_type_error",
    "format_runtime_error",
]
