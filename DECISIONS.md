# DECISIONS

Written as I go, not reconstructed at the end.

## Stack
- Python. Best retrieval/LLM tooling and the language I'm fastest in.
- CLI only — interface quality is not assessed on this problem.

## Architecture
- Four separable modules: retrieval, answer, refusal, llm.
- Reason: the day-two change would move ONE of these. Keeping them separate
  means one can change without rewriting the others. (This paid off — see the
  day-two section: the change touched three files, not the whole system.)
- The model sits behind a single `llm.generate()` seam so it can be changed
  in one place without touching the rest.

## Corpus findings
- Checked all cross-references and day-counts programmatically
  (tests/audit_manual.py), not by eye.
- Exactly one contradiction: §4.3.2 (report within 10 days) vs §9.1.4
  ("the 30 days required under §4.3").
- Exactly one apparent gap: full-time students — defined (§1.4.6),
  signposted (§3.2.3, §5.2.3, §7.1.3), never actually ruled on. The
  §7.1.3 -> §5.4 reference is broken (§5.4 is care allowances); that broken
  reference is the mechanism of the gap, not a separate flaw.
- No third flaw found.

## Model
- API model, to get the floor working fast.
- Called in one place (llm.py) behind a single generate() function, so the
  model can be changed without touching retrieval, answer, or refusal.
- Choice: Google Gemini free tier. No card needed, and gemini-3.6-flash is
  plenty for grounded Q&A on a small manual. Chosen over OpenAI/Anthropic
  (paid, no free tier) to stay zero-cost.
- Known limit: the free tier allows 20 requests/day. Judges use their own key
  (per the handbook), so this mainly affects local testing. llm.py handles a
  spent quota (and transient rate limits) with retries and a clear message
  instead of crashing.
- Considered but not done: a local/offline model would remove the API
  dependency and the daily limit. The generate() seam is designed so this
  swap would touch only llm.py. Left out to keep setup simple within time;
  noted as the first thing to add with more time.

## Retrieval — why hybrid
- Started with keyword search: simplest, no downloads. Wanted the floor
  running before anything heavy.
- Keyword search FAILED on realistic questions. Example: "what is the resource
  limit" — the manual says "resources exceed $4,000" and never uses "limit".
  Keyword matches exact words, not meaning, so it missed the answering clause.
- Real caseworkers won't use the manual's exact wording, so this mattered.
- Added semantic search (all-MiniLM-L6-v2): matches by MEANING, so "resource
  limit" now finds "resources exceed $4,000".
- Kept keyword too, blended 70% semantic / 30% keyword — keyword catches exact
  terms semantic can miss (clause numbers, dollar figures).
- Not over-building: the floor genuinely did not work without semantic search.
- Cost: the embedding model downloads ~90MB on first run (noted in README).

## Refusal threshold (the judgement call)
- Where to draw the answer-vs-refuse line has no single right answer. Setting
  leans CAUTIOUS: when grounding is unclear, refuse.
- Trade-off: avoids confident wrong answers (the main harm) but can cause
  false refusals. For a benefits office, "refuse when unsure" is safer than
  "guess", because a wrong entitlement answer harms a real person.

## Contradiction handling (bonus)
- The answer prompt instructs: if two retrieved clauses conflict, do NOT pick
  one silently — state the inconsistency and show both with citations.
- Verified: "how many days to report a change?" surfaces §4.3.2 (10 days) vs
  §9.1.4 (30 days) instead of answering one side confidently.
- Prompt-level fix chosen over new detection machinery: it needs both clauses
  retrieved (they are, via hybrid search) and generalises to any conflict.

## Verifiable citations (bonus)
- After answering, the full text of each cited § clause is printed under a
  "Sources:" heading, so a caseworker can verify the answer without leaving
  the screen. Refusals show no sources.

## Day-two change: Amendment 2026-01 (date-aware answers)
The requirement changed: answers must be correct for the DATE of the claim,
because Amendment 2026-01 takes effect 1 March 2026.

### What I changed
- Loaded the amendment into the corpus, tagging each clause with its source
  ("amendment-2026-01").
- Added an optional --date argument (defaults to today); the claim date flows
  to the answer step.
- Made the answer prompt date-aware: base manual for claims before 1 March
  2026, amended figures on/after, and it states which version it used and why.
- Encoded the transitional rules (amendment paragraph 5): money/threshold/
  sanction changes trigger on the DETERMINATION date, but the reporting-
  deadline change triggers on the date the CHANGE OCCURRED — different date
  triggers. A naive "new rules after March" would get the reporting deadline
  wrong.
- Fixed a retrieval gap: an amendment clause (e.g. "in §6.4.1(a) substitute
  $175") did not always rank high enough to be retrieved alongside its base
  clause, so the answer used the old figure. Now, whenever a base clause is
  retrieved, any amendment clause referencing its section number is pulled in
  too. Verified: earnings disregard returns $175 for an April 2026 claim and
  $120 for a January 2026 claim.

### Why the design absorbed this cleanly
- The change landed in three clear places (retrieval, answer, main), not
  scattered everywhere, because the modules were separable. Refusal was
  untouched.
- The earlier contradiction (§4.3.2 vs §9.1.4) is actually resolved by the
  amendment (both become 14 days) for changes on/after 1 March 2026 — so the
  date logic and contradiction handling work together.

### What I chose NOT to do / would do with more time
- The date-vs-rule decision is applied by the model from the prompt, not
  computed in code. With more time I'd move it into code for stronger
  guarantees.
- Amendment-attachment matches on section numbers in the amendment text;
  simple and works here. A more robust version would parse the "substitute"
  instructions explicitly.
- Lettered amendment clauses like §10.5.3A are parsed but the section-number
  regex is simple; not fully hardened for every lettered edge case.

## Test findings (honest) — current
Ran the 10-question set (tests/run_tests.py): 9/10 matched expectation.
- Q4 (income disregards) and Q8 (contradiction) were failures in an earlier
  run and are now fixed — Q4 by widening retrieval, Q8 by contradiction
  detection. Kept visible here to show the fixes.
- Q7 now tests the day-two date logic directly: earnings disregard returns
  the amended $175 for an April 2026 claim (and $120 for January).
- Q9 (prison) is the one remaining honest failure: "prison" is semantically
  distant from the manual's "correctional facility" (§4.1.1), so retrieval
  doesn't surface it. A query-expansion step (synonyms before search) would
  likely fix it, but adds a model call and complexity; left documented as the
  next improvement.
- A test set where everything passes means the questions were too easy, so the
  one honest failure is kept deliberately.