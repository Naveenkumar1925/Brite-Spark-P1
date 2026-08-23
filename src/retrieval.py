"""Finds relevant clauses from the manual. No answering, no refusing.
Hybrid search: keyword (exact words) + semantic (meaning), combined."""
import re
import torch

from sentence_transformers import SentenceTransformer, util

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


def _load_stopwords():
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

# Load the embedding model once (downloads ~90MB the first time).
_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def _parse_clauses(text, source):
    """Split one document's text into clauses keyed by § number.
    'source' records where each clause came from (manual or amendment)."""
    lines = text.splitlines()
    clauses = []
    current = None
    for line in lines:
        m = re.match(r"\*\*(\d+(?:\.\d+)+)", line)   # matches **4.3.2** or **4.3.2 Title**
        if m:
            if current:
                clauses.append(current)
            current = {"section": m.group(1), "text": line, "source": source}
        elif current:
            current["text"] += " " + line.strip()
    if current:
        clauses.append(current)
    return clauses


def load_clauses(manual_path, amendment_path=None):
    """Load clauses from the manual, and (if given) the amendment.
    Each clause carries its source. Amendment clauses are tagged so the
    answer step can apply the version in force on the claim's date.
    Also pre-computes a semantic embedding for each clause."""
    text = open(manual_path, encoding="utf-8").read()
    clauses = _parse_clauses(text, source="manual")

    if amendment_path:
        amend_text = open(amendment_path, encoding="utf-8").read()
        amend_clauses = _parse_clauses(amend_text, source="amendment-2026-01")
        clauses += amend_clauses

    # embed every clause once, up front
    texts = []
    for c in clauses:
        texts.append(c["text"])
    embeddings = _MODEL.encode(texts, convert_to_tensor=True)
    for c, emb in zip(clauses, embeddings):
        c["embedding"] = emb

    return clauses


def _keyword_scores(question, clauses):
    """Score each clause by how many non-filler question words it contains,
    normalised to 0..1."""
    q_words = set(re.findall(r"[a-z]+", question.lower())) - STOPWORDS
    scores = []
    for c in clauses:
        c_words = re.findall(r"[a-z]+", c["text"].lower())
        overlap = 0
        for w in c_words:
            if w in q_words:
                overlap += 1
        scores.append(overlap)
    if scores:
        top = scores[0]
        for s in scores:
            if s > top:
                top = s
    else:
        top = 0
    if top == 0:
        return [0.0] * len(clauses)
    normalized = []
    for s in scores:
        normalized.append(s / top)
    return normalized


def search(question, clauses, top_k=10):
    """Return the top_k clauses by a blend of keyword and semantic match."""
    # semantic scores (0..1)
    q_emb = _MODEL.encode(question, convert_to_tensor=True)
    emb_list = []
    for c in clauses:
        emb_list.append(c["embedding"])
    clause_embs = torch.stack(emb_list)
    sem = util.cos_sim(q_emb, clause_embs)[0]
    sem_scores = []
    for s in sem:
        sem_scores.append(float(s))

    # keyword scores (0..1)
    kw_scores = _keyword_scores(question, clauses)

    # blend: semantic leads, keyword boosts exact-term matches
    blended = []
    for c, sem_s, kw_s in zip(clauses, sem_scores, kw_scores):
        score = 0.7 * sem_s + 0.3 * kw_s
        blended.append((score, c))

    blended.sort(key=lambda x: x[0], reverse=True)
    top_results = []
    for score, c in blended[:top_k]:
        top_results.append(c)
    return top_results