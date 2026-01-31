# TestClient needs httpx: pip install httpx
import logging

import pytest
from fastapi.testclient import TestClient

from main import app  # pyright: ignore[reportMissingImports]

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_store(monkeypatch):
    import main
    monkeypatch.setattr(main, "MANAGERS", [{"id": 1, "name": "Mike Smith"}, {"id": 2, "name": "Jane Doe"}])
    monkeypatch.setattr(main, "TEAMS", [{"id": 1, "name": "Eagles", "location": "Boston"}, {"id": 2, "name": "Hawks", "location": "Chicago"}])
    monkeypatch.setattr(
        main,
        "PLAYERS",
        [
            {"id": 1, "firstName": "Alice", "lastName": "Anderson", "weight": 65, "height": 170, "manager_id": 1, "team_id": 1},
            {"id": 2, "firstName": "Bob", "lastName": "Brown", "weight": 80, "height": 182, "manager_id": 1, "team_id": 1},
            {"id": 3, "firstName": "Carol", "lastName": "Clark", "weight": 58, "height": 165, "manager_id": 2, "team_id": 2},
        ],
    )
    monkeypatch.setattr(main, "BATTING_STATS", [{"id": 1, "player_id": 1, "season": 2024, "at_bats": 100, "hits": 30}])
    monkeypatch.setattr(main, "FIELDING_STATS", [{"id": 1, "player_id": 1, "season": 2024, "position": "SS"}])
    monkeypatch.setattr(main, "PITCHING_STATS", [])
    monkeypatch.setattr(main, "_next_id", 4)
    monkeypatch.setattr(main, "_player_cache", {})

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


def test_player_admin_false():
    r = client.get("/v1/players", params={"isAdmin":"false"})
    assert r.status_code == 200
    data = r.json()
    assert data["players"][0] == {"firstName": "Alice"}
    assert "lastName" not in data["players"][0]



def test_players_invalid_is_admin():
    r = client.get("/v1/players", params={"isAdmin": "yes"})
    assert r.status_code == 400


def test_get_player_by_id(monkeypatch):
    monkeypatch.setattr("main.time.sleep", lambda s: None)
    r = client.get("/v1/players/1")
    assert r.status_code == 200
    assert r.json()["firstName"] == "Alice"


def test_get_player_by_id_not_found(monkeypatch):
    monkeypatch.setattr("main.time.sleep", lambda s: None)
    r = client.get("/v1/players/999")
    assert r.status_code == 404


def test_patch_invalidates_cache(monkeypatch):
    monkeypatch.setattr("main.time.sleep", lambda s: None)
    client.get("/v1/players/1")
    client.patch("/v1/players/1", json={"firstName": "Alicia"})
    r = client.get("/v1/players/1")
    assert r.json()["firstName"] == "Alicia"


def test_patch_weight_updates_and_verifiable_via_get(monkeypatch):
    monkeypatch.setattr("main.time.sleep", lambda s: None)
    r = client.patch("/v1/players/1", json={"weight": 100})
    assert r.status_code == 200
    assert r.json()["weight"] == 100
    r2 = client.get("/v1/players/1")
    assert r2.json()["weight"] == 100


def test_patch_weight_non_integer_returns_422():
    r = client.patch("/v1/players/1", json={"weight": "not-a-number"})
    assert r.status_code == 422


def test_patch_weight_out_of_range_returns_422():
    r = client.patch("/v1/players/1", json={"weight": 600})
    assert r.status_code == 422


def test_get_player_by_id_includes_manager_and_team(monkeypatch):
    monkeypatch.setattr("main.time.sleep", lambda s: None)
    r = client.get("/v1/players/1")
    assert r.status_code == 200
    assert r.json()["manager"] == {"id": 1, "name": "Mike Smith"}
    assert r.json()["team"] == {"id": 1, "name": "Eagles", "location": "Boston"}


def test_get_player_batting(monkeypatch):
    monkeypatch.setattr("main.time.sleep", lambda s: None)
    r = client.get("/v1/players/1/batting")
    assert r.status_code == 200
    assert r.json()["player_id"] == 1
    assert len(r.json()["batting"]) == 1
    assert r.json()["batting"][0]["hits"] == 30


def test_get_player_fielding():
    r = client.get("/v1/players/1/fielding")
    assert r.status_code == 200
    assert r.json()["fielding"][0]["position"] == "SS"


def test_sort_by_weight():
    r = client.get("/v1/players", params={"isAdmin": "true", "sort": "weight"})
    assert r.status_code == 200
    weights = [p["weight"] for p in r.json()["players"]]
    assert weights == sorted(weights)


def test_sort_invalid_returns_400():
    r = client.get("/v1/players", params={"isAdmin": "true", "sort": "age"})
    assert r.status_code == 400


def test_pagination_page1_limit2():
    r = client.get("/v1/players", params={"isAdmin": "true", "page": 1, "limit": 2})
    assert r.status_code == 200
    data = r.json()
    assert len(data["players"]) == 2
    assert data["total"] == 3


def test_pagination_page_beyond_returns_empty():
    r = client.get("/v1/players", params={"isAdmin": "true", "page": 10, "limit": 5})
    assert r.status_code == 200
    assert r.json()["players"] == []
    assert r.json()["total"] == 3


def test_unexpected_error_logs_exception(caplog, monkeypatch):
    import main
    monkeypatch.setattr(main, "PLAYERS", [object()])
    no_raise_client = TestClient(app, raise_server_exceptions=False)
    with caplog.at_level(logging.ERROR, logger="main"):
        r = no_raise_client.get("/v1/players", params={"isAdmin": "false"})
    assert r.status_code == 500
    assert any("Unhandled" in rec.message for rec in caplog.records)
