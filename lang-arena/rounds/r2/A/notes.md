# Terse Plain: designer A, round 2

## Rationale
Base: round 1 winner Terse (B). Its core already decodes almost perfectly, so I kept every word that reads literally (`lift`, `cut`, `grows`, `seeks`, `vs`, `to`, `lag`, `stock`, `has`, `split`) and spent changes on the gaps the round 1 testers exposed: encode validity, ambiguous clause boundaries, and missing idioms. Learnability first: no new invented forms, only clearer glosses and one fewer special word.

## Changes from base
- **Dropped `then`.** Commas now carry sequence: a comma-listed run of actions happens in order, each starting after the last finishes (rule 2). Plain English already reads `collect, clean, analyze` as ordered, and each step is shorter.
- **`lag` no longer needs a number.** Round 1 lost half an encode point when a learner wrote a bare delay. The gloss now says the length is optional (`lag 2 weeks gives its length`).
- **`else` is its own clause.** `valid: process; else reject, tell sender` (b6). With the base's comma it was unclear whether `tell sender` belonged to else. A semicolon costs the same.
- **Threshold, count and time conditions are named in rule 1** (`over 90`, `3 fails`, `each day`). Round 1 learners found recurring events and thresholds the hardest to write.
- **`grows` covers vicious cycles** ("upward or downward"), so "keeps getting worse" has a home. **`seeks X` names the goal.**
- **Join idiom in the spec:** `split A, B ... all done:`.
- **`back` became `back to`** so the entry always names its target.
- **b2:** dropped the redundant second `room`.
- Core: 12 words + 3 rules = 15 (full economy). The freed `then` slot became a rule that pins down punctuation.

## Self-measured (arena.py check)
- length_ratio 0.4432 (base 0.4523)
- compression 0.7954
- core_size 15, economy 1.0
- errors: none

## Cold-read self-test
Each fact appears as a literal word. Remaining risks: b5's "each waits" is implicit in the comma list (the base also lost half of that fact), and in b10 "factory has" may not read as "system with subsystems".

## Ideas for next time
- Test leaving rise/fall implicit in `stock` (b3 would save about 7 words), if spec decoders reliably expand it.
- Try `subsystems:` as the nesting form if the b10 cold read keeps missing it.
- Try a compact form for a loop with mixed signs and a delay in a single chain.
