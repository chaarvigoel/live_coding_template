"""Tests for nested set equality."""

import pytest

from set_compare import nested_sets_equal  # pyright: ignore[reportMissingImports]


def test_empty_sets_equal():
    assert nested_sets_equal(set(), set()) is True


def test_single_string_equal():
    assert nested_sets_equal({"a"}, {"a"}) is True


def test_string_order_irrelevant():
    assert nested_sets_equal({"a", "b"}, {"b", "a"}) is True


def test_different_strings_unequal():
    assert nested_sets_equal({"a"}, {"b"}) is False


def test_nested_set_equal():
    assert nested_sets_equal({"a", frozenset({"b"})}, {"a", frozenset({"b"})}) is True


def test_nested_set_order_irrelevant():
    assert nested_sets_equal({"a", frozenset({"b", "c"})}, {"a", frozenset({"c", "b"})}) is True


def test_different_nested_content_unequal():
    assert nested_sets_equal({"a", frozenset({"b"})}, {"a", frozenset({"c"})}) is False


def test_different_sizes_unequal():
    assert nested_sets_equal({"a"}, {"a", "b"}) is False


def test_deeply_nested_equal():
    inner = frozenset({"x"})
    outer = frozenset({"a", inner})
    assert nested_sets_equal({outer}, {outer}) is True
