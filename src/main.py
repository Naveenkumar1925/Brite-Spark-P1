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
    """Answer one question (or refuse), with source clauses shown."""
    found = search(question, clauses, top_k=8)
    raw = build_answer(question, found)

    if is_refusal(raw):
        return refusal_message(question)

    # find which § numbers the answer cited, and show their source text
    import re
    cited = re.findall(r"§\s?(\d+(?:\.\d+)+)", raw)
    seen = []
    sources = []
    for section in cited:
        if section in seen:
            continue
        seen.append(section)
        for c in clauses:
            if c["section"] == section:
                # strip the leading bold number from the stored text
                text = re.sub(r"^\*\*[\d.]+\*\*\s*", "", c["text"]).strip()
                sources.append(f"§{section}: {text}")
                break

    if sources:
        return raw + "\n\nSources:\n" + "\n".join(sources)
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