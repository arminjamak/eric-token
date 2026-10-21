# Terse Plain

_Systems said in the fewest literal words._

## Core words

| word | meaning |
|---|---|
| `lift` | A lift B: more A gives more B, less A gives less B |
| `cut` | A cut B: more A gives less B, less A gives more B |
| `grows` | tags the loop just named as reinforcing: it amplifies itself, upward or downward |
| `seeks` | tags the loop just named as balancing: settles at a goal; seeks X names the goal |
| `vs` | is compared with |
| `to` | moves or flows to; A to B to C is a path |
| `back to` | flows back to an earlier step: a rework loop |
| `lag` | arrives only after a delay; lag 2 weeks gives its length |
| `stock` | X stock: X is an amount that accumulates over time |
| `in, out` | in: inflow into the stock; out: outflow from it |
| `has` | X has A, B: X is a system containing subsystems A and B |
| `split` | split A, B: A and B run in parallel; all done: they join |

## Rules

1. X: Y means when X holds, Y happens. A following else clause gives the other case. X can be a threshold, count or time: over 90, 3 fails, each day.
   - e.g. `valid: process; else reject; 3 fails: stop`
   - reads as: if valid, process it, otherwise reject it; after three failures, stop

2. Semicolons separate clauses. Commas list items; listed actions happen in order, each starting only after the last finishes. After split or has, commas list parts.
   - e.g. `collect, clean, publish`
   - reads as: collect; once done, clean; once done, publish

3. A lift or cut chain that ends on its first word is a closed loop; add grows or seeks to say which kind.
   - e.g. `cats lift kits lift cats, grows`
   - reads as: more cats, more kittens, more cats: a reinforcing loop

Any other English word is an ordinary content word (a thing, quantity, actor or action) with its usual meaning.
