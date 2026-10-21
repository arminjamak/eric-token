# Terse: design notes (round 1, designer B)

## Rationale
Concision first. Every structural idea maps to one short, literal English word, so a sentence reads like clipped speech:

- **Causal links:** `A lift B` (same direction) and `A cut B` (opposite direction). Chains compose: `population cut rations cut deaths cut population` gives the sign of each link without extra words.
- **Loops:** a chain that ends on its first word closes the loop. `grows` marks a reinforcing loop and `seeks` marks a balancing one.
- **Conditions:** `X: Y` (a colon costs half a word, while `if` costs a whole word), with `else` for the other branch. Count thresholds come free: `3 fails: human review`.
- **Sequence vs parallel:** `then` means strictly after the previous step. `split A, B` means parallel. A join is written in plain English (`both done:`).
- **Flow:** `to` / `back`, `from` for inputs. `stock`, `in`, `out` for accumulations. `lag N` for delays. `has` for nesting.
- **Punctuation:** a semicolon separates clauses and a comma lists items.

The core is 13 words and 2 rules (15 in total), which gets full economy. I left out any token that plain English already handles (`both`, `else`, `so`, `over`, `forever`).

## Changes from base
None. Round 1 started from scratch.

## Self-measured (arena.py check)
- length_ratio 0.4523
- compression 0.7824
- core_size 15
- economy 1.0
- errors: none

## Cold-read self-test
Every fact appears as a literal word in the text, apart from the meanings of `lift`/`cut`, which context makes guessable. Two risks remain:
- `inspection` stands for "quality check".
- `seeks capacity` stands for "levels off at carrying capacity".

## Ideas for next time
- Test whether dropping `then` in favour of comma sequencing survives fidelity (it would save about 3 words).
- Find a shorter stock idiom than `in over out: rises, else falls`. The spec could make rise and fall implicit, but that would cost cold-read accuracy.
- Consider `all done:` as the explicit join idiom in the spec.
