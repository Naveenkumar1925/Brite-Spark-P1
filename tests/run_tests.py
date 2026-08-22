"""Runnable 10-question test set for the Grounded Answer assistant.

Each question has an expected behaviour:
  - "answer"  -> the manual covers it; we expect a grounded answer
  - "refuse"  -> the manual does not settle it; we expect a refusal

Run:  python -m tests.run_tests

Honesty note: a test set where everything passes means the questions were
too easy. Failures here are reported, not hidden.
"""
import time

from src.retrieval import load_clauses
from src.main import ask
from src.refusal import refusal_message

MANUAL_PATH = "data/policy-manual.md"

# (question, expected behaviour, note about why this question is here)
TESTS = [
    ("What is the resource limit for a household?", "answer",
     "straightforward - §2.4.1"),
    ("How long do I have to request a review of a decision?", "answer",
     "straightforward - §11.1.2"),
    ("Can I be eligible if I am 17 years old?", "answer",
     "tricky - under-18 rule §2.3.1"),
    ("What income is disregarded when calculating my award?", "answer",
     "list-style - §6.4.1"),
    ("How is a full-time student's award calculated?", "refuse",
     "PLANTED GAP - looks covered, is not"),
    ("Am I eligible if I own a pet?", "refuse",
     "genuinely not in the manual"),
    ("Can I apply for assistance if I live in a different county?", "refuse",
     "not covered - out of scope"),
    ("How many days do I have to report a change of circumstances?", "answer",
     "CONTRADICTION - §4.3.2 (10) vs §9.1.4 (30); watch what it does"),
    ("What happens to my award if I go to prison?", "answer",
     "covered - excluded person §4.1.1(b)"),
    ("Can someone else attend my interview with me?", "answer",
     "covered - §8.5.3"),
]


def behaviour_of(result):
    """Classify a result as 'refuse' or 'answer'."""
    if result.strip() == refusal_message("").strip():
        return "refuse"
    return "answer"


def main():
    print("Loading manual...\n")
    clauses = load_clauses(MANUAL_PATH)

    passed = 0
    for i, (question, expected, note) in enumerate(TESTS, 1):
        result = ask(question, clauses)
        actual = behaviour_of(result)
        ok = (actual == expected)
        if ok:
            passed += 1

        print(f"Q{i}: {question}")
        print(f"    why tested : {note}")
        print(f"    expected   : {expected}")
        print(f"    actual     : {actual}   {'PASS' if ok else 'FAIL'}")
        print(f"    response   : {result.strip()[:160]}")
        print()

        time.sleep(13)   # stay under 5 requests/minute on free tier

    print(f"RESULT: {passed}/{len(TESTS)} matched expectation.")
    print("(Note: a 'FAIL' here is useful information, not hidden.)")


if __name__ == "__main__":
    main()