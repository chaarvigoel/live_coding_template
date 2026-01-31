# TestClient needs httpx: pip install httpx
import logging

import pytest
from fastapi.testclient import TestClient

from main import app  # pyright: ignore[reportMissingImports]

client = TestClient(app)

def test_post_player_creates_and_returns_player():
    r = client.post(
        "/v1/players",
        json={"firstName": "Dave", "lastName": "Davis", "weight": 75, "height": 180},
    )
    assert r.status_code == 201
    data = r.json()
    assert data["firstName"] == "Dave"
    assert data["lastName"] == "Davis"


def test_post_player_appears_in_list():
    client.post(
        "/v1/players",
        json={"firstName": "Eve", "lastName": "Evans", "weight": 60, "height": 165},
    )
    r = client.get("/v1/players", params={"isAdmin": "true"})
    assert r.status_code == 200
    names = [p["firstName"] for p in r.json()["players"]]
    assert "Eve" in names


def test_player_admin_true():
    r = client.get("/v1/players", params={"isAdmin":"true"})
    assert r.status_code == 200
    data = r.json()
    assert data["players"][0]["firstName"] == "Alice"


def test_player_admin_false():
    r = client.get("/v1/players", params={"isAdmin":"false"})
    assert r.status_code == 200
    data = r.json()
    assert data["players"][0] == {"firstName": "Alice"}
    assert data["players"][1] == {"firstName": "Bob"}
    assert "lastName" not in data["players"][0]




def test_players_invalid_is_admin():
    r = client.get("/v1/players", params={"isAdmin": "yes"})
    assert r.status_code == 400


def test_invalid_is_admin_logs_warning(caplog):
    with caplog.at_level(logging.WARNING, logger="main"):
        client.get("/v1/players", params={"isAdmin": "yes"})
    assert any("Invalid isAdmin param" in rec.message for rec in caplog.records)
    assert any(rec.levelname == "WARNING" for rec in caplog.records)


def test_unexpected_error_logs_exception(caplog, monkeypatch):
    import main
    monkeypatch.setattr(main, "PLAYERS", [object()])  # no ["firstName"] -> raises
    with caplog.at_level(logging.ERROR, logger="main"):
        r = client.get("/v1/players", params={"isAdmin": "false"})
    assert r.status_code == 500
    assert any("Unexpected error in get_players" in rec.message for rec in caplog.records)
