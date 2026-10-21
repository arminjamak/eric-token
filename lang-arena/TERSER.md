# Terser

_Systems said in the fewest literal words._

Terser is the language chosen from the Lang Arena. It is the one that is **most concise and most learnable at the same time**. It ranks first among all four arena languages on each balance measure below:

| Language | Concision (/50) | Learnability (/50) | Weaker half | Product | Harmonic mean |
|---|---|---|---|---|---|
| **Terser** | **45.1** | 48.0 | **45.1** | **2166** | **46.5** |
| Terse Plain | 39.8 | **49.6** | 39.8 | 1971 | 44.1 |
| Terse | 39.1 | 48.2 | 39.1 | 1884 | 43.2 |
| Plain Loop | 28.2 | 49.7 | 28.2 | 1400 | 36.0 |

Terser gives up 1.6 points of learnability compared with the most learnable language, and gains 5.3 points of concision in return. Readers with no spec still recovered 98% of the facts, and learners with the spec recovered 100%.

## Learn it in one minute

There are 11 words and 4 rules. Every other word keeps its ordinary English meaning.

### Words

| word | meaning | example |
|---|---|---|
| `lift` | more A brings more B; less brings less | `ads lift sales` |
| `cut` | more A brings less B; less brings more | `price cut demand` |
| `grows` | ends a loop: reinforcing, escalates up or down | `cash lift interest lift cash, grows` |
| `seeks` | ends a loop: balancing, settles toward a goal. `seeks X` names it | `room vs target ... seeks` |
| `vs` | compared with | `room vs target` |
| `to` | moves or flows to | `parts to assembly to test` |
| `back to` | flows back to an earlier step | `defects back to assembly` |
| `lag` | delay. `lag 2 weeks` gives its length | `order; lag 2 weeks, arrive` |
| `stock` | an amount that accumulates; rises when in > out | `tank level stock` |
| `in` / `out` | an inflow to / outflow from the stock | `inlet in, drain out` |
| `split` | parallel paths. `both done:` / `all done:` joins them | `order split packing, billing; both done: ship` |

### Rules

1. **`X: Y`** means "when X, Y". `else Z` is the other case. X can be a threshold (`over 90:`), a count (`3 fails:`) or a schedule (`each day:`).
2. **`;`** separates clauses. **`,`** lists steps in order, each waiting for the one before. After `split`, the listed paths run in parallel.
3. **A chain that ends on its first word is a loop.** Close it with `grows` or `seeks`.
   **Tip:** count the `cut`s in the loop. If the count is even (zero included), the loop is `grows`. If it is odd, the loop is `seeks`.
4. **`X (A to B)`** means system X contains subsystems A and B. A path into X enters at A and leaves from B.

## Examples

| System | Terser |
|---|---|
| Word-of-mouth growth | `customers lift referrals lift customers, grows forever` |
| Thermostat | `room vs target; below: heater on, warms; reached: off; seeks` |
| Tank | `tank level stock, inlet in, drain out` |
| Delayed ordering | `inventory below target: order; lag 2 weeks, so over-order; swings` |
| Pipeline | `collect data, clean, analyze, publish results` |
| Request check | `check requests; valid: process, else reject, tell sender` |
| Split and join | `order split packing, billing; both done: ship` |
| Limits to growth | `births lift population lift births, grows; population cut rations cut deaths cut population, seeks capacity` |
| Retry and escalate | `try job; fail: wait, retry; 3 fails: human review` |
| Factory | `parts from suppliers to factory (intake to assembly to inspection) to customers; defects back to assembly` |
| Vicious cycle | `stress cut sleep cut stress, grows` |
| Message queue | `message to queue; queue full: drop, else worker picks up, processes, result to storage` |
| Market | `demand vs supply; above: price rises; price cut demand lift price, seeks equilibrium; price lift supply lag cut price, seeks equilibrium` |

The full arena history, scores and runner-up languages are in [RESULTS.md](RESULTS.md).
