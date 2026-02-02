# security_analyst

```bash
cd security_analyst && python -m venv .venv && source .venv/bin/activate
pip install -e . && pip install pytest
pytest
uvicorn src.main:app --reload
```
