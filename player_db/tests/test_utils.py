"""Unit tests for utility functions."""

from main import find_player  # pyright: ignore[reportMissingImports]


def test_find_player_exists():
    players = [
        {"id": 1, "firstName": "Alice"},
        {"id": 2, "firstName": "Bob"},
    ]
    assert find_player(players, 1) == {"id": 1, "firstName": "Alice"}
    assert find_player(players, 2) == {"id": 2, "firstName": "Bob"}


def test_find_player_not_found():
    players = [{"id": 1, "firstName": "Alice"}]
    assert find_player(players, 999) is None
    assert find_player(players, 0) is None


def test_find_player_empty_list():
    assert find_player([], 1) is None


def test_find_player_returns_first_match():
    players = [
        {"id": 1, "firstName": "First"},
        {"id": 1, "firstName": "Duplicate"},
    ]
    result = find_player(players, 1)
    assert result is not None
    assert result["firstName"] == "First"


def test_find_player_missing_id_key():
    players = [{"firstName": "NoId"}]
    assert find_player(players, 1) is None


def test_find_player_id_zero():
    players = [{"id": 0, "firstName": "Zero"}]
    assert find_player(players, 0) == {"id": 0, "firstName": "Zero"}
