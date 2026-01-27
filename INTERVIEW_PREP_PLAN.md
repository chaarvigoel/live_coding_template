# 1-Week Cursor + Live Coding Interview Prep

**Goal:** Feel confident using Cursor as your IDE and AI pair programmer, and articulate how you use it—before and during your Monday live coding session.

---

## Clarifications to lock in

- **Which Monday?** If it’s *this* Monday (e.g. Jan 27), treat this as a **2–3 day intensive**: do Day 1 → Day 6 → Day 7, and skim the rest. If it’s *next* Monday (e.g. Feb 2), follow the full week.
- **Language?** This plan assumes Python (your template). Adjust examples if you’ll use something else.
- **Problem type?** “Open-ended” often means a small app (CLI, API, script). We’ll practice that.

---

## Cursor essentials (learn these first)

### Must-know shortcuts (macOS)

| Shortcut | What it does |
|----------|----------------|
| **⌘L** | Open **Chat** – ask questions, get code, explain things |
| **⌘K** | **Inline edit** – select code, describe change, apply in place |
| **⌘I** | **Composer** – multi-file edits, “build X” from a prompt |
| **Tab** | Accept **Ghost AI** suggestion (gray inline completions) |
| **Esc** | Dismiss suggestion |
| **⌘⇧P** | Command palette – run any Cursor/VS Code command |

### Core Cursor concepts

1. **Chat (⌘L)**  
   - Use for: design questions, “how do I…?”, “explain this”, “write a function that…”, debugging.  
   - You can @-mention files (`@src/main.py`) or symbols so the AI has context.

2. **Inline edit (⌘K)**  
   - Select code → ⌘K → natural language instruction → accept or tweak.  
   - Great for refactors, adding error handling, renaming, adding tests.

3. **Composer (⌘I)**  
   - Describe a bigger change (“add a CLI that reads a config file and…”).  
   - Cursor can create/edit multiple files. Review each diff before accepting.

4. **Ghost / Tab completion**  
   - Gray text as you type. Tab to accept. Use for boilerplate, obvious next steps.

---

## Day-by-day plan

### **Day 1: Cursor as an IDE**

**Focus:** Feel at home in Cursor (it’s VS Code under the hood).

