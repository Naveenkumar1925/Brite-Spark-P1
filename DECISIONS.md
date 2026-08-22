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

