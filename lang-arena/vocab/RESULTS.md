# Vocabulary loop: word length vs descriptiveness

Goal: make every core keyword of Terser say what it means, at the lowest cost in letters. All workers were low-cost Haiku agents following fixed, step-by-step instructions.

## Method

1. **Propose.** Two proposers suggest 5 new words per meaning: one is literal-first, the other short-first. The previous champions are always re-rated alongside the new words.
2. **Rate blind.** Four raters see each word *alone* and pick 1 of the 12 meanings. They also state a confidence from 1 to 3. The raters use two different paraphrases of the meaning list, shuffled.
3. **Score.** `D` is the mean over raters of (correct × confidence / 3). A word's `fitness = D − 0.03 × (letters − 3)`.
4. **Stop rule.** The loop continues while the champion set beats the previous set, re-rated by the same raters, by at least 6%.

| iteration | words rated | champion-set fitness | previous set, re-rated | gain |
|---|---|---|---|---|
| i1 | 104 | 10.09 | 6.78 (Terser's words) | **+48.8%** ✓ |
| i2 | 113 | 10.36 | 10.00 | **+3.6%** ✗, stop |

Full leaderboards: [i1/leaderboard.md](i1/leaderboard.md), [i2/leaderboard.md](i2/leaderboard.md).

## Final picks

| meaning | Terser | Terser 2 | D | why |
|---|---|---|---|---|
| more A → more B | lift (D 0.42) | **raises** | 0.83 | `fuels` scored 0.03 higher, which is within noise; `raises` pairs with `lowers` |
| more A → less B | cut (0.25) | **lowers** | 0.75–0.83 | champion |
| reinforcing loop | grows (0.0) | **runaway** | 0.92–1.0 | champion |
| balancing loop | seeks (0.75) | **balancing** | 1.0 | champion |
| inflow / outflow | in / out (0.42 / 0.58) | **inflow / outflow** | 1.0 / 1.0 | a natural pair; `inlet` and `drains` scored slightly higher but don't pair |
| parallel | split (0.83) | **parallel** | 1.0 | champion |
| compare | vs | vs | 0.67–0.75 | `compare` scored higher but breaks the `A vs B` pattern |
| flow | to | to | — | `onward` and `passes` won in isolation but can't chain: `A onward B onward C` |
| rework | back to | back to | 0.83 | `rewinds` won in isolation but breaks `defects back to assembly` |
| delay, stock | lag, stock | lag, stock | 1.0 | already the champions |

**Limit of the method.** Rating a word alone undervalues small connecting words (`to`, `vs`) whose meaning comes from where they sit in the sentence. So a champion only replaced the current word when it also fit the word's sentence pattern.

## Validation (rounds/r3)

The same arena protocol was run on both languages under identical conditions: Haiku testers and a Sonnet judge, blind.

| | Terser | **Terser 2** |
|---|---|---|
| length vs English | 37% | 38% |
| cold-read (no spec) | 0.99 | **1.00** |
| spec-decode | 1.00 | 1.00 |
| encode unseen systems | 0.85 | **0.975** |
| cold reader difficulty (1–10) | 6 | **4** |
| concision /50 | **45.1** | 44.1 |
| learnability /50 | 48.4 | **49.8** |
| **total** | 93.48 | **93.83** |

Terser 2 trades 1 point of concision for 1.4 points of learnability. Its learner also encoded the delayed market loop with the correct signs, the mistake Terser's learners made in round 2. The margin is small, and one test round is noisy. The direction matches the vocabulary loop, though.