- [ ] Open your `live_coding_template` in Cursor.
- [ ] Confirm: terminal (`` Ctrl+` ``), file explorer, run `python src/main.py`, then `pytest -q`.
- [ ] Use **⌘P** to open `main.py` and `test_smoke.py` by name.
- [ ] Use **⌘L** → ask: *“How do I run pytest from the project root?”* – run what it suggests.
- [ ] **Small task:** In Chat, ask: *“Add a `greet(name: str) -> str` in `src/main.py` that returns `'Hello, {name}!'`, and call it from `main()`.”* Apply the change, run `main`, run tests.
- [ ] **Goal:** You’ve used Chat once, run code, run tests. No Composer yet.

**~60–90 min**

---

### **Day 2: Chat + inline edit (⌘K)**

**Focus:** Use Chat for design + implementation; use ⌘K for quick, localized edits.

- [ ] **Chat:** "Add a `src/utils.py` with a `parse_config(path: str) -> dict` that reads a JSON file. Use it from `main()` to print a `message` key if present."
- [ ] **⌘K:** In `utils.py`, select `parse_config` → ⌘K → *"Add a check: if the file doesn't exist, return `{}`."*
- [ ] **⌘K:** In `test_smoke.py`, add a test for `greet` or `parse_config` via ⌘K.
- [ ] Run `pytest -q` and fix any failures (use Chat: "this test fails because…").
- [ ] **Goal:** You're comfortable with Chat for "build this" and ⌘K for "change this selection."

**~90 min**

---

### **Day 3: Composer for multi-file work**

**Focus:** Use Composer for a single, coherent feature that touches 2+ files.

- [ ] **Composer (⌘I):** "Add a minimal CLI: `python -m src.main --config path/to/config.json`. Use `argparse`. Keep `main()` as the entry point. Add a test that runs the CLI with a temp config and checks stdout."
- [ ] Review each file Composer creates/edits. Accept or adjust.
- [ ] Run the CLI and tests. Fix issues via Chat or ⌘K.
- [ ] **Goal:** You can drive a small, multi-file change with Composer and sanity-check the result.

**~90 min**

---

### **Day 4: Problem-solving + structure**

**Focus:** Open-ended "build a small thing" with clear structure and some design discussion.

- [ ] Pick a **tiny** project, e.g.:
  - "CLI tool that reads a CSV, filters rows by a column value, and writes result to a new CSV."
  - "Simple stats module: `mean`, `median`, `stddev` over a list of numbers, plus tests."
- [ ] **Before coding:** Write 2–3 bullet points (structure: modules, entrypoint, tests). Say them out loud as if to an interviewer.
- [ ] Implement using Chat/Composer/⌘K. Keep functions small, names clear.
- [ ] Add 2–3 tests. Run lint/format (`ruff check .`, `black .`).
- [ ] **Goal:** You can sketch structure, implement with Cursor, and keep code tidy.

**~2 hours**

---

### **Day 5: "With vs without AI"**

**Focus:** Practice explaining *when* and *why* you use AI—exactly what the interview wants.

- [ ] **Part A – Without AI:** Implement something small (e.g. "reverse words in a string" or "parse a simple key=value config") from scratch. No Chat, no Composer, no Tab completion if you can avoid it. Time yourself.
- [ ] **Part B – With AI:** Do a *different* but similar-sized task (or the same one in a new branch) using Chat/Composer/⌘K. Time yourself.
- [ ] **Reflect:** What was faster? What did you double-check when using AI? What would you *not* delegate to AI in an interview?
- [ ] **Script 2–3 lines** you could say in the interview, e.g.:
  - *"I use Cursor's AI for boilerplate and first drafts; I always review and run tests."*
  - *"I use Chat to explore design options, then implement or refine with inline edit."*
- [ ] **Goal:** You can clearly explain your "with vs without AI" workflow.

**~90 min**

---

### **Day 6: Dry run (mock interview)**

**Focus:** Simulate the real session: screen share, timer, narration.

- [ ] **Setup:** Same project layout you'll use Monday (e.g. `live_coding_template`). Close unnecessary apps. Optional: use a second device to record your screen.
- [ ] **Task:** e.g. "Add a `--verbose` flag to the CLI that logs each config key as it's read" or "Add a `stats` module with `mean`/`median` and wire it into `main`."
- [ ] **Rules:** 25–30 min. Share screen. **Talk out loud:** "First I'll add the flag in argparse… I'll use Cursor to generate the parser changes, then I'll add the logging."
- [ ] Use Chat/⌘K/Composer deliberately and **briefly say why** each time.
- [ ] Run tests and fix any failures on the fly.
- [ ] **Review:** Watch the recording. Note: too quiet? Too much AI without explanation? Any fumbling with Cursor?
- [ ] **Goal:** One full run-through that feels close to the real thing.

**~45–60 min**

---

### **Day 7: Polish and rest**

**Focus:** Fix gaps from Day 6, then dial down.

- [ ] Redo **one** weaker part of the dry run (e.g. "I hesitated on Composer" → do one more Composer task).
- [ ] Skim this doc. Re-practice the **shortcuts** (⌘L, ⌘K, ⌘I, Tab).
- [ ] **Checklist for interview:**
  - [ ] Cursor open with `live_coding_template` (or your chosen skeleton).
  - [ ] Terminal ready, venv activated, `pytest -q` runs.
  - [ ] Browser/other distractions closed; desktop clean for screen share.
  - [ ] You know what you'll say for "how I use AI" (from Day 5).
- [ ] **Goal:** Confident, rested, no last-minute tool surprises.

**~30–45 min**

---

## Interview day checklist

- [ ] **IDE:** Cursor, project open, venv activated, tests passing.
- [ ] **Screen share:** Entire screen, clear resolution; close notifications if possible.
- [ ] **Communication:** Think out loud. Say "I'm using the AI to…" or "I'll do this part myself because…".
- [ ] **AI usage:** Use it naturally, but **explain** when you prompt, accept, or reject suggestions.

---

## Quick "how I use Cursor" script

You can say something like:

> "I use Cursor as my main IDE. For this task I'll use the AI in a few ways: **Chat** when I want to explore design or get a first implementation, **inline edit** for small, targeted changes, and **Composer** if we touch multiple files. I always review the output, run tests, and fix anything that doesn't match what I want. I don't paste blindly—I treat it as a pair programmer I can redirect."

Adjust to your real habits; the key is to **show you're intentional** about when and how you use AI.

---

## If you're short on time

**Minimum viable prep:**

1. **Day 1** – Cursor basics + one Chat-driven change in your project.
2. **Day 5** – "With vs without AI" reflection + 2–3 talking points.
3. **Day 6** – One dry run with screen share and narration.

That gives you: basic Cursor fluency, a clear story about AI use, and one full practice run.

---

## Optional: practice task ideas

Use these for Day 4 or Day 6:

- **CLI:** "Filter lines of a log file by a regex and optionally write to a file."
- **Data:** "Read JSON from stdin, extract a nested key (e.g. `config.debug`), print it."
- **API-style:** "Module with `fetch_users() -> list[dict]` that reads from a JSON file (no real HTTP). Add `get_user_by_id` and tests."

Stick to **one** small, well-scoped task per practice session.

---

Good luck with your interview. Use this plan as a guide, not a rigid schedule. The aim is to be comfortable with Cursor and to clearly explain how you use AI while you code.
