"""Finds relevant clauses from the manual."""
import re
# A solid fallback list, used if nltk is unavailable (keeps clean clone safe).
_FALLBACK_STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "for", "of", "to", "in", "on", "at", "by", "and", "or", "but", "if",
    "then", "so", "as", "from", "with", "without", "within", "into", "onto",
    "this", "that", "these", "those", "it", "its", "they", "them", "their",
    "he", "she", "his", "her", "i", "me", "my", "we", "us", "our", "you",
    "your", "what", "which", "who", "whom", "whose", "how", "when", "where",
    "why", "does", "do", "did", "done", "can", "could", "may", "might",
    "must", "shall", "should", "will", "would", "have", "has", "had",
    "not", "no", "yes", "any", "all", "some", "such", "than", "there",
    "here", "about", "over", "under", "up", "down", "out", "off",
}

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
    q_words = set(re.findall(r"[a-z]+", question.lower())) - STOPWORDS

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

def _load_stopwords():
    """Use nltk's standard English stopwords; fall back to the built-in
    list if nltk (or its data) isn't available."""
    try:
        import nltk
        from nltk.corpus import stopwords
        try:
            return set(stopwords.words("english"))
        except LookupError:
            nltk.download("stopwords", quiet=True)
            return set(stopwords.words("english"))
    except Exception:
        return _FALLBACK_STOPWORDS


STOPWORDS = _load_stopwords()