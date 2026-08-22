"""CLI entry point.
- Run with a question:  python -m src.main "your question"
- Run with nothing:     python -m src.main   (starts an interactive loop)

Each question is answered independently. No memory between questions
(the spec does not require multi-turn conversation)."""
import sys

from src.retrieval import load_clauses, search
from src.answer import build_answer
from src.refusal import is_refusal, refusal_message

MANUAL_PATH = "data/policy-manual.md"


def ask(question, clauses):
    """Answer one question (or refuse). clauses are passed in so we
    don't reload/re-embed the manual for every question."""
    found = search(question, clauses)
    raw = build_answer(question, found)
    if is_refusal(raw):
        return refusal_message(question)
    return raw


def interactive_loop(clauses):
    """Let the user type questions one after another. Type 'quit' to exit."""
    print("Grounded Answer assistant. Type a question, or 'quit' to exit.\n")
    while True:
        question = input("Question: ").strip()
        if question.lower() in ("quit", "exit", "q", ""):
            print("Goodbye, Thank for your time in for testing my prototype.")
            break
        print("\n" + ask(question, clauses) + "\n")


if __name__ == "__main__":
    # Load and embed the manual ONCE, up front.
    print("Loading manual...")
    clauses = load_clauses(MANUAL_PATH)

    if len(sys.argv) >= 2:
        # single question mode
        print(ask(sys.argv[1], clauses))
    else:
        # interactive mode
        interactive_loop(clauses)