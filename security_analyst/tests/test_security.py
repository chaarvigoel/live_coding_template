"""Security-related tests."""

import pytest
from fastapi.testclient import TestClient

from main import app  # pyright: ignore[reportMissingImports]

client = TestClient(app)
_SEED = [
    {"id": 1, "reporter": {"firstName": "Alice", "lastName": "Anderson", "email": "alice@example.com"}},
    {"id": 2, "reporter": {"firstName": "Bob", "lastName": "Brown", "email": "bob@corp.com"}},
    {"id": 3, "reporter": {"firstName": "Carol", "lastName": "Clark", "email": "carol@acme.org"}},
]


@pytest.fixture(autouse=True)
def reset_store(monkeypatch):
    import main
    monkeypatch.setattr(main, "INCIDENTS", [dict(i) for i in _SEED])
    monkeypatch.setattr(main, "_next_id", 4)


def test_include_pii_false_returns_first_name_only():
    r = client.get("/v1/incidents", params={"includePII": "false"})
    assert r.status_code == 200
    data = r.json()
    first = data["incidents"][0]
    assert first["reporter"] == {"firstName": "Alice"}
    assert "email" not in first["reporter"]


def test_include_pii_true_returns_full_reporter():
    r = client.get("/v1/incidents", params={"includePII": "true"})
    assert r.status_code == 200
    data = r.json()
    first = data["incidents"][0]
    assert first["reporter"]["email"] == "alice@example.com"


def test_include_pii_invalid_returns_400():
    r = client.get("/v1/incidents", params={"includePII": "yes"})
    assert r.status_code == 400


def test_create_incident_returns_201():
    r = client.post(
        "/v1/incidents",
        json={"reporter": {"firstName": "Dave", "lastName": "Davis", "email": "dave@test.com"}},
    )
    assert r.status_code == 201
    data = r.json()
    assert data["id"] == 4
    assert data["reporter"]["firstName"] == "Dave"
    assert data["reporter"]["email"] == "dave@test.com"


def test_create_incident_appears_in_list():
    client.post(
        "/v1/incidents",
        json={"reporter": {"firstName": "Eve", "lastName": "Evans", "email": "eve@test.com"}},
    )
    r = client.get("/v1/incidents", params={"includePII": "true"})
    assert r.status_code == 200
    names = [i["reporter"]["firstName"] for i in r.json()["incidents"]]
    assert "Eve" in names


# --- Part 1 edge cases ---


def test_include_pii_missing_returns_422():
    r = client.get("/v1/incidents")
    assert r.status_code == 422


def test_include_pii_case_sensitivity_true_rejected():
    r = client.get("/v1/incidents", params={"includePII": "True"})
    assert r.status_code == 400


def test_include_pii_empty_incidents(monkeypatch):
    import main
    monkeypatch.setattr(main, "INCIDENTS", [])
    r = client.get("/v1/incidents", params={"includePII": "true"})
    assert r.status_code == 200
    assert r.json() == {"incidents": []}


def test_include_pii_reporter_missing_first_name_returns_500(monkeypatch):
    import main
    monkeypatch.setattr(main, "INCIDENTS", [{"id": 1, "reporter": {"lastName": "X", "email": "a@b.com"}}])
    no_raise = TestClient(app, raise_server_exceptions=False)
    r = no_raise.get("/v1/incidents", params={"includePII": "false"})
    assert r.status_code == 500


# --- Part 2 edge cases ---


def test_create_missing_required_field_returns_422():
    r = client.post("/v1/incidents", json={"reporter": {"firstName": "X", "lastName": "Y"}})
    assert r.status_code == 422


def test_create_missing_reporter_returns_422():
    r = client.post("/v1/incidents", json={})
    assert r.status_code == 422


def test_create_empty_first_name_accepted():
    r = client.post(
        "/v1/incidents",
        json={"reporter": {"firstName": "", "lastName": "Smith", "email": "a@b.com"}},
    )
    assert r.status_code == 201
    assert r.json()["reporter"]["firstName"] == ""


def test_create_null_email_returns_422():
    r = client.post(
        "/v1/incidents",
        json={"reporter": {"firstName": "X", "lastName": "Y", "email": None}},
    )
    assert r.status_code == 422


def test_create_extra_fields_ignored():
    r = client.post(
        "/v1/incidents",
        json={
            "reporter": {"firstName": "Z", "lastName": "Zed", "email": "z@z.com"},
            "extraField": "ignored",
        },
    )
    assert r.status_code == 201
    assert "extraField" not in r.json()
