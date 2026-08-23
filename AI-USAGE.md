# AI Usage

Per the Brite Spark AI policy: I used AI tooling during this build and take
full ownership of every line. I can explain any part of the submission.

## What I used AI for
- Writing and refining the hybrid retrieval (semantic + keyword) and the
  grounded-answer prompt.
- Building the date-aware answering for the day-two amendment (the prompt
  logic for the transitional rules) and the amendment-attachment step.
- Debugging: the embedding tensor error, the API library switch
  (google.generativeai -> google.genai), and adding retry/quota handling.
- Drafting the README, DECISIONS.md, and the test harness.

## What I did / verified myself
- Chose the approach and made every design decision.
- Read the manual and confirmed the two planted flaws; wrote a script
  (tests/audit_manual.py) that verifies them programmatically.
- Read the day-two amendment, worked out the transitional-rule behaviour, and
  verified it by hand ($175 for an April 2026 claim, $120 for January).
- Ran the 10-question test set and recorded the honest results, including the
  one remaining failure.
- Tested the clean-clone setup end to end myself.