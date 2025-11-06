"""
Tests for AIGo Standard Library - String Module

Tests all string manipulation functions.
"""

import pytest
from src.aigo.stdlib.string import StringModule


class TestCaseConversion:
    """Test case conversion functions."""

    def test_to_upper(self):
        """Test uppercase conversion."""
        assert StringModule.to_upper("hello") == "HELLO"
        assert StringModule.to_upper("Hello World") == "HELLO WORLD"
        assert StringModule.to_upper("123abc") == "123ABC"

    def test_to_lower(self):
        """Test lowercase conversion."""
        assert StringModule.to_lower("HELLO") == "hello"
        assert StringModule.to_lower("Hello World") == "hello world"
        assert StringModule.to_lower("123ABC") == "123abc"

    def test_to_title(self):
        """Test title case conversion."""
        assert StringModule.to_title("hello world") == "Hello World"
        assert StringModule.to_title("the quick brown fox") == "The Quick Brown Fox"

    def test_capitalize(self):
        """Test capitalize function."""
        assert StringModule.capitalize("hello world") == "Hello world"
        assert StringModule.capitalize("HELLO") == "Hello"

    def test_swap_case(self):
        """Test swap case function."""
        assert StringModule.swap_case("Hello World") == "hELLO wORLD"
        assert StringModule.swap_case("ABC123def") == "abc123DEF"


class TestTrimming:
    """Test trimming functions."""

    def test_trim(self):
        """Test trim function."""
        assert StringModule.trim("  hello  ") == "hello"
        assert StringModule.trim("\t\ntest\n\t") == "test"

    def test_trim_left(self):
        """Test left trim function."""
        assert StringModule.trim_left("  hello  ") == "hello  "
        assert StringModule.trim_left("\t\ntest") == "test"

    def test_trim_right(self):
        """Test right trim function."""
        assert StringModule.trim_right("  hello  ") == "  hello"
        assert StringModule.trim_right("test\n\t") == "test"

    def test_trim_chars(self):
        """Test trim with specific characters."""
        assert StringModule.trim_chars("***hello***", "*") == "hello"
        assert StringModule.trim_chars("abcHELLOabc", "abc") == "HELLO"


class TestSearching:
    """Test searching functions."""

    def test_contains(self):
        """Test contains function."""
        assert StringModule.contains("hello world", "world") is True
        assert StringModule.contains("hello world", "xyz") is False

    def test_starts_with(self):
        """Test starts_with function."""
        assert StringModule.starts_with("hello world", "hello") is True
        assert StringModule.starts_with("hello world", "world") is False

    def test_ends_with(self):
        """Test ends_with function."""
        assert StringModule.ends_with("hello world", "world") is True
        assert StringModule.ends_with("hello world", "hello") is False

    def test_find(self):
        """Test find function."""
        assert StringModule.find("hello world", "world") == 6
        assert StringModule.find("hello world", "xyz") == -1
        assert StringModule.find("hello world hello", "hello", 5) == 12

    def test_rfind(self):
        """Test reverse find function."""
        assert StringModule.rfind("hello world hello", "hello") == 12
        assert StringModule.rfind("hello world", "xyz") == -1

    def test_count(self):
        """Test count function."""
        assert StringModule.count("hello world hello", "hello") == 2
        assert StringModule.count("aaa", "aa") == 2
        assert StringModule.count("hello", "xyz") == 0


class TestReplacing:
    """Test replacing functions."""

    def test_replace(self):
        """Test replace function."""
        assert StringModule.replace("hello world", "world", "AIGo") == "hello AIGo"
        assert StringModule.replace("aaa", "a", "b", 2) == "bba"

    def test_replace_all(self):
        """Test replace all function."""
        assert StringModule.replace_all("hello hello", "hello", "hi") == "hi hi"
        assert StringModule.replace_all("aaa", "a", "b") == "bbb"


class TestSplitting:
    """Test splitting and joining functions."""

    def test_split(self):
        """Test split function."""
        assert StringModule.split("a,b,c", ",") == ["a", "b", "c"]
        assert StringModule.split("one two three") == ["one", "two", "three"]

    def test_split_with_maxsplit(self):
        """Test split with maxsplit."""
        assert StringModule.split("a,b,c,d", ",", 2) == ["a", "b", "c,d"]

    def test_split_lines(self):
        """Test split lines function."""
        assert StringModule.split_lines("a\nb\nc") == ["a", "b", "c"]
        assert StringModule.split_lines("a\r\nb\nc") == ["a", "b", "c"]

    def test_join(self):
        """Test join function."""
        assert StringModule.join(",", ["a", "b", "c"]) == "a,b,c"
        assert StringModule.join(" ", ["hello", "world"]) == "hello world"


