"""Turns the 'cannot ground an answer' signal into a helpful refusal.

We do NOT hard-code specific questions (like the student gap). We refuse
whenever the answer step could not ground an answer in the clauses.
This handles the known gaps AND any new one the day-two change might add.
"""

# The signal answer.py returns when the clauses don't cover the question.
NOT_IN_MANUAL = "NOT_IN_MANUAL"


def is_refusal(raw_answer):
    """True if the answer step could not ground an answer."""
    return NOT_IN_MANUAL in raw_answer.strip().upper()


def refusal_message(question):
    """A helpful refusal: says the manual doesn't settle it, and who to ask."""
    return (
        "The manual does not settle this question. I could not find a clause "
        "that directly answers it.\n"
        "Next step: refer this to a supervisor, who can give a decision and "
        "record the reasons on the case file."
    )