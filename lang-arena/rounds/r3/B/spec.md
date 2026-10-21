# Terser 2

_Systems said in the fewest literal words; every keyword says what it means._

## Core words

| word | meaning |
|---|---|
| `raises` | A raises B: more A brings more B; less A brings less B |
| `lowers` | A lowers B: more A brings less B; less A brings more B |
| `runaway` | ends a loop: reinforcing, each change feeds itself and escalates, upward or downward |
| `balancing` | ends a loop: pulls toward a goal or limit and settles; balancing at X names it |
| `vs` | X vs Y: X is compared with Y |
| `to` | moves or flows to; A to B to C is a path |
| `back to` | flows back to an earlier step (rework or repeat) |
| `lag` | delay: what came just before arrives or acts late; lag 2 weeks gives its length |
| `stock` | X stock: X accumulates; rises while inflow exceeds outflow, falls while outflow exceeds inflow |
| `inflow, outflow` | A inflow: A adds to the stock; A outflow: A drains it |
| `parallel` | parallel A, B: A and B run at once; both done (or all done): join, wait for all |

## Rules

1. X: Y means when X holds, Y happens; else Z is the other case, to the clause end. Thresholds and counts work as X; each day: Y repeats.
   - e.g. `valid: process, else reject, tell sender; 3 fails: stop`
   - reads as: if valid, process it, otherwise reject it and tell the sender; after three failures, stop

2. Semicolons separate clauses. Commas list items; listed actions run in order, each starting only after the previous finishes. After parallel they run in parallel.
   - e.g. `collect data, clean, publish`
   - reads as: collect the data, then clean it, then publish it, each step waiting for the last

3. A cause chain ending on its first word is a closed loop, marked runaway or balancing. Links may mix raises and lowers.
   - e.g. `price raises supply lowers price, balancing`
   - reads as: higher price brings more supply, which lowers price: a balancing loop

4. X (A, B) or X (A to B): system X contains subsystems A and B. A path into X enters its first part and leaves from its last.
   - e.g. `ore to mill (crush to sort) to port`
   - reads as: ore goes into the mill, a system with subsystems crush then sort, and leaves sort for the port

Any other English word is an ordinary content word (a thing, quantity, actor or action) with its usual meaning.
