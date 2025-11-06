"""
AIGo Standard Library - String Module

String manipulation utilities for AIGo programs.

This module provides string operations including:
- Case conversion
- Searching and replacing
- Trimming and padding
- Splitting and joining
- Character analysis

Usage in AIGo:
    import std.string

    let upper: string = string.to_upper("hello")
    let trimmed: string = string.trim("  spaces  ")
    let parts: array<string> = string.split("a,b,c", ",")
"""

from typing import List, Optional


class StringModule:
    """AIGo String standard library module."""

    # Case conversion
    @staticmethod
    def to_upper(s: str) -> str:
        """
        Convert string to uppercase.

        Args:
            s: Input string

        Returns:
            Uppercase string
        """
        return s.upper()

    @staticmethod
    def to_lower(s: str) -> str:
        """
        Convert string to lowercase.

        Args:
            s: Input string

        Returns:
            Lowercase string
        """
        return s.lower()

    @staticmethod
    def to_title(s: str) -> str:
        """
        Convert string to title case.

        Args:
            s: Input string

        Returns:
            Title case string
        """
        return s.title()

    @staticmethod
    def capitalize(s: str) -> str:
        """
        Capitalize the first character.

        Args:
            s: Input string

        Returns:
            Capitalized string
        """
        return s.capitalize()

    @staticmethod
    def swap_case(s: str) -> str:
        """
        Swap case of all characters.

        Args:
            s: Input string

        Returns:
            String with swapped case
        """
        return s.swapcase()

    # Trimming
    @staticmethod
    def trim(s: str) -> str:
        """
        Remove leading and trailing whitespace.

        Args:
            s: Input string

        Returns:
            Trimmed string
        """
        return s.strip()

    @staticmethod
    def trim_left(s: str) -> str:
        """
        Remove leading whitespace.

        Args:
            s: Input string

        Returns:
            Left-trimmed string
        """
        return s.lstrip()

    @staticmethod
    def trim_right(s: str) -> str:
        """
        Remove trailing whitespace.

        Args:
            s: Input string

        Returns:
            Right-trimmed string
        """
        return s.rstrip()

    @staticmethod
    def trim_chars(s: str, chars: str) -> str:
        """
        Remove specified characters from both ends.

        Args:
            s: Input string
            chars: Characters to remove

        Returns:
            Trimmed string
        """
        return s.strip(chars)

    # Searching
    @staticmethod
    def contains(s: str, substr: str) -> bool:
        """
        Check if string contains substring.

        Args:
            s: Input string
            substr: Substring to find

        Returns:
            True if substr is in s
        """
        return substr in s

    @staticmethod
    def starts_with(s: str, prefix: str) -> bool:
        """
        Check if string starts with prefix.

        Args:
            s: Input string
            prefix: Prefix to check

        Returns:
            True if s starts with prefix
        """
        return s.startswith(prefix)

    @staticmethod
    def ends_with(s: str, suffix: str) -> bool:
        """
        Check if string ends with suffix.

        Args:
            s: Input string
            suffix: Suffix to check

        Returns:
            True if s ends with suffix
        """
        return s.endswith(suffix)

    @staticmethod
    def find(s: str, substr: str, start: int = 0) -> int:
        """
        Find first occurrence of substring.

        Args:
            s: Input string
            substr: Substring to find
            start: Starting position (default: 0)

        Returns:
            Index of first occurrence, or -1 if not found
        """
        result = s.find(substr, start)
        return result

    @staticmethod
    def rfind(s: str, substr: str) -> int:
        """
        Find last occurrence of substring.

        Args:
            s: Input string
            substr: Substring to find

        Returns:
            Index of last occurrence, or -1 if not found
        """
        return s.rfind(substr)

    @staticmethod
    def count(s: str, substr: str) -> int:
        """
        Count occurrences of substring.

        Args:
            s: Input string
            substr: Substring to count

        Returns:
            Number of occurrences
        """
        return s.count(substr)

    # Replacing
    @staticmethod
    def replace(s: str, old: str, new: str, count: int = -1) -> str:
        """
        Replace occurrences of substring.

        Args:
            s: Input string
            old: Substring to replace
            new: Replacement string
            count: Maximum replacements (default: -1 for all)

        Returns:
            String with replacements
        """
        return s.replace(old, new, count)

    @staticmethod
    def replace_all(s: str, old: str, new: str) -> str:
        """
        Replace all occurrences of substring.

        Args:
            s: Input string
            old: Substring to replace
            new: Replacement string

        Returns:
            String with all replacements
        """
        return s.replace(old, new)

    # Splitting and joining
    @staticmethod
    def split(s: str, sep: Optional[str] = None, maxsplit: int = -1) -> List[str]:
        """
        Split string by separator.

        Args:
            s: Input string
            sep: Separator (default: whitespace)
            maxsplit: Maximum splits (default: -1 for all)

        Returns:
            List of substrings
        """
        return s.split(sep, maxsplit)

    @staticmethod
    def split_lines(s: str, keepends: bool = False) -> List[str]:
        """
        Split string into lines.

        Args:
            s: Input string
            keepends: Keep line endings (default: False)

        Returns:
            List of lines
        """
        return s.splitlines(keepends)

    @staticmethod
    def join(separator: str, parts: List[str]) -> str:
        """
        Join strings with separator.

        Args:
            separator: Separator string
            parts: List of strings to join

        Returns:
            Joined string
        """
        return separator.join(parts)

    # Padding
    @staticmethod
    def pad_left(s: str, width: int, fillchar: str = " ") -> str:
        """
        Pad string on the left.

        Args:
            s: Input string
            width: Target width
            fillchar: Fill character (default: space)

        Returns:
            Padded string
        """
        return s.rjust(width, fillchar)

    @staticmethod
    def pad_right(s: str, width: int, fillchar: str = " ") -> str:
        """
        Pad string on the right.

        Args:
            s: Input string
            width: Target width
            fillchar: Fill character (default: space)

        Returns:
            Padded string
        """
        return s.ljust(width, fillchar)

    @staticmethod
    def pad_center(s: str, width: int, fillchar: str = " ") -> str:
        """
        Center string with padding.

        Args:
            s: Input string
            width: Target width
            fillchar: Fill character (default: space)

        Returns:
            Centered string
        """
        return s.center(width, fillchar)

    @staticmethod
    def zero_pad(s: str, width: int) -> str:
        """
        Pad string with zeros on the left.

        Args:
            s: Input string
            width: Target width

        Returns:
            Zero-padded string
        """
        return s.zfill(width)

    # Character analysis
    @staticmethod
    def is_alpha(s: str) -> bool:
        """
        Check if all characters are alphabetic.

        Args:
            s: Input string

        Returns:
            True if all characters are alphabetic
        """
        return s.isalpha()

    @staticmethod
    def is_digit(s: str) -> bool:
        """
        Check if all characters are digits.

        Args:
            s: Input string

        Returns:
            True if all characters are digits
        """
        return s.isdigit()

    @staticmethod
    def is_alnum(s: str) -> bool:
        """
        Check if all characters are alphanumeric.

        Args:
            s: Input string

        Returns:
            True if all characters are alphanumeric
        """
        return s.isalnum()

    @staticmethod
    def is_lower(s: str) -> bool:
        """
        Check if all cased characters are lowercase.

        Args:
            s: Input string

        Returns:
            True if all cased characters are lowercase
        """
        return s.islower()

    @staticmethod
    def is_upper(s: str) -> bool:
        """
        Check if all cased characters are uppercase.

        Args:
            s: Input string

        Returns:
            True if all cased characters are uppercase
        """
        return s.isupper()

    @staticmethod
    def is_space(s: str) -> bool:
        """
        Check if all characters are whitespace.

        Args:
            s: Input string

        Returns:
            True if all characters are whitespace
        """
        return s.isspace()

    @staticmethod
    def is_title(s: str) -> bool:
        """
        Check if string is in title case.

        Args:
            s: Input string

        Returns:
            True if string is title cased
        """
        return s.istitle()

    # String properties
    @staticmethod
    def length(s: str) -> int:
        """
        Get string length.

        Args:
            s: Input string

        Returns:
            Length of string
        """
        return len(s)

    @staticmethod
    def is_empty(s: str) -> bool:
        """
        Check if string is empty.

        Args:
            s: Input string

        Returns:
            True if string is empty
        """
        return len(s) == 0

    @staticmethod
    def reverse(s: str) -> str:
        """
        Reverse string.

        Args:
            s: Input string

        Returns:
            Reversed string
        """
        return s[::-1]

    # Character access
    @staticmethod
    def char_at(s: str, index: int) -> str:
        """
        Get character at index.

        Args:
            s: Input string
            index: Character index

        Returns:
            Character at index

        Raises:
            IndexError: If index is out of range
        """
        if index < 0 or index >= len(s):
            raise IndexError(f"string.char_at: index {index} out of range")
        return s[index]

    @staticmethod
    def substring(s: str, start: int, end: Optional[int] = None) -> str:
        """
        Get substring.

        Args:
            s: Input string
            start: Start index (inclusive)
            end: End index (exclusive, default: end of string)

        Returns:
            Substring
        """
        if end is None:
            return s[start:]
        return s[start:end]

    # Special functions
    @staticmethod
    def repeat(s: str, count: int) -> str:
        """
        Repeat string count times.

        Args:
            s: Input string
            count: Number of repetitions

        Returns:
            Repeated string
        """
        return s * count

    @staticmethod
    def is_palindrome(s: str) -> bool:
        """
        Check if string is a palindrome.

        Args:
            s: Input string

        Returns:
            True if string is palindrome
        """
        return s == s[::-1]

    @staticmethod
    def count_vowels(s: str) -> int:
        """
        Count vowels in string.

        Args:
            s: Input string

        Returns:
            Number of vowels
        """
        vowels = "aeiouAEIOU"
        return sum(1 for char in s if char in vowels)

    @staticmethod
    def count_consonants(s: str) -> int:
        """
        Count consonants in string.

        Args:
            s: Input string

        Returns:
            Number of consonants
        """
        consonants = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"
        return sum(1 for char in s if char in consonants)

    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> int:
        """
        Calculate Levenshtein distance between two strings.

        Args:
            s1: First string
            s2: Second string

        Returns:
            Levenshtein distance
        """
        if len(s1) < len(s2):
            return StringModule.levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]


# Create module instance
string_module = StringModule()

__all__ = ["StringModule", "string_module"]