class TestPadding:
    """Test padding functions."""

    def test_pad_left(self):
        """Test left padding."""
        assert StringModule.pad_left("5", 3) == "  5"
        assert StringModule.pad_left("5", 3, "0") == "005"

    def test_pad_right(self):
        """Test right padding."""
        assert StringModule.pad_right("5", 3) == "5  "
        assert StringModule.pad_right("5", 3, "0") == "500"

    def test_pad_center(self):
        """Test center padding."""
        assert StringModule.pad_center("5", 3) == " 5 "
        assert len(StringModule.pad_center("test", 10)) == 10

    def test_zero_pad(self):
        """Test zero padding."""
        assert StringModule.zero_pad("42", 5) == "00042"
        assert StringModule.zero_pad("100", 5) == "00100"


class TestCharacterAnalysis:
    """Test character analysis functions."""

    def test_is_alpha(self):
        """Test is_alpha function."""
        assert StringModule.is_alpha("hello") is True
        assert StringModule.is_alpha("hello123") is False
        assert StringModule.is_alpha("") is False

    def test_is_digit(self):
        """Test is_digit function."""
        assert StringModule.is_digit("123") is True
        assert StringModule.is_digit("12a") is False
        assert StringModule.is_digit("") is False

    def test_is_alnum(self):
        """Test is_alnum function."""
        assert StringModule.is_alnum("hello123") is True
        assert StringModule.is_alnum("hello 123") is False
        assert StringModule.is_alnum("") is False

    def test_is_lower(self):
        """Test is_lower function."""
        assert StringModule.is_lower("hello") is True
        assert StringModule.is_lower("Hello") is False
        assert StringModule.is_lower("123") is False

    def test_is_upper(self):
        """Test is_upper function."""
        assert StringModule.is_upper("HELLO") is True
        assert StringModule.is_upper("Hello") is False
        assert StringModule.is_upper("123") is False

    def test_is_space(self):
        """Test is_space function."""
        assert StringModule.is_space("   ") is True
        assert StringModule.is_space("\t\n") is True
        assert StringModule.is_space("hello") is False

    def test_is_title(self):
        """Test is_title function."""
        assert StringModule.is_title("Hello World") is True
        assert StringModule.is_title("hello world") is False


class TestStringProperties:
    """Test string property functions."""

    def test_length(self):
        """Test length function."""
        assert StringModule.length("hello") == 5
        assert StringModule.length("") == 0
        assert StringModule.length("hello world") == 11

    def test_is_empty(self):
        """Test is_empty function."""
        assert StringModule.is_empty("") is True
        assert StringModule.is_empty("hello") is False

    def test_reverse(self):
        """Test reverse function."""
        assert StringModule.reverse("hello") == "olleh"
        assert StringModule.reverse("12345") == "54321"
        assert StringModule.reverse("") == ""


class TestCharacterAccess:
    """Test character access functions."""

    def test_char_at(self):
        """Test char_at function."""
        assert StringModule.char_at("hello", 0) == "h"
        assert StringModule.char_at("hello", 4) == "o"

    def test_char_at_out_of_range_raises_error(self):
        """Test that char_at out of range raises error."""
        with pytest.raises(IndexError):
            StringModule.char_at("hello", 10)
        with pytest.raises(IndexError):
            StringModule.char_at("hello", -1)

    def test_substring(self):
        """Test substring function."""
        assert StringModule.substring("hello world", 0, 5) == "hello"
        assert StringModule.substring("hello world", 6) == "world"
        assert StringModule.substring("hello", 1, 4) == "ell"


class TestSpecialFunctions:
    """Test special string functions."""

    def test_repeat(self):
        """Test repeat function."""
        assert StringModule.repeat("ha", 3) == "hahaha"
        assert StringModule.repeat("x", 0) == ""

    def test_is_palindrome(self):
        """Test is_palindrome function."""
        assert StringModule.is_palindrome("racecar") is True
        assert StringModule.is_palindrome("hello") is False
        assert StringModule.is_palindrome("") is True
        assert StringModule.is_palindrome("a") is True

    def test_count_vowels(self):
        """Test count_vowels function."""
        assert StringModule.count_vowels("hello") == 2
        assert StringModule.count_vowels("aeiou") == 5
        assert StringModule.count_vowels("xyz") == 0

    def test_count_consonants(self):
        """Test count_consonants function."""
        assert StringModule.count_consonants("hello") == 3
        assert StringModule.count_consonants("aeiou") == 0
        assert StringModule.count_consonants("bcdfg") == 5

    def test_levenshtein_distance(self):
        """Test Levenshtein distance calculation."""
        assert StringModule.levenshtein_distance("kitten", "sitting") == 3
        assert StringModule.levenshtein_distance("hello", "hello") == 0
        assert StringModule.levenshtein_distance("", "abc") == 3
        assert StringModule.levenshtein_distance("abc", "") == 3
