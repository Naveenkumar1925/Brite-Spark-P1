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
```bash
# 1. clone
git clone https://github.com/Naveenkumar1925/Brite-Spark-P1.git
cd Brite-Spark-P1

# 2. create environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. install dependencies
pip install -r requirements.txt
```
