# Lang Arena results

**Current language: Terser 2.** This is Terser with keywords optimised by the [vocabulary loop](vocab/RESULTS.md). It beat Terser 93.83 to 93.48 in a blind validation round (`rounds/r3`). See **[TERSER.md](TERSER.md)** for the one-page guide.

**Arena winner: Terser.** It was built by designer B, the concision-first designer, and won both rounds. It is also the most concise *and* most learnable language at the same time: it ranks first on the weaker half, the product and the harmonic mean of the two scores. The arena stopped after round 2. B raised its total by only **+5.84** points, short of the required +6, which ended the arena.

## Scoreboard

| Round | A: learnability-first | B: concision-first | Winner | A gain | B gain |
|---|---|---|---|---|---|
| 1 (from scratch) | Plain Loop **77.86** | Terse **87.28** | B | | |
| 2 (both forked Terse) | Terse Plain **89.33** | Terser **93.12** | B | +11.47 ✓ | **+5.84 ✗** |

| Component | r1 A | r1 B | r2 A | r2 B |
|---|---|---|---|---|
| length vs English | 60% | 45% | 44% | **37%** |
| compression (0–1) | 0.57 | 0.78 | 0.80 | **0.90** |
| spec-decode fidelity | 0.99 | 1.00 | 1.00 | 1.00 |
| cold-read (no spec) | 0.99 | 0.98 | **0.99** | 0.98 |
| encode unseen systems | **1.00** | 0.84 | 0.97 | 0.83 |
| core size (words + rules) | 15 | 15 | 15 | 15 |
| **Concision (out of 50)** | 28.2 | 39.1 | 39.8 | **45.1** |
| **Learnability (out of 50)** | **49.7** | 48.2 | 49.6 | 48.0 |
| **Total** | 77.86 | 87.28 | 89.33 | **93.12** |

In both rounds the winning principle was **concision**. Learnability was already close to its ceiling: every language could be read cold at 98% or better. Most of the difference therefore came from length. B's miss on the stopping rule was very narrow (0.16 points), which is within the noise of LLM grading.

## The final language: Terser

_Systems said in the fewest literal words._ It has 11 core words and 4 rules. Every other word keeps its ordinary English meaning.

| word | meaning |
|---|---|
| `lift` | A lift B: more A brings more B; less A brings less B |
| `cut` | A cut B: more A brings less B; less A brings more B |
| `grows` | ends a loop: reinforcing; each change feeds itself and escalates, upward or downward |
| `seeks` | ends a loop: balancing; pulls toward a goal or limit and settles. `seeks X` names the goal |
| `vs` | X vs Y: X is compared with Y |
| `to` | moves or flows to. A to B to C is a path |
| `back to` | flows back to an earlier step (rework or repeat) |
| `lag` | delay: what came just before arrives or acts late. `lag 2 weeks` gives its length |
| `stock` | X stock: X accumulates; rises while in exceeds out, falls while out exceeds in |
| `in` / `out` | A in: A is an inflow to the stock. A out: an outflow from it |
| `split` | split A, B: A and B run in parallel. `both done:` or `all done:` joins them, waiting for all |

**Rules**

1. **`X: Y`** means that when X holds, Y happens. An `else` introduces the other case and runs to the end of the clause. X can be a threshold or a count, and `each day: Y` repeats Y.
2. **`;`** separates clauses. **`,`** lists items. Listed actions run in order, each starting after the previous one finishes, except after `split`, where they run in parallel.
3. A cause chain that **ends on its first word** is a closed loop, marked `grows` or `seeks`. Its links may mix lift and cut.
4. **`X (A to B)`** means system X contains subsystems A and B. A path into X enters its first part and leaves from its last.

### Benchmark translations

