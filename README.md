# The Grounded Answer — Brite Spark 2026, Problem 1

A command-line assistant that answers questions from the Calder County
Household Support Program policy manual. Every answer cites the exact
clause (§) it used. When the manual does not settle a question, the
assistant refuses and says who to ask instead.

No web UI — a CLI is the expected delivery for this problem.

## What it does
- Answers policy questions grounded in the manual, with clause-level citations.
- Refuses when the manual does not cover the question (or covers it ambiguously).
- Ships with a 10-question test set and honest pass/fail results.

## Setup

1. Clone and enter the project:
```bash
   git clone https://github.com/Naveenkumar1925/Brite-Spark-P1.git
   cd Brite-Spark-P1
```

2. Create and activate a virtual environment:
```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Mac/Linux:
   source .venv/bin/activate
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

4. Set your Gemini API key. Create a file named `.env` in the project root
   with this one line (get a free key at https://aistudio.google.com/apikey):
   Then create a file named `.env` in the project root containing this one line:
```
   GEMINI_API_KEY=your_key_here
```
