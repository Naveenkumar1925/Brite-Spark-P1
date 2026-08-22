# Test set — 10 questions (honest results)

Floor requirement: my own 10 questions with honest pass/fail.
Run with: python -m tests.run_tests

A mix on purpose: straightforward answers, tricky answers, the planted
gap, the planted contradiction, and genuinely uncovered topics.
Result: 7/10 matched expectation. The 3 mismatches are real findings,
kept here honestly — a test set where everything passes means the
questions were too easy.

| # | Question | Expected | Actual | Result | Notes |
|---|----------|----------|--------|--------|-------|
| 1 | What is the resource limit for a household? | answer | answer | PASS | §2.4.1, $4,000 |
| 2 | How long to request a review? | answer | answer | PASS | §11.1.2, 30 days |
| 3 | Can I be eligible if I am 17? | answer | answer | PASS | §2.3.1 |
| 4 | What income is disregarded? | answer | refuse | FAIL | False refusal — manual DOES cover this (§6.4.1). Refusal threshold too aggressive on list-style questions. |
| 5 | How is a full-time student's award calculated? | refuse | refuse | PASS | The planted GAP — correctly refused instead of inventing an answer. |
| 6 | Am I eligible if I own a pet? | refuse | refuse | PASS | Genuinely not in manual. |
| 7 | Can I apply if I live in a different county? | refuse | answer | FAIL | System answered from §2.1.2 (residency). On reflection the manual DOES address this, so my "refuse" label was wrong — the system behaved correctly. |
| 8 | How many days to report a change? | answer | answer | PASS* | Answered "10 days" (§4.3.2) — but silently picked one side of the §4.3.2 vs §9.1.4 contradiction. Passes the answer/refuse check but reveals: no conflict detection yet. |
| 9 | What happens to my award if I go to prison? | answer | refuse | FAIL | False refusal. §4.1.1(b) covers "correctional facility" but the question said "prison" — vocabulary gap + threshold too cautious. |
| 10 | Can someone attend my interview with me? | answer | answer | PASS | §8.5.3 |

## What the failures tell us
- Q4, Q9: refusal threshold is too aggressive — it refuses some questions
  the manual actually answers (false refusals).
- Q8: the system answers one side of a contradiction without noticing the
  conflict. Detecting this is the "if you have time" bonus in the spec.
- Q7: not a real failure — my expected label was wrong; the system was right.