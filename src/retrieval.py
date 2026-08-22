"""Finds relevant clauses from the manual."""
import re


def load_clauses(manual_path):
    """Split the manual into clauses keyed by their § number.
    Returns a list of dicts: {"section": "4.3.2", "text": "..."}."""
    text = open(manual_path, encoding="utf-8").read()
    lines = text.splitlines()

    clauses = []
    current = None
    for line in lines:
        # a clause starts with a bold number like **4.3.2** or **1.4.6 Applicant**
        m = re.match(r"\*\*(\d+(?:\.\d+)+)\*\*", line)
        if m:
            if current:
                clauses.append(current)
            section = m.group(1)
            current = {"section": section, "text": line}
        elif current:
            current["text"] += " " + line.strip()
    if current:
        clauses.append(current)
    return clauses


def search(question, clauses, top_k=5):
    """Return the top_k clauses whose text best matches the question words."""
    q_words = set(re.findall(r"[a-z]+", question.lower()))

    scored = []
    for c in clauses:
        c_words = re.findall(r"[a-z]+", c["text"].lower())
        overlap = 0
        for w in c_words:
            if w in q_words:
                overlap += 1
        if overlap > 0:
            scored.append((overlap, c))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:top_k]]