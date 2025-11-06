"""
Tests for AIGo Standard Library - Collections Module

Tests collection operations and utilities.
"""

import pytest
from src.aigo.stdlib.collections import CollectionsModule


class TestListOperations:
    """Test basic list operations."""

    def test_map(self):
        """Test map function."""
        result = CollectionsModule.map([1, 2, 3], lambda x: x * 2)
        assert result == [2, 4, 6]

    def test_filter(self):
        """Test filter function."""
        result = CollectionsModule.filter([1, 2, 3, 4, 5], lambda x: x % 2 == 0)
        assert result == [2, 4]

    def test_reduce(self):
        """Test reduce function."""
        result = CollectionsModule.reduce([1, 2, 3, 4], lambda acc, x: acc + x, 0)
        assert result == 10

    def test_foreach(self):
        """Test foreach function."""
        results = []
        CollectionsModule.foreach([1, 2, 3], lambda x: results.append(x * 2))
        assert results == [2, 4, 6]


class TestSearching:
    """Test searching and finding functions."""

    def test_find(self):
        """Test find function."""
        result = CollectionsModule.find([1, 2, 3, 4, 5], lambda x: x > 3)
        assert result == 4

    def test_find_not_found(self):
        """Test find when not found."""
        result = CollectionsModule.find([1, 2, 3], lambda x: x > 10)
        assert result is None

    def test_find_index(self):
        """Test find_index function."""
        result = CollectionsModule.find_index([1, 2, 3, 4, 5], lambda x: x > 3)
        assert result == 3

    def test_find_index_not_found(self):
        """Test find_index when not found."""
        result = CollectionsModule.find_index([1, 2, 3], lambda x: x > 10)
        assert result == -1

    def test_contains(self):
        """Test contains function."""
        assert CollectionsModule.contains([1, 2, 3], 2) is True
        assert CollectionsModule.contains([1, 2, 3], 5) is False

    def test_index_of(self):
        """Test index_of function."""
        assert CollectionsModule.index_of([1, 2, 3, 2], 2) == 1
        assert CollectionsModule.index_of([1, 2, 3], 5) == -1


class TestAggregation:
    """Test aggregation functions."""

    def test_all(self):
        """Test all function."""
        assert CollectionsModule.all([2, 4, 6], lambda x: x % 2 == 0) is True
        assert CollectionsModule.all([2, 3, 4], lambda x: x % 2 == 0) is False

    def test_any(self):
        """Test any function."""
        assert CollectionsModule.any([1, 2, 3], lambda x: x > 2) is True
        assert CollectionsModule.any([1, 2, 3], lambda x: x > 10) is False

    def test_count(self):
        """Test count function."""
        assert CollectionsModule.count([1, 2, 3, 4, 5], lambda x: x % 2 == 0) == 2
        assert CollectionsModule.count([1, 3, 5], lambda x: x % 2 == 0) == 0


class TestTransformation:
    """Test transformation functions."""

    def test_reverse(self):
        """Test reverse function."""
        assert CollectionsModule.reverse([1, 2, 3]) == [3, 2, 1]
        assert CollectionsModule.reverse([]) == []

    def test_sort(self):
        """Test sort function."""
        assert CollectionsModule.sort([3, 1, 2]) == [1, 2, 3]
        assert CollectionsModule.sort([3, 1, 2], reverse=True) == [3, 2, 1]

    def test_sort_by(self):
        """Test sort_by function."""
        result = CollectionsModule.sort_by(["aaa", "b", "cc"], lambda x: len(x))
        assert result == ["b", "cc", "aaa"]

    def test_unique(self):
        """Test unique function."""
        assert CollectionsModule.unique([1, 2, 2, 3, 3, 3]) == [1, 2, 3]
        assert CollectionsModule.unique([1, 2, 3]) == [1, 2, 3]

    def test_flatten(self):
        """Test flatten function."""
        assert CollectionsModule.flatten([[1, 2], [3, 4], [5]]) == [1, 2, 3, 4, 5]
        assert CollectionsModule.flatten([[], [1], []]) == [1]


