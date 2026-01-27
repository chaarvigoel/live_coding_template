import json

import pytest

from main import main, greet
from utils import parse_config


def test_smoke(capsys):
    main(argv=[])  # Pass empty argv to avoid pytest args
    out = capsys.readouterr().out
    assert "Template ready" in out


def test_greet():
    assert greet("Alice") == "Hello, Alice!"
    assert greet("Bob") == "Hello, Bob!"
    assert greet("") == "Hello, !"


def test_greet_single_char():
    assert greet("x") == "Hello, x!"


def test_greet_whitespace():
    assert greet("  ") == "Hello,   !"
    assert greet("a b") == "Hello, a b!"


def test_greet_unicode():
    assert greet("日本語") == "Hello, 日本語!"
    assert greet("café") == "Hello, café!"


def test_greet_long_name():
    long_name = "A" * 1000
    assert greet(long_name) == f"Hello, {long_name}!"


def test_parse_config(tmp_path):
    cfg_file = tmp_path / "config.json"
    cfg_file.write_text('{"message": "test message", "key": 42}', encoding="utf-8")
    got = parse_config(str(cfg_file))
    assert got["message"] == "test message"
    assert got["key"] == 42


def test_parse_config_missing_file():
    got = parse_config("/nonexistent/path/config.json")
    assert got == {}


def test_parse_config_empty_object(tmp_path):
    cfg_file = tmp_path / "config.json"
    cfg_file.write_text("{}", encoding="utf-8")
    got = parse_config(str(cfg_file))
    assert got == {}


def test_parse_config_no_message_key(tmp_path):
    cfg_file = tmp_path / "config.json"
    cfg_file.write_text('{"other": "value", "count": 1}', encoding="utf-8")
    got = parse_config(str(cfg_file))
    assert got == {"other": "value", "count": 1}
    assert "message" not in got


def test_parse_config_nested(tmp_path):
    cfg_file = tmp_path / "config.json"
    cfg_file.write_text(
        '{"message": "hi", "nested": {"a": 1, "b": [2, 3]}}',
        encoding="utf-8",
    )
    got = parse_config(str(cfg_file))
    assert got["message"] == "hi"
    assert got["nested"] == {"a": 1, "b": [2, 3]}


def test_parse_config_invalid_json(tmp_path):
    cfg_file = tmp_path / "config.json"
    cfg_file.write_text("{ invalid }", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        parse_config(str(cfg_file))


def test_parse_config_empty_file(tmp_path):
    cfg_file = tmp_path / "config.json"
    cfg_file.write_text("", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        parse_config(str(cfg_file))


def test_cli_with_config(tmp_path, capsys):
    """Test CLI with --config flag using a temporary config file."""
    cfg_file = tmp_path / "test_config.json"
    cfg_file.write_text('{"message": "CLI test message"}', encoding="utf-8")

    main(argv=["--config", str(cfg_file)])
    out = capsys.readouterr().out
    assert "Hello, World!" in out
    assert "CLI test message" in out
    assert "Template ready" in out


def test_main_default_config(capsys):
    """main(argv=[]) uses default config.json if present."""
    main(argv=[])
    out = capsys.readouterr().out
    assert "Hello, World!" in out
    assert "Template ready" in out


def test_main_config_missing_file(tmp_path, capsys):
    """main with --config pointing to missing file: no message, rest unchanged."""
    main(argv=["--config", str(tmp_path / "nonexistent.json")])
    out = capsys.readouterr().out
    assert "Hello, World!" in out
    assert "Template ready" in out


def test_main_config_no_message_key(tmp_path, capsys):
    """main with config that has no 'message' key: only greet + Template ready."""
    cfg_file = tmp_path / "config.json"
    cfg_file.write_text('{"other": 42}', encoding="utf-8")
    main(argv=["--config", str(cfg_file)])
    out = capsys.readouterr().out
    assert "Hello, World!" in out
    assert "Template ready" in out
    assert "42" not in out  # we don't print non-message keys


def test_main_config_empty_object(tmp_path, capsys):
    """main with config {}: no message line, greet + Template ready."""
    cfg_file = tmp_path / "config.json"
    cfg_file.write_text("{}", encoding="utf-8")
    main(argv=["--config", str(cfg_file)])
    out = capsys.readouterr().out
    assert "Hello, World!" in out
    assert "Template ready" in out


def test_main_passes_argv_to_argparse(tmp_path, capsys):
    """main(argv) forwards argv to argparse; --config is respected."""
    cfg_file = tmp_path / "alt.json"
    cfg_file.write_text('{"message": "from alt"}', encoding="utf-8")
    main(argv=["--config", str(cfg_file)])
    out = capsys.readouterr().out
    assert "from alt" in out
    assert "Hello, World!" in out
    assert "Template ready" in out
