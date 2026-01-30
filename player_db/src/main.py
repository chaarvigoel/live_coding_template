import logging

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        raise exc
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"error": "Something went wrong"},
    )


# --- Player models ---
class CreatePlayerBody(BaseModel):
    """Request body for POST /v1/players."""

    firstName: str
    lastName: str
    weight: int = Field(ge=1, le=500)
    height: int = Field(ge=1, le=300)


class Player(BaseModel):
    """Full player (stored and returned)."""

    firstName: str
    lastName: str


# In-memory store with id
PLAYERS: list[dict[str, str]] = [
    {"firstName": "Alice", "lastName": "Anderson"},
    {"firstName": "Bob", "lastName": "Brown"},
    {"firstName": "Carol", "lastName": "Clark"},
]

def add_player(firstName: str, lastName: str):
    new_player = Player(firstName=firstName, lastName=lastName)
    PLAYERS.append(new_player.model_dump())

    


@app.get("/v1/players")
def get_players(isAdmin: str | None = Query(None, alias="isAdmin")):
    if isAdmin not in {"true", "false"}:
        logger.warning("Invalid isAdmin param: %s", isAdmin)
        raise HTTPException(status_code=400, detail="isAdmin parameter must be 'true' or 'false'")
    
    try:
        if isAdmin == "true":
            return {"players": PLAYERS}
        return {"players": [{"firstName": p["firstName"]} for p in PLAYERS]}
    except Exception as e:
        logger.exception("Unexpected error in get_players: %s", e)
        return JSONResponse(
            status_code=500,
            content={"error": "Something went wrong"},
        )
