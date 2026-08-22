"""Builds a grounded answer from retrieved clauses. Cites the § used."""
from src.llm import generate


PROMPT = """You are a policy assistant for the Calder County Household Support Program.
Answer the question using ONLY the clauses provided below.

Rules:
- Use only the information in these clauses. Do not use any outside knowledge.
- Every claim must come from a clause. Cite the clause number like (§4.3.2).
- If the clauses do not contain the answer, say exactly: NOT_IN_MANUAL
- Keep the answer short and in plain language.

CLAUSES:
{clauses}

QUESTION: {question}

ANSWER:"""


def build_answer(question, clauses):
    """Return a grounded answer string that cites the § clauses used."""
    parts = []
    for c in clauses:
        parts.append(f"§{c['section']}: {c['text']}")
    clause_text = "\n\n".join(parts)
    prompt = PROMPT.format(clauses=clause_text, question=question)
    return generate(prompt)