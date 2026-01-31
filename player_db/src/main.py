import logging
import time

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
app = FastAPI()

# --- Models ---
# Player: schema for creating a player (POST body) and full player response
class Player(BaseModel):
    id: int | None = None
    firstName: str
    lastName: str
    weight: int = Field(ge=1, le=500)
    height: int = Field(ge=1, le=300)
    manager_id: int | None = None
    team_id: int | None = None


# UpdatePlayer: schema for partial updates (PATCH body); all fields optional
class UpdatePlayer(BaseModel):
    firstName: str | None = None
    lastName: str | None = None
    weight: int | None = Field(None, ge=1, le=500)
    height: int | None = Field(None, ge=1, le=300)
    manager_id: int | None = None
    team_id: int | None = None


# --- Store ---
# _next_id: auto-increment for new player ids
# _player_cache: cache for GET /players/{id} (invalidated on PATCH)
_next_id = 4
_player_cache: dict[int, dict] = {}

MANAGERS: list[dict] = [
    {"id": 1, "name": "Mike Smith"},
    {"id": 2, "name": "Jane Doe"},
]

TEAMS: list[dict] = [
    {"id": 1, "name": "Eagles", "location": "Boston"},
    {"id": 2, "name": "Hawks", "location": "Chicago"},
]

PLAYERS: list[dict] = [
    {"id": 1, "firstName": "Alice", "lastName": "Anderson", "weight": 65, "height": 170, "manager_id": 1, "team_id": 1},
    {"id": 2, "firstName": "Bob", "lastName": "Brown", "weight": 80, "height": 182, "manager_id": 1, "team_id": 1},
    {"id": 3, "firstName": "Carol", "lastName": "Clark", "weight": 58, "height": 165, "manager_id": 2, "team_id": 2},
]

BATTING_STATS: list[dict] = [
    {"id": 1, "player_id": 1, "season": 2024, "at_bats": 100, "hits": 30, "home_runs": 5},
    {"id": 2, "player_id": 2, "season": 2024, "at_bats": 95, "hits": 28, "home_runs": 3},
]

FIELDING_STATS: list[dict] = [
    {"id": 1, "player_id": 1, "season": 2024, "position": "SS", "errors": 2, "assists": 45},
]

PITCHING_STATS: list[dict] = [
    {"id": 1, "player_id": 2, "season": 2024, "innings": 120.5, "strikeouts": 95, "era": 3.25},
]


def _find_by_id(items: list[dict], id: int) -> dict | None:
    """Look up an item by id in a list of dicts. Returns None if not found."""
    return next((x for x in items if x.get("id") == id), None)


def find_player(players: list[dict], id: int) -> dict | None:
    """Find a player by id in the given list. Returns None if not found."""
    return _find_by_id(players, id)


def _player_with_relations(player: dict) -> dict:
    """Enrich player dict with nested manager and team objects when manager_id/team_id are set."""
    out = dict(player)
    if player.get("manager_id") is not None:
        m = _find_by_id(MANAGERS, player["manager_id"])
        out["manager"] = m if m else None
    if player.get("team_id") is not None:
        t = _find_by_id(TEAMS, player["team_id"])
        out["team"] = t if t else None
    return out


def _get_player_by_id(id: int) -> dict | None:
    """Simulated slow lookup. Do not remove the delay."""
    time.sleep(2)
    return find_player(PLAYERS, id)


@app.exception_handler(Exception)
async def handle_exception(request: Request, exc: Exception):
    """Catch unhandled exceptions: re-raise HTTPException, log others and return 500."""
    if isinstance(exc, HTTPException):
        raise exc
    logger.exception("Unhandled: %s", exc)
    return JSONResponse(status_code=500, content={"error": "Something went wrong"})


@app.get("/v1/players")
def get_players(  # List players; optional sort, pagination; admin sees full objects, non-admin only firstName
    isAdmin: str | None = Query(None, alias="isAdmin"),
    sort: str | None = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    if isAdmin not in ("true", "false"):
        logger.warning("Invalid isAdmin: %s", isAdmin)
        raise HTTPException(400, "isAdmin must be 'true' or 'false'")
    if sort and sort not in ("weight", "height"):
        logger.warning("Invalid sort: %s", sort)
        raise HTTPException(400, "sort must be 'weight' or 'height'")

    players = sorted(PLAYERS, key=lambda p: p.get(sort, 0)) if sort else list(PLAYERS)
    total = len(players)
    start = (page - 1) * limit
    slice_players = players[start : start + limit]
    if isAdmin == "true":
        data = slice_players
    else:
        data = [{"firstName": p["firstName"]} for p in slice_players]
    return {"players": data, "page": page, "limit": limit, "total": total}


@app.get("/v1/players/{id}")
def get_player_by_id(id: int):  # Get single player by id (cached); includes manager and team when set
    if id in _player_cache:
        return _player_with_relations(_player_cache[id])
    player = _get_player_by_id(id)
    if not player:
        raise HTTPException(404, "Not found")
    _player_cache[id] = player
    return _player_with_relations(player)


@app.get("/v1/players/{id}/batting")
def get_player_batting(id: int):
    player = find_player(PLAYERS, id)
    if not player:
        raise HTTPException(404, "Not found")
    stats = [s for s in BATTING_STATS if s.get("player_id") == id]
    return {"player_id": id, "batting": stats}


@app.get("/v1/players/{id}/fielding")
def get_player_fielding(id: int):  # Get fielding stats for a player
    player = find_player(PLAYERS, id)
    if not player:
        raise HTTPException(404, "Not found")
    stats = [s for s in FIELDING_STATS if s.get("player_id") == id]
    return {"player_id": id, "fielding": stats}


@app.get("/v1/players/{id}/pitching")
def get_player_pitching(id: int):  # Get pitching stats for a player
    player = find_player(PLAYERS, id)
    if not player:
        raise HTTPException(404, "Not found")
    stats = [s for s in PITCHING_STATS if s.get("player_id") == id]
    return {"player_id": id, "pitching": stats}


@app.post("/v1/players", status_code=201)
def post_player(body: Player):
    global _next_id
    player = {"id": _next_id, **body.model_dump(exclude={"id"})}
    _next_id += 1
    PLAYERS.append(player)
    return player


@app.patch("/v1/players/{id}")
def patch_player(id: int, body: UpdatePlayer):  # Partial update; invalidates cache for this player
    player = find_player(PLAYERS, id)
    if not player:
        raise HTTPException(404, "Not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        if v is not None:
            player[k] = v
    if id in _player_cache:
        del _player_cache[id]
    return player
