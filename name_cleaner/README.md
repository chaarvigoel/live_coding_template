# name_cleaner

### Setup
```bash
cd name_cleaner
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -U pip pytest ruff black
```

### Run
```bash
python src/main.py
```

### Test
```bash
pytest -q
```

### Lint / Format
```bash
ruff check .
black .
```