class TestSlicing:
    """Test slicing and chunking functions."""

    def test_take(self):
        """Test take function."""
        assert CollectionsModule.take([1, 2, 3, 4, 5], 3) == [1, 2, 3]
        assert CollectionsModule.take([1, 2], 5) == [1, 2]

    def test_skip(self):
        """Test skip function."""
        assert CollectionsModule.skip([1, 2, 3, 4, 5], 2) == [3, 4, 5]
        assert CollectionsModule.skip([1, 2], 5) == []

    def test_chunk(self):
        """Test chunk function."""
        assert CollectionsModule.chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
        assert CollectionsModule.chunk([1, 2, 3], 1) == [[1], [2], [3]]

    def test_partition(self):
        """Test partition function."""
        matching, not_matching = CollectionsModule.partition(
            [1, 2, 3, 4, 5], lambda x: x % 2 == 0
        )
        assert matching == [2, 4]
        assert not_matching == [1, 3, 5]


class TestCombining:
    """Test combining functions."""

    def test_zip(self):
        """Test zip function."""
        result = CollectionsModule.zip([1, 2, 3], ["a", "b", "c"])
        assert result == [(1, "a"), (2, "b"), (3, "c")]

    def test_concat(self):
        """Test concat function."""
        result = CollectionsModule.concat([[1, 2], [3, 4], [5]])
        assert result == [1, 2, 3, 4, 5]


class TestNumericOperations:
    """Test numeric operation functions."""

    def test_sum(self):
        """Test sum function."""
        assert CollectionsModule.sum([1, 2, 3, 4, 5]) == 15
        assert CollectionsModule.sum([]) == 0

    def test_product(self):
        """Test product function."""
        assert CollectionsModule.product([1, 2, 3, 4]) == 24
        assert CollectionsModule.product([5, 2]) == 10

    def test_min(self):
        """Test min function."""
        assert CollectionsModule.min([3, 1, 4, 1, 5]) == 1

    def test_min_empty_raises_error(self):
        """Test that min of empty list raises error."""
        with pytest.raises(ValueError):
            CollectionsModule.min([])

    def test_max(self):
        """Test max function."""
        assert CollectionsModule.max([3, 1, 4, 1, 5]) == 5

    def test_max_empty_raises_error(self):
        """Test that max of empty list raises error."""
        with pytest.raises(ValueError):
            CollectionsModule.max([])


class TestListProperties:
    """Test list property functions."""

    def test_length(self):
        """Test length function."""
        assert CollectionsModule.length([1, 2, 3]) == 3
        assert CollectionsModule.length([]) == 0

    def test_is_empty(self):
        """Test is_empty function."""
        assert CollectionsModule.is_empty([]) is True
        assert CollectionsModule.is_empty([1]) is False

    def test_first(self):
        """Test first function."""
        assert CollectionsModule.first([1, 2, 3]) == 1
        assert CollectionsModule.first([]) is None

    def test_last(self):
        """Test last function."""
        assert CollectionsModule.last([1, 2, 3]) == 3
        assert CollectionsModule.last([]) is None


class TestSetOperations:
    """Test set operation functions."""

    def test_union(self):
        """Test union function."""
        result = CollectionsModule.union([1, 2, 3], [3, 4, 5])
        assert set(result) == {1, 2, 3, 4, 5}

    def test_intersection(self):
        """Test intersection function."""
        result = CollectionsModule.intersection([1, 2, 3], [2, 3, 4])
        assert set(result) == {2, 3}

    def test_difference(self):
        """Test difference function."""
        result = CollectionsModule.difference([1, 2, 3], [2, 3, 4])
        assert set(result) == {1}


class TestDictionaryOperations:
    """Test dictionary operation functions."""

    def test_dict_keys(self):
        """Test dict_keys function."""
        result = CollectionsModule.dict_keys({"a": 1, "b": 2, "c": 3})
        assert set(result) == {"a", "b", "c"}

    def test_dict_values(self):
        """Test dict_values function."""
        result = CollectionsModule.dict_values({"a": 1, "b": 2, "c": 3})
        assert set(result) == {1, 2, 3}

    def test_dict_items(self):
        """Test dict_items function."""
        result = CollectionsModule.dict_items({"a": 1, "b": 2})
        assert set(result) == {("a", 1), ("b", 2)}
