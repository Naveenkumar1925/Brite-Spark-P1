# DECISIONS

Written as I go, not reconstructed at the end.

## Stack
- Python. Best retrieval/LLM tooling and the language.
- CLI only — interface quality is not assessed on this problem.

## Architecture
- Four separable modules: retrieval, answer, refusal, llm.
- Reason: the day-two change will move ONE of these. Keeping them
  separate means one can change without rewriting the others.
- The model sits behind a single `llm.generate()` seam so it can be
  swapped (offline <-> API) without touching the rest.

## Corpus findings
- Checked all cross-references and day-counts programmatically, not by eye.
- Exactly one contradiction: §4.3.2 (report within 10 days) vs §9.1.4
  ("the 30 days required under §4.3").
- Exactly one apparent gap: full-time students — defined (§1.4.6),
  signposted (§3.2.3, §5.2.3, §7.1.3), never actually ruled on. The
  §7.1.3 -> §5.4 reference is broken (§5.4 is care allowances); that
  broken reference is the mechanism of the gap, not a separate flaw.
- No third flaw found.

## Model
- Starting with an API model to get the floor working fast.
- Behind one llm.generate() seam, so switching to an offline local model
  later needs no change to retrieval / answer / refusal.

  - API choice: Google Gemini (free tier). No card needed, generous limits,
  and gemini-3.6-flash is plenty for grounded Q&A on a small manual.
  Chosen over OpenAI/Anthropic (paid, no free tier) to stay zero-cost.
- Offline is the end goal (no key dependency, no token limits).

## Retrieval — why hybrid
- Started with keyword search because it's simplest, needs no downloads,
  and works offline. Wanted the floor running before adding anything heavy.
- Keyword search FAILED on realistic questions. Example: asked "what is the
  resource limit", but the manual says "resources exceed $4,000" and never
  uses the word "limit". Keyword matches exact words, not meaning, so it
  missed the one clause that answered the question.
- Why this matters: real caseworkers won't use the manual's exact wording.
  A system that only works when the question copies the manual is useless.
  The rubric asks for handling "the ugly inputs, not just the happy path".
- So added semantic search (all-MiniLM-L6-v2): it matches by MEANING, so
  "resource limit" now finds "resources exceed $4,000".
- Kept keyword too, blended 70% semantic / 30% keyword. Reason for keeping
  keyword: it catches exact terms semantic can miss — clause numbers like
  §4.3.2, form names, specific dollar figures. Together they cover both
  meaning and exact matches.
- This is NOT over-building: the floor (grounded answers) genuinely did not
  work without semantic search. We added it because it was needed, not to
  look clever. Everything above the floor is still being held back.
- Cost: the embedding model downloads ~90MB on first run (documented in
  README). Accepted because retrieval accuracy is core to the floor.