| | Plain English | Terser |
|---|---|---|
| reinforcing loop | More customers lead to more word-of-mouth referrals, which bring in more customers. This loop reinforces itself and grows without limit. | `customers lift referrals lift customers, grows forever` |
| thermostat | A thermostat compares the room temperature with a target. When the room is colder than the target, the heater turns on and raises the temperature. When the room reaches the target, the heater turns off. | `room vs target; below: heater on, warms; reached: off; seeks` |
| stock and flow | Water flows into a tank through an inlet and out through a drain. The water level is a stock: it rises when inflow exceeds outflow and falls when outflow exceeds inflow. | `tank level stock, inlet in, drain out` |
| delay oscillation | A shop orders goods when inventory is below target. Deliveries arrive after a two-week delay. Because of the delay, the shop over-orders, and inventory oscillates above and below the target. | `inventory below target: order; lag 2 weeks, so over-order; swings` |
| pipeline | Raw data is collected, then cleaned, then analyzed, and the results are published. Each step starts only after the previous step finishes. | `collect data, clean, analyze, publish results` |
| branch | Each incoming request is checked. If it is valid, it goes to processing; if not, it is rejected and the sender is notified. | `check requests; valid: process, else reject, tell sender` |
| split / join | An order splits into two parallel tasks: packing and billing. Shipping starts only when both tasks are complete. | `order split packing, billing; both done: ship` |
| limits to growth | A population grows through reproduction, which is a reinforcing loop. As the population grows, food per individual drops, which raises the death rate and slows growth. Growth eventually levels off at the carrying capacity. | `births lift population lift births, grows; population cut rations cut deaths cut population, seeks capacity` |
| retry + escalate | A job is attempted. If it fails, the system waits and then retries. After three failed attempts, the job is sent to a human for review. | `try job; fail: wait, retry; 3 fails: human review` |
| nested subsystems | A factory is a system containing three subsystems: intake, assembly, and quality check. Parts enter from suppliers into intake, move through assembly to quality check, and finished products leave to customers. Defective products from quality check return to assembly. | `parts from suppliers to factory (intake to assembly to inspection) to customers; defects back to assembly` |

### Unseen systems, written by a learner after one read of the spec

These four systems were never shown to the designers.

| Held-out system | Learner's Terser |
|---|---|
| Stress reduces sleep, and less sleep increases stress: a vicious cycle. | `stress cut sleep cut stress, grows` |
| A bank balance with deposits in, withdrawals and fees out, and monthly interest proportional to the balance. | `bank account balance stock, deposits in, withdrawals out, fees out; each month: balance lift interest, interest in` |
| A message is dropped if the queue is full; otherwise a worker processes it and stores the result. | `message to queue; queue full: drop message, else worker picks up, processes, result to storage` |
| Prices rise when demand exceeds supply; higher prices cut demand and, after a delay, raise supply, so prices return to equilibrium. | `demand vs supply; above: price rises; price cut demand cut price, seeks equilibrium; ...` ⚠ sign error |

## Known weak spots, for anyone continuing the work

- **Loop signs with several `cut`s.** A loop with an even number of `cut` links is reinforcing, and one with an odd number is balancing. Learners got this wrong (h4), and cold readers stumbled on `population cut rations cut deaths cut population`. A short rule stating the parity would probably fix it.
- **Implied facts read weaker cold.** `stock` implies rise and fall, and the commas imply that each step waits for the last. Both decode perfectly with the spec, but only vaguely without it.
- **Escalation.** `grows` does not clearly say "keeps getting worse". Both designers' learners lost half a point there.
- **Runner-up.** A's round 2 language, Terse Plain, is the better choice for teaching. It scored 0.97 on encoding unseen systems against Terser's 0.83, at 44% of English length instead of 37%. It keeps an explicit `has` word for subsystems and a separate `else` clause.

## Files

- `rounds/rN/{A,B}/language.json`: each language. `spec.md` is the generated spec testers saw. `notes.md` is the designer's rationale.
- `rounds/rN/{A,B}/tests/`: the raw output of the cold reader and the spec learner.
- `rounds/rN/judge.json`: per-fact grades. `blind_map.json` shows which blind label was which designer.
- `benchmark/heldout.json`: the held-out encode set, published now that the arena is over.
