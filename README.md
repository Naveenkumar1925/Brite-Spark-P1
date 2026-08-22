# The Grounded Answer — Brite Spark 2026, Problem 1

A command-line assistant that answers questions from the Calder County
Household Support Program policy manual. Every answer cites the exact clause
(§) it used. When the manual does not cover a question, the assistant refuses
and points the user to a supervisor — instead of guessing.

No web UI — a CLI is the expected delivery for this problem.

---

## Table of contents
1. What it does
2. Requirements
3. Setup (step by step)
4. How to run
5. How to run the tests
6. What each file does
7. How the system works
8. Known limits

---

## 1. What it does

- Answers policy questions grounded in the manual, with clause-level citations.
- Refuses when the manual does not settle the question, and says who to ask.
- Ships with a runnable 10-question test set and honest pass/fail results.

---

## 2. Requirements

- Python 3.10 or newer
- An internet connection (for the Gemini API, and a one-time model download)
- A free Google Gemini API key: https://aistudio.google.com/apikey

All Python dependencies are listed in `requirements.txt` and installed in
step 3 below.

---

## 3. Setup (step by step)

**Step 1 — Clone and enter the project:**
```bash
git clone https://github.com/Naveenkumar1925/Brite-Spark-P1.git
cd Brite-Spark-P1
```

**Step 2 — Create and activate a virtual environment:**
```bash
python -m venv .venv
```
```bash
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
```
After activating, your prompt should show `(.venv)`.

**Step 3 — Install dependencies:**
```bash
pip install -r requirements.txt
```
This installs the Gemini client, the embedding model library, and helpers.
It may take a few minutes (one dependency, torch, is large).

**Step 4 — Set your Gemini API key. Create a file named `.env` in the project root**
   with this one line (get a free key at https://aistudio.google.com/apikey):
   Then create a file named `.env` in the project root containing this one line:
```
   GEMINI_API_KEY=your_key_here
```

The `.env` file is private and is never committed to the repository.

---

## 5. How to run

**Ask a single question:**
```bash
python -m src.main "What is the resource limit for a household?"
```
Expected: an answer citing §2.4.1 ($4,000).

**Ask a question the manual does not cover (see the refusal):**
```bash
python -m src.main "How is a full-time student's award calculated?"
```
Expected: a refusal that points the user to a supervisor.

**Interactive mode** (ask many questions in a row, type `quit` to exit):
```bash
python -m src.main
```

**Note:** on the first run only, a small embedding model (~90MB,
all-MiniLM-L6-v2) downloads automatically. This needs internet once; after
that it is cached locally.

---

## 6. How to run the tests

The project ships with a 10-question test set that checks both answering and
refusing, and prints honest pass/fail results.

**Run the test set:**
```bash
python -m tests.run_tests
```
It runs each of the 10 questions, classifies the result as an answer or a
refusal, and compares it to what was expected. It prints a PASS/FAIL line per
question and a final score. (There is a short pause between questions to stay
inside the Gemini free-tier rate limit, so it takes about two minutes.)

The questions and the honest results are also documented in
`tests/test_questions.md`.

---


---

## 7. How the system works

One question flows through four steps:

1. **Retrieval** (`retrieval.py`) — the manual is split into clauses, each
   keyed by its § number. For a question, it scores every clause by a blend
   of semantic similarity (meaning) and keyword overlap (exact terms like
   clause numbers), and returns the top matches.
2. **Answer** (`answer.py`) — the top clauses are given to the model with a
   strict instruction: answer using only these clauses, cite the § used, and
   if they do not contain the answer, say so.
3. **Refusal** (`refusal.py`) — if the answer step could not ground an answer,
   this returns a helpful refusal that points the user to a supervisor.
4. **CLI** (`main.py`) — ties it together and prints the answer or refusal.

The four steps are kept separate on purpose, so any one of them can change
without rewriting the others.

---

## 8. Known limits

These are documented honestly in `DECISIONS.md` and `tests/test_questions.md`:

- The refusal threshold currently leans cautious, so it can refuse a few
  questions the manual actually answers (false refusals).
- It does not yet detect internal contradictions in the manual — it will
  answer one side confidently.
- It uses an online API model (Gemini). The model call is isolated in
  `src/llm.py` so it can be swapped for an offline model later.
