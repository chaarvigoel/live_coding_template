## Live coding template

### Setup
python -m venv .venv
source .venv/bin/activate
pip install -U pip pytest ruff black

### Run
python src/main.py

### Test
pytest -q

### Lint/Format
ruff check .
black .
