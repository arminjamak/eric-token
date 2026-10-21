# Plain Loop: designer A, round 1

## Rationale
Bias: learnability first. Every sentence should read as clipped but ordinary English, so a cold reader gets most facts without the spec.

- **Few reserved words (9) + 6 rules = core 15**, so economy is at full marks. Most structure rides on words that already mean the right thing: `if/else`, `then`, `to`, `back to`, `after`, `has`, `split`, `both done`.
- **Cause = the English "more X, more Y" idiom.** Any comparative works (less, higher, slower). That idiom carries polarity for free and reads literally.
- **Loops close implicitly.** A cause chain followed by `: reinforcing loop` or `: balancing loop` feeds back to its first item, so we never repeat the start node. The loop names are the standard systems terms, which cold readers recognise.
- **Flows use `to` chains** (`suppliers to intake to assembly`). `back to` marks rework or a return.
- **Conditions use `if C, X; else Y`**, with `over / below / at` for thresholds. Semicolons separate branches.
- **Colon = parts or details** (`factory has subsystems: ...`) for nesting.
- **Articles and filler are dropped.** Punctuation is kept where it prevents misreading, because it costs only half a word.

## Changes from base
Round 1, so there is no base. Designed from scratch.

## Self-measured metrics (`arena.py check`)
- length_ratio 0.6018
- compression 0.5689
- core_size 15
- economy 1.0
- errors: none

## Trade-offs made
- Kept "compare" (b2), "incoming" (b6) and "in parallel" (b7) because each one carries a graded fact a cold reader might otherwise miss.
- Dropped the repeated start node in loops (about 4 words saved). The spec covers this, and "loop" makes it guessable cold.
- Kept `stock` defined plainly but still wrote the rise/fall conditions out in b3, so they survive a cold read.

## Ideas for next time
- Compression is the weak axis (about 40% shorter vs the 70% needed for full marks). Candidates: drop commas in `then` chains; use `if under` style ellipsis more; let a bare `: balancing loop` replace a stated goal comparison.
- Consider `max N` for retry limits as a lexicon entry if held-out items stress limits.
- Check how testers decode the elliptical "if under, falls" and "less food each". Expand them if they lose facts.
