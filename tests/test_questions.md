# Test set — 10 questions (honest results)

Floor requirement: my own 10 questions with honest pass/fail.
Run with: python -m tests.run_tests

A mix on purpose: straightforward answers, tricky answers, the planted gap,
the planted contradiction, genuinely uncovered topics, and (after the day-two
change) a date-sensitive question.

Result: 9/10 matched expectation. The one mismatch is a real, documented
finding kept honestly — a test set where everything passes means the
questions were too easy.

| # | Question | Expected | Actual | Result | Notes |
|---|----------|----------|--------|--------|-------|
| 1 | What is the resource limit for a household? | answer | answer | PASS | §2.4.1, $4,000 |
| 2 | How long to request a review? | answer | answer | PASS | §11.1.2, 30 days |
| 3 | Can I be eligible if I am 17? | answer | answer | PASS | §2.3.1 |
| 4 | What income is disregarded? | answer | answer | PASS | §6.4.1. Was a false refusal earlier; fixed by widening retrieval to top 8. |
| 5 | How is a full-time student's award calculated? | refuse | refuse | PASS | The planted GAP — correctly refused instead of inventing an answer. |
| 6 | Am I eligible if I own a pet? | refuse | refuse | PASS | Genuinely not in manual. |
| 7 | Earnings disregard for a claim dated 2026-04-15? | answer | answer | PASS | Date-aware: returns $175 (amended). A January claim returns $120 (base manual). Proves the day-two date logic. |
| 8 | How many days to report a change? | answer | answer | PASS | Now surfaces the §4.3.2 (10) vs §9.1.4 (30) conflict instead of silently picking one. Contradiction detection working. |
| 9 | What happens to my award if I go to prison? | answer | refuse | FAIL | Known limitation: "prison" is semantically distant from the manual's "correctional facility" (§4.1.1), so retrieval doesn't surface it. Documented in DECISIONS.md; query expansion would fix it. |
| 10 | Can someone attend my interview with me? | answer | answer | PASS | §8.5.3 |

## What the results tell us
- Q4 and Q8 were failures in an earlier run and are now fixed (wider
  retrieval; contradiction detection). Kept in the history to show the fixes.
- Q7 now tests the day-two date logic directly: the same question gives
  different correct answers for an April 2026 vs a January 2026 claim.
- Q9 is the one remaining honest failure — a genuine vocabulary-gap limit of
  semantic retrieval, documented rather than hidden.