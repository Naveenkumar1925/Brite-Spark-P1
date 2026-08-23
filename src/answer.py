"""Builds a grounded answer from retrieved clauses, correct for a claim date.
Cites the § used, and applies Amendment 2026-01 with its transitional rules."""
from src.llm import generate


PROMPT = """You are a policy assistant for the Calder County Household Support Program.
Answer the question using ONLY the clauses provided below.

The claim being asked about is dated: {claim_date}

Some clauses are from the base manual (as at 31 December 2025) and some are
from Amendment 2026-01, which takes effect on 1 March 2026. A clause's source
is shown in square brackets after its number, e.g. [amendment-2026-01].

How to choose which version applies:
- The amendment's changes to earnings disregard, income thresholds, and
  sanctions apply to any DETERMINATION made on or after 1 March 2026,
  including for an earlier period. Treat the claim date as the determination
  date for this purpose.
- The amendment's change to the reporting deadline for a change of
  circumstances applies ONLY where the change of circumstances OCCURRED on or
  after 1 March 2026. If the change occurred before 1 March 2026, the old
  reporting deadline still applies, no matter when the decision is made.
- For a claim dated before 1 March 2026, use the base manual figures.
- For a claim dated on or after 1 March 2026, use the amended figures
  (subject to the reporting-deadline rule above).

Rules:
- Use only the information in these clauses. Do not use outside knowledge.
- Every claim must come from a clause. Cite the clause number like (§4.3.2).
- State which version you applied and why, given the claim date.
- If the clauses do not contain the answer, say exactly: NOT_IN_MANUAL
- If two clauses genuinely conflict AND the amendment does not resolve the
  conflict for this claim date, do not pick one silently: state the
  inconsistency and show both with citations.
- Keep the answer short and in plain language.

CLAUSES:
{clauses}

QUESTION: {question}

ANSWER:"""


def build_answer(question, clauses, claim_date):
    """Return a grounded answer, correct for the given claim date."""
    parts = []
    for c in clauses:
        source = c.get("source", "manual")
        tag = "" if source == "manual" else f" [{source}]"
        parts.append(f"§{c['section']}{tag}: {c['text']}")
    clause_text = "\n\n".join(parts)

    prompt = PROMPT.format(
        clauses=clause_text,
        question=question,
        claim_date=claim_date,
    )
    return generate(prompt)