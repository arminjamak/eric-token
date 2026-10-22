# Terser 2

_Systems said in the fewest literal words; every keyword says what it means._

Terser 2 is the current language. It is Terser, the winner of the Lang Arena, with its keywords replaced by the most self-explanatory short words found by the [vocabulary loop](vocab/RESULTS.md). In a blind head-to-head test it beat Terser **93.83 to 93.48**:

| | Terser | **Terser 2** |
|---|---|---|
| length vs plain English | 37% | 38% |
| read correctly with no spec | 99% | **100%** |
| unseen systems written correctly by a learner | 85% | **97.5%** |
| concision /50 | **45.1** | 44.1 |
| learnability /50 | 48.4 | **49.8** |

## Learn it in one minute

There are 11 keywords and 4 rules. Every other word keeps its ordinary English meaning.

### Keywords

| word | meaning | example |
|---|---|---|
| `raises` | more A brings more B; less brings less | `ads raises sales` |
| `lowers` | more A brings less B; less brings more | `price lowers demand` |
| `runaway` | ends a loop: reinforcing, escalates up or down | `cash raises interest raises cash, runaway` |
| `balancing` | ends a loop: settles toward a goal. `balancing at X` names it | `..., balancing at capacity` |
| `vs` | compared with | `room vs target` |
| `to` | moves or flows to | `parts to assembly to test` |
| `back to` | flows back to an earlier step | `defects back to assembly` |
| `lag` | delay. `lag 2 weeks` gives its length | `order; lag 2 weeks, arrive` |
| `stock` | an amount that accumulates; rises when inflow > outflow | `tank level stock` |
| `inflow` / `outflow` | adds to / drains the stock | `inlet inflow, drain outflow` |
| `parallel` | paths that run at once. `both done:` / `all done:` joins them | `order parallel packing, billing; both done: ship` |

### Rules

1. **`X: Y`** means "when X, Y". `else Z` is the other case. X can be a threshold (`over 90:`), a count (`3 fails:`) or a schedule (`each day:`).
2. **`;`** separates clauses. **`,`** lists steps in order, each waiting for the one before. After `parallel`, the listed paths run at the same time.
3. **A chain that ends on its first word is a loop.** Close it with `runaway` or `balancing`.
   Tip: count the `lowers` in the loop. An even count (including zero) means `runaway`; an odd count means `balancing`.
4. **`X (A to B)`** means system X contains subsystems A and B. A path into X enters at A and leaves from B.

## Examples

| System | Terser 2 |
|---|---|
| Word-of-mouth growth | `customers raises referrals raises customers, runaway forever` |
| Thermostat | `room vs target; below: heater on, warms; reached: off; balancing` |
| Tank | `tank level stock, inlet inflow, drain outflow` |
| Delayed ordering | `inventory below target: order; lag 2 weeks, so over-order; swings` |
| Pipeline | `collect data, clean, analyze, publish results` |
| Request check | `check requests; valid: process, else reject, tell sender` |
| Split and join | `order parallel packing, billing; both done: ship` |
| Limits to growth | `births raises population raises births, runaway; population lowers rations lowers deaths lowers population, balancing at capacity` |
| Retry and escalate | `try job; fail: wait, retry; 3 fails: human review` |
| Factory | `parts from suppliers to factory (intake to assembly to inspection) to customers; defects back to assembly` |
| Vicious cycle | `stress lowers sleep lowers stress, runaway` |
| Bank account | `account balance stock, deposits inflow, withdrawals outflow, fees outflow; each month: balance raises interest, interest inflow` |
| Market | `demand exceeds supply: price rises; price lowers demand raises price, balancing at equilibrium; price raises supply lag lowers price, balancing at equilibrium` |

The last three examples were written by a Haiku learner after one read of the spec, on systems it had never seen.

The full reference, covering grammar, every systems-thinking concept, archetypes and cross-field examples, is in [LANGUAGE.md](LANGUAGE.md). The arena history is in [RESULTS.md](RESULTS.md), and the vocabulary loop in [vocab/RESULTS.md](vocab/RESULTS.md).
