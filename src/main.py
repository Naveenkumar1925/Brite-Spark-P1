"""CLI entry point.
- Run with a question:   python -m src.main "your question"
- With a claim date:     python -m src.main "your question" --date 2026-02-15
- Run with nothing:      python -m src.main   (starts an interactive loop)

Each question is answered independently. No memory between questions
(the spec does not require multi-turn conversation).

The claim date matters: Amendment 2026-01 takes effect 1 March 2026, so the
correct answer can depend on the date of the claim being asked about. If no
date is given, today's date is used.
"""
import re
import sys
from datetime import date

from src.retrieval import load_clauses, search
from src.answer import build_answer
from src.refusal import is_refusal, refusal_message

MANUAL_PATH = "data/policy-manual.md"
AMENDMENT_PATH = "data/amendment-2026-01.md"


def _attach_amendments(found, all_clauses):
    """For every retrieved clause, also include any amendment clause that
    references its section number, so the answer sees the change too."""
    found_sections = []
    for c in found:
        found_sections.append(c["section"])

    result = list(found)
    for c in all_clauses:
        if c.get("source") == "manual":
            continue  # only pull in amendment clauses
        for section in found_sections:
            if section in c["text"]:
                if c not in result:
                    result.append(c)
                break
    return result


def ask(question, clauses, claim_date):
    """Answer one question (or refuse), for a given claim date, with sources."""
    found = search(question, clauses, top_k=8)
    found = _attach_amendments(found, clauses)
    raw = build_answer(question, found, claim_date)

    if is_refusal(raw):
        return refusal_message(question)

    # find which § numbers the answer cited, and show their source text
    cited = re.findall(r"§\s?(\d+(?:\.\d+)+[A-Z]?)", raw)
    seen = []
    sources = []
    for section in cited:
        if section in seen:
            continue
        seen.append(section)
        for c in clauses:
            if c["section"] == section:
                text = re.sub(r"^\*\*[\d.A-Z]+\*\*?\s*", "", c["text"]).strip()
                tag = "" if c.get("source") == "manual" else f" [{c.get('source')}]"
                sources.append(f"§{section}{tag}: {text}")
                break

    if sources:
        return raw + "\n\nSources:\n" + "\n".join(sources)
    return raw


def interactive_loop(clauses, claim_date):
    """Let the user type questions one after another. Type 'quit' to exit."""
    print(f"Grounded Answer assistant. Claim date: {claim_date}. "
          f"Type a question, or 'quit' to exit.\n")
    while True:
        question = input("Question: ").strip()
        if question.lower() in ("quit", "exit", "q", ""):
            print("Goodbye, and thank you for testing this prototype.")
            break
        print("\n" + ask(question, clauses, claim_date) + "\n")


def parse_args(argv):
    """Pull out an optional --date YYYY-MM-DD; return (question, claim_date).
    question is None if not given (interactive mode)."""
    claim_date = date.today().isoformat()
    question = None
    args = argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--date" and i + 1 < len(args):
            claim_date = args[i + 1]
            i += 2
        else:
            question = args[i]
            i += 1
    return question, claim_date


if __name__ == "__main__":
    question, claim_date = parse_args(sys.argv)

    print("Loading manual and amendment...")
    clauses = load_clauses(MANUAL_PATH, AMENDMENT_PATH)

    if question is not None:
        print(ask(question, clauses, claim_date))
    else:
        interactive_loop(clauses, claim_date)