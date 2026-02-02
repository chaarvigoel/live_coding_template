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

class UpdateIncident(BaseModel):
    status: str | None = None
    severity: str | None = None

VALID_STATUS = ("open", "triaged", "resolved")
VALID_SEVERITY = ("low", "medium", "high", "critical")


_next_id = 4
INCIDENTS: list[dict] = [
    {"id": 1, "reporter": {"firstName": "Alice", "lastName": "Anderson", "email": "alice@example.com"}, "status": "open", "severity": "medium"},
    {"id": 2, "reporter": {"firstName": "Bob", "lastName": "Brown", "email": "bob@corp.com"}, "status": "open", "severity": "low"},
    {"id": 3, "reporter": {"firstName": "Carol", "lastName": "Clark", "email": "carol@acme.org"}, "status": "open", "severity": "high"},
]


@app.get("/v1/incidents")
def get_incidents(includePII: str, severity: str | None = None):
    if includePII not in ("true", "false"):
        raise HTTPException(400, "includePII must be 'true' or 'false'")
    if severity is not None and severity not in VALID_SEVERITY:
        raise HTTPException(400, "severity must be low, medium, high, or critical")
    incidents = INCIDENTS
    if severity is not None:
        incidents = [i for i in incidents if i.get("severity") == severity]
    if includePII == "true":
        data = incidents
    else:
        data = [
            {"id": i["id"], "reporter": {"firstName": i["reporter"]["firstName"]}, "status": i.get("status", "open"), "severity": i.get("severity")}
            for i in incidents
        ]
    return {"incidents": data}

@app.post("/v1/incidents", status_code=201)
def create_incident(body: CreateIncident):
    global _next_id
    new_incident = {"id": _next_id, **body.model_dump(exclude={"id"}), "status": "open"}
    _next_id += 1
    INCIDENTS.append(new_incident)
    return new_incident


def find_incident(incidents: list[dict], id: int) -> dict | None:
    return next((x for x in incidents if x.get("id") == id), None) 

@app.patch("/v1/incidents/{id}", status_code=200)
def patch_incident(id: int, body: UpdateIncident):
    incident = find_incident(INCIDENTS, id)
    if not incident:
        raise HTTPException(404, "incident id not found")
    if body.status is not None:
        if body.status not in VALID_STATUS:
            raise HTTPException(400, "status must be open, triaged, or resolved")
        incident["status"] = body.status
    return incident



