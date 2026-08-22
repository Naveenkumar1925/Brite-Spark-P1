# AI Usage

Per the Brite Spark AI policy: I used AI tooling during this build and take
full ownership of every line. I can explain any part of the submission.

## What I used AI for
- Writing and refining the hybrid retrieval (semantic + keyword) and the
  grounded-answer prompt.
- Debugging: the embedding tensor error, the API library switch
  (google.generativeai -> google.genai), and adding retry/quota handling.
- Drafting the README, DECISIONS.md, and the 10-question test harness.

## What I did / verified myself
- Chose the approach and made every design decision.
- Read the manual and confirmed the two planted flaws; wrote a script
  (tests/audit_manual.py) that verifies them programmatically.
- Ran the 10-question test set and recorded the honest pass/fail results,
  including the failures.
- Tested the clean-clone setup end to end myself.