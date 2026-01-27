import json
from pathlib import Path


def parse_config(path: str) -> dict:
    if not Path(path).exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)
