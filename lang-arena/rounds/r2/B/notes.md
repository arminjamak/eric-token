# Terser: design notes (round 2, designer B)

## Rationale
Built on Terse (r1 winner), still concision first. Fidelity and economy were already full, so the gains had to come from compression (0.78) and encode validity (0.84).

## Changes from base, and why
- **No trailing periods.** They cost 5 word-units and carried nothing.
- **`then` removed. Commas now carry strict sequence** (rule 2; after `split` they are parallel). This shortens b5 and frees a slot.
- **`stock` meaning absorbs rise and fall** (it rises while in exceeds out). b3 drops `in over out: rises, else falls`, so b3 is now 8 word-units instead of 16. This may cost a little on the cold read.
- **`has` replaced by parentheses (rule 4).** `X (A to B)` nests subsystems, and a path through X enters its first part. In b10 the subsystems and the flow are written once instead of twice (17.5 word-units instead of 24).
- **`lag` no longer requires N.** A bare `lag` is valid. This fixes the r1 encode validity failure (0.5).
- **`grows` covers escalation in either direction**, so "keeps getting worse" has a home.
- **Rule 3 shows a mixed lift/cut loop.** Rule 1 names thresholds, counts and recurrence (`each day:`). r1 learners found these hardest.
- Item edits: b4 dropped `deliveries` (lag covers arrival) and `around target`, b6 uses `check requests`, and b8's second loop ends `, seeks capacity`.

Core: 11 words and 4 rules = 15 (full economy).

## Self-measured (arena.py check)
- length_ratio 0.3685 (was 0.4523)
- compression 0.9021 (was 0.7824)
- core_size 15, economy 1.0
- errors: none

Projected total is about 93 to 94: concision about 45.1 at full fidelity, plus learnability of 48 to 49.

## Cold-read self-test
Every fact is still a literal word, except three that are implied:
- b3: rise and fall come from `stock`.
- b5: "each step waits" comes from the commas.
- b10: "subsystems" comes from the parentheses.

## Ideas for next time
- Use loop polarity from counting `cut`s, so `grows`/`seeks` could be dropped when a chain is closed.
- Allow a chain to continue from the last word of the previous clause (`...population, grows; cut rations ...`).
- Find a one-word join (`join:`) if `both done` turns out to be redundant for readers.
