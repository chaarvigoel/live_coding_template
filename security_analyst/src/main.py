"""Security analyst application."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Reporter(BaseModel):
    firstName: str
    lastName: str
    email: str


class CreateIncident(BaseModel):
    reporter: Reporter


_next_id = 4
INCIDENTS: list[dict] = [
    {"id": 1, "reporter": {"firstName": "Alice", "lastName": "Anderson", "email": "alice@example.com"}},
    {"id": 2, "reporter": {"firstName": "Bob", "lastName": "Brown", "email": "bob@corp.com"}},
    {"id": 3, "reporter": {"firstName": "Carol", "lastName": "Clark", "email": "carol@acme.org"}},
]


@app.get("/v1/incidents")
def get_incidents(includePII: str):
    if includePII not in ("true", "false"):
        raise HTTPException(400, "includePII must be 'true' or 'false'")
    if includePII == "true":
        data = INCIDENTS
    else:
        data = [{"id": i["id"], "reporter": {"firstName": i["reporter"]["firstName"]}} for i in INCIDENTS]
    return {"incidents": data}


@app.post("/v1/incidents", status_code=201)
def create_incident(body: CreateIncident):
    global _next_id
    new_incident = {"id": _next_id, **body.model_dump(exclude={"id"})}
    _next_id += 1
    INCIDENTS.append(new_incident)
    return new_incident

