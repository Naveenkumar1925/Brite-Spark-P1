# Demo transcript — The Grounded Answer

Example interactions showing the assistant's behaviour. Run any of these
yourself with:  python -m src.main "your question" --date YYYY-MM-DD

---

## 1. A grounded answer with citation
```
$ python -m src.main "What is the resource limit for a household?"

The resource limit for a household is $4,000. A household is not eligible
if its total countable resources exceed this amount (§2.4.1).

Sources:
§2.4.1: A household is not eligible where the total countable resources of
the household exceed $4,000.
```

## 2. A refusal (the manual does not cover it)
```
$ python -m src.main "How is a full-time student's award calculated?"

The manual does not settle this question. I could not find a clause that
directly answers it.
Next step: refer this to a supervisor, who can give a decision and record
the reasons on the case file.
```
The manual defines "full-time student" and points to separate treatment, but
no clause actually rules on it — so the assistant refuses rather than guessing.

## 3. Surfacing a contradiction instead of guessing
```
$ python -m src.main "How many days do I have to report a change?" --date 2026-01-15

The manual is inconsistent on this point:
- §4.3.2 says a change must be reported within 10 calendar days.
- §9.1.4 refers to "the 30 calendar days required under §4.3".
```
Rather than confidently picking one, the assistant shows both conflicting
clauses so a caseworker can see the discrepancy.

## 4. Date-aware answers (the day-two amendment)
```
$ python -m src.main "What is the earnings disregard?" --date 2026-04-15
  -> $175 per month (amended figure, §1.1 [amendment-2026-01])

$ python -m src.main "What is the earnings disregard?" --date 2026-01-15
  -> $120 per month (base manual, §6.4.1)
```
The same question gives different correct answers depending on the claim date,
because Amendment 2026-01 takes effect 1 March 2026.

## 5. Spanning-date claim (the hardest transitional case)
```
$ python -m src.main "My claim covers February and March 2026. What earnings
  disregard applies?" --date 2026-03-15

Because your claim spans 1 March 2026, the figures in force on each day apply
and the award is apportioned (§5.3 [amendment-2026-01]):
- February 2026: $120 per month (base manual, §6.4.1(a))
- March 2026:    $175 per month (amended, §1.1 [amendment-2026-01])
```
The assistant applies the correct figure to each part of the period and cites
the apportionment rule — without any special-case code.
