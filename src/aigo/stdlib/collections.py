"""
AIGo Standard Library - Collections Module

Collection utilities and data structures for AIGo programs.

This module provides:
- List operations (map, filter, reduce, etc.)
- Array utilities
- Stack and Queue helpers
- Set operations
- Dictionary utilities

Usage in AIGo:
    import std.collections

    let doubled: array<i32> = collections.map(numbers, double_fn)
    let evens: array<i32> = collections.filter(numbers, is_even_fn)
    let sum: i32 = collections.reduce(numbers, add_fn, 0)
"""

from typing import List, Any, Callable, Optional, TypeVar, Set, Dict

T = TypeVar("T")
U = TypeVar("U")


class CollectionsModule:
    """AIGo Collections standard library module."""

    # List operations
    @staticmethod
    def map(items: List[T], func: Callable[[T], U]) -> List[U]:
        """
        Apply function to each element.

        Args:
            items: Input list
            func: Function to apply

        Returns:
            List of transformed elements
        """
        return [func(item) for item in items]

    @staticmethod
    def filter(items: List[T], predicate: Callable[[T], bool]) -> List[T]:
        """
        Filter list by predicate.

        Args:
            items: Input list
            predicate: Filter function

        Returns:
            List of items matching predicate
        """
        return [item for item in items if predicate(item)]

    @staticmethod
    def reduce(items: List[T], func: Callable[[U, T], U], initial: U) -> U:
        """
        Reduce list to single value.

        Args:
            items: Input list
            func: Reduction function
            initial: Initial value

        Returns:
            Reduced value
        """
        result = initial
        for item in items:
            result = func(result, item)
        return result

    @staticmethod
    def foreach(items: List[T], func: Callable[[T], None]) -> None:
        """
        Apply function to each element (for side effects).

        Args:
            items: Input list
            func: Function to apply
        """
        for item in items:
            func(item)

    # Searching and finding
    @staticmethod
    def find(items: List[T], predicate: Callable[[T], bool]) -> Optional[T]:
        """
        Find first element matching predicate.

        Args:
            items: Input list
            predicate: Search predicate

        Returns:
            First matching element or None
        """
        for item in items:
            if predicate(item):
                return item
        return None

    @staticmethod
    def find_index(items: List[T], predicate: Callable[[T], bool]) -> int:
        """
        Find index of first element matching predicate.

        Args:
            items: Input list
            predicate: Search predicate

        Returns:
            Index of first match, or -1 if not found
        """
        for i, item in enumerate(items):
            if predicate(item):
                return i
        return -1

    @staticmethod
    def contains(items: List[T], value: T) -> bool:
        """
        Check if list contains value.

        Args:
            items: Input list
            value: Value to find

        Returns:
            True if value is in list
        """
        return value in items

    @staticmethod
    def index_of(items: List[T], value: T) -> int:
        """
        Get index of first occurrence of value.

        Args:
            items: Input list
            value: Value to find

        Returns:
            Index of value, or -1 if not found
        """
        try:
            return items.index(value)
        except ValueError:
            return -1

    # Aggregation
    @staticmethod
    def all(items: List[T], predicate: Callable[[T], bool]) -> bool:
        """
        Check if all elements match predicate.

        Args:
            items: Input list
            predicate: Predicate function

        Returns:
            True if all elements match
        """
        return all(predicate(item) for item in items)

    @staticmethod
    def any(items: List[T], predicate: Callable[[T], bool]) -> bool:
        """
        Check if any element matches predicate.

        Args:
            items: Input list
            predicate: Predicate function

        Returns:
            True if any element matches
        """
        return any(predicate(item) for item in items)

    @staticmethod
    def count(items: List[T], predicate: Callable[[T], bool]) -> int:
        """
        Count elements matching predicate.

        Args:
            items: Input list
            predicate: Predicate function

        Returns:
            Number of matching elements
        """
        return sum(1 for item in items if predicate(item))

    # Transformation
    @staticmethod
    def reverse(items: List[T]) -> List[T]:
        """
        Reverse list.

        Args:
            items: Input list

        Returns:
            Reversed list
        """
        return list(reversed(items))

    @staticmethod
    def sort(items: List[T], reverse: bool = False) -> List[T]:
        """
        Sort list.

        Args:
            items: Input list
            reverse: Sort in descending order (default: False)

        Returns:
            Sorted list
        """
        return sorted(items, reverse=reverse)

    @staticmethod
    def sort_by(items: List[T], key: Callable[[T], Any], reverse: bool = False) -> List[T]:
        """
        Sort list by key function.

        Args:
            items: Input list
            key: Key extraction function
            reverse: Sort in descending order (default: False)

        Returns:
            Sorted list
        """
        return sorted(items, key=key, reverse=reverse)

    @staticmethod
    def unique(items: List[T]) -> List[T]:
        """
        Remove duplicates preserving order.

        Args:
            items: Input list

        Returns:
            List with duplicates removed
        """
        seen: Set[T] = set()
        result = []
        for item in items:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result

    @staticmethod
    def flatten(items: List[List[T]]) -> List[T]:
        """
        Flatten nested list.

        Args:
            items: Nested list

        Returns:
            Flattened list
        """
        return [item for sublist in items for item in sublist]

    # Slicing and chunking
    @staticmethod
    def take(items: List[T], n: int) -> List[T]:
        """
        Take first n elements.

        Args:
            items: Input list
            n: Number of elements

        Returns:
            First n elements
        """
        return items[:n]

    @staticmethod
    def skip(items: List[T], n: int) -> List[T]:
        """
        Skip first n elements.

        Args:
            items: Input list
            n: Number of elements to skip

        Returns:
            List without first n elements
        """
        return items[n:]

    @staticmethod
    def chunk(items: List[T], size: int) -> List[List[T]]:
        """
        Split list into chunks of given size.

        Args:
            items: Input list
            size: Chunk size

        Returns:
            List of chunks
        """
        return [items[i : i + size] for i in range(0, len(items), size)]

    @staticmethod
    def partition(items: List[T], predicate: Callable[[T], bool]) -> tuple[List[T], List[T]]:
        """
        Partition list by predicate.

        Args:
            items: Input list
            predicate: Partition predicate

        Returns:
            Tuple of (matching, not_matching)
        """
        matching = []
        not_matching = []
        for item in items:
            if predicate(item):
                matching.append(item)
            else:
                not_matching.append(item)
        return matching, not_matching

    # Combining
    @staticmethod
    def zip(list1: List[T], list2: List[U]) -> List[tuple[T, U]]:
        """
        Zip two lists together.

        Args:
            list1: First list
            list2: Second list

        Returns:
            List of tuples
        """
        return list(zip(list1, list2))

    @staticmethod
    def concat(lists: List[List[T]]) -> List[T]:
        """
        Concatenate multiple lists.

        Args:
            lists: List of lists

        Returns:
            Concatenated list
        """
        result = []
        for lst in lists:
            result.extend(lst)
        return result

    # Numeric operations
    @staticmethod
    def sum(items: List[int]) -> int:
        """
        Sum of all elements.

        Args:
            items: List of numbers

        Returns:
            Sum
        """
        return sum(items)

    @staticmethod
    def product(items: List[int]) -> int:
        """
        Product of all elements.

        Args:
            items: List of numbers

        Returns:
            Product
        """
        result = 1
        for item in items:
            result *= item
        return result

    @staticmethod
    def min(items: List[T]) -> T:
        """
        Minimum element.

        Args:
            items: Input list

        Returns:
            Minimum element

        Raises:
            ValueError: If list is empty
        """
        if not items:
            raise ValueError("collections.min: empty list")
        return min(items)

    @staticmethod
    def max(items: List[T]) -> T:
        """
        Maximum element.

        Args:
            items: Input list

        Returns:
            Maximum element

        Raises:
            ValueError: If list is empty
        """
        if not items:
            raise ValueError("collections.max: empty list")
        return max(items)

    # List properties
    @staticmethod
    def length(items: List[T]) -> int:
        """
        Get list length.

        Args:
            items: Input list

        Returns:
            Length of list
        """
        return len(items)

    @staticmethod
    def is_empty(items: List[T]) -> bool:
        """
        Check if list is empty.

        Args:
            items: Input list

        Returns:
            True if list is empty
        """
        return len(items) == 0

    @staticmethod
    def first(items: List[T]) -> Optional[T]:
        """
        Get first element.

        Args:
            items: Input list

        Returns:
            First element or None if empty
        """
        return items[0] if items else None

    @staticmethod
    def last(items: List[T]) -> Optional[T]:
        """
        Get last element.

        Args:
            items: Input list

        Returns:
            Last element or None if empty
        """
        return items[-1] if items else None

    # Set operations
    @staticmethod
    def union(set1: List[T], set2: List[T]) -> List[T]:
        """
        Union of two lists (unique elements).

        Args:
            set1: First list
            set2: Second list

        Returns:
            Union of lists
        """
        return list(set(set1) | set(set2))

    @staticmethod
    def intersection(set1: List[T], set2: List[T]) -> List[T]:
        """
        Intersection of two lists.

        Args:
            set1: First list
            set2: Second list

        Returns:
            Intersection of lists
        """
        return list(set(set1) & set(set2))

    @staticmethod
    def difference(set1: List[T], set2: List[T]) -> List[T]:
        """
        Difference of two lists (elements in set1 but not in set2).

        Args:
            set1: First list
            set2: Second list

        Returns:
            Difference of lists
        """
        return list(set(set1) - set(set2))

    # Dictionary operations
    @staticmethod
    def dict_keys(d: Dict[T, U]) -> List[T]:
        """
        Get dictionary keys.

        Args:
            d: Input dictionary

        Returns:
            List of keys
        """
        return list(d.keys())

    @staticmethod
    def dict_values(d: Dict[T, U]) -> List[U]:
        """
        Get dictionary values.

        Args:
            d: Input dictionary

        Returns:
            List of values
        """
        return list(d.values())

    @staticmethod
    def dict_items(d: Dict[T, U]) -> List[tuple[T, U]]:
        """
        Get dictionary items.

        Args:
            d: Input dictionary

        Returns:
            List of (key, value) tuples
        """
        return list(d.items())


# Create module instance
collections_module = CollectionsModule()

__all__ = ["CollectionsModule", "collections_module"]
