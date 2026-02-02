"""
Nested set equality: determine if two sets (which can contain strings or nested sets)
are exactly the same, without using built-in set equality.

Note: In Python, nested sets must use frozenset (sets are unhashable).
      e.g. {"a", frozenset({"b"})} not {"a", {"b"}}
"""


def nested_sets_equal(a: set | frozenset, b: set | frozenset) -> bool:
    """
    Return True iff a and b contain the same elements.

    Elements may be strings or recursively nested frozensets.
    Does not use built-in set equality.
    """
    a, b = set(a), set(b)
    if len(a) != len(b):
        return False
    b_remaining = list(b)
    for x in a:
        for i, y in enumerate(b_remaining):
            if _elem_equal(x, y):
                b_remaining.pop(i)
                break
        else:
            return False
    return True


def _elem_equal(x, y) -> bool:
    if type(x) != type(y):
        return False
    if isinstance(x, str):
        return x == y
    return nested_sets_equal(x, y)
