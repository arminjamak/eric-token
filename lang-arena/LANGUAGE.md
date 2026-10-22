# Terser 2: Language Reference

_Systems said in the fewest literal words; every keyword says what it means._

This is the full reference for Terser 2: what the language is, how its grammar works, every systems-thinking concept it can express, and how those concepts combine into whole systems. For the one-page summary, see [TERSER.md](TERSER.md). For how the language was made, see [RESULTS.md](RESULTS.md) and [vocab/RESULTS.md](vocab/RESULTS.md).

---

## Contents

1. [What Terser 2 is](#1-what-terser-2-is)
2. [Design principles](#2-design-principles)
3. [Building blocks](#3-building-blocks)
4. [Grammar](#4-grammar)
5. [Reading aloud](#5-reading-aloud)
6. [Style rules and common mistakes](#6-style-rules-and-common-mistakes)
7. [Systems-thinking concepts](#7-systems-thinking-concepts)
8. [How the concepts combine](#8-how-the-concepts-combine)
9. [System archetypes](#9-system-archetypes)
10. [Systems from other fields](#10-systems-from-other-fields)
11. [Behaviour over time](#11-behaviour-over-time)
12. [Limits of the language](#12-limits-of-the-language)
13. [Quick reference card](#13-quick-reference-card)

---

## 1. What Terser 2 is

Terser 2 is a constructed language for describing systems: the causal loops, flows, accumulations, delays, decisions and nested parts that make up anything from a thermostat to an economy. It is built entirely from ordinary written English words and a few punctuation marks. It has no symbols, no arrows and no invented words.

A Terser 2 sentence sounds like someone explaining a system with as few words as possible, stating only the literal concepts:

> `births raises population raises births, runaway; population lowers rations lowers deaths lowers population, balancing at capacity`
>
> _Births raise the population, which raises births: a runaway loop. A bigger population means smaller rations, smaller rations mean more deaths, and more deaths mean a smaller population: a balancing loop that settles at capacity._

The plain-English version of that system takes 34 words. The Terser 2 version takes 16. Across the benchmark, Terser 2 runs at **38% of the length of plain English**. In blind tests, readers recovered **100%** of the meaning *without ever seeing the rules*, and learners wrote **97.5%** of unseen systems correctly after one read of the spec.

**Size:** 11 keywords and 4 rules. Every other word is an ordinary English word with its ordinary meaning.

---

## 2. Design principles

| Principle | What it means in practice |
|---|---|
| **Less but more** | Every word carries a concept. There are no articles, no "is", no "which", no "then": structure is carried by punctuation and a few keywords. |
| **Literal** | Each keyword is the plain English word for its idea: `raises`, `lowers`, `runaway`, `balancing`, `inflow`, `parallel`. A newcomer can read it cold. |
| **English only** | Only real English words, digits and `. , : ; ( ) ' -`. This keeps it typeable, speakable and searchable. |
| **One way to say it** | Each structure has one canonical form. A learner never has to choose between synonyms for a structural idea. |
| **Content stays content** | The language never reinterprets ordinary words. `rabbits`, `price` and `heater on` mean exactly what they mean in English. |
| **Diagram-equivalent** | Every sentence maps onto a causal loop diagram, a stock-and-flow diagram or a process flowchart, and back. |

---

## 3. Building blocks

A Terser 2 text has three kinds of material.

### 3.1 Keywords (11)

| Keyword | Category | Meaning |
|---|---|---|
| `raises` | causal link | More of A brings more of B; less brings less. The two move in the **same** direction. |
| `lowers` | causal link | More of A brings less of B; less brings more. The two move in **opposite** directions. |
| `runaway` | loop tag | The loop just stated is **reinforcing**: every change feeds itself and escalates, upward or downward. |
| `balancing` | loop tag | The loop just stated is **balancing**: it pulls toward a goal or limit and settles. `balancing at X` names the goal. |
| `vs` | comparison | A is compared with B. Usually followed by conditions on the result. |
| `to` | path | Moves or flows to. `A to B to C` is a path. |
| `back to` | path | Flows back to an earlier step: rework, return, repeat. |
| `lag` | time | Delay. What came just before arrives or acts late. `lag 2 weeks` gives the length. |
| `stock` | accumulation | `X stock`: X is an amount that accumulates over time. |
| `inflow` / `outflow` | flow | `A inflow`: A adds to the stock. `A outflow`: A drains it. |
| `parallel` | concurrency | `parallel A, B`: A and B run at the same time. `all done:` or `both done:` joins them. |

### 3.2 Punctuation (5 marks, 4 roles)

| Mark | Role | Strength |
|---|---|---|
| `;` | Separates **clauses**: independent statements about the system. | strongest |
| `:` | **Condition → consequence**: `X: Y` means "when X, Y". | middle |
| `,` | **Lists**: steps in order, branches after `parallel`, or flows after `stock`. Also closes a loop before its tag. | weakest |
| `( )` | **Containment**: `X (A to B)` means system X contains subsystems A and B. | grouping |

### 3.3 Content words

Everything else is a content word: an **element** (a noun such as `price`, `water level`, `queue`), an **action** (a bare verb such as `check`, `ship`, `retry`), a **state** (`full`, `valid`, `below`), a **quantity** (`3`, `2 weeks`) or an **outcome** (`swings`, `collapse`, `levels off`). Content words keep their everyday meaning, and multi-word names are fine: `account balance`, `quick fix`, `human review`.

---

## 4. Grammar

A text is a sequence of **clauses** separated by `;`. Each clause is one of the eight forms below. Forms can nest inside conditions and inside parentheses.

### 4.1 Causal chain

```
A raises B
A lowers B
A raises B lowers C raises D
```

Read the links left to right, each joining the two elements on either side of it. The keyword form never changes. Write `customers raises referrals`, not `customers raise`. The fixed form makes keywords easy to spot.

### 4.2 Loop (rule 3)

**A chain that ends on its first word is a closed feedback loop.** It is closed with a comma and a loop tag:

```
A raises B raises A, runaway
A raises B lowers A, balancing
A raises B lowers A, balancing at goal
```

**Parity rule:** count the `lowers` in the loop.

| Number of `lowers` | Loop type |
|---|---|
| 0, 2, 4 … (even) | `runaway` (reinforcing) |
| 1, 3, 5 … (odd) | `balancing` |

The tag must agree with the parity. Words after the tag describe its behaviour: `runaway forever`, `balancing at capacity`.

### 4.3 Delay

`lag` follows the element or link whose effect arrives late. A duration can follow it:

```
price raises supply lag lowers price, balancing
inventory below target: order; lag 2 weeks, so over-order
```

The first sentence says that supply responds to price only after a delay.

### 4.4 Stock and flows

```
X stock, A inflow, B outflow
```

A stock rises while total inflow exceeds total outflow and falls while outflow exceeds inflow; that rule is part of the meaning of `stock` and never needs stating. A stock may have any number of flows, and one flow may leave one stock and enter another (§7.11).

### 4.5 Path

```
A to B to C
C back to A
from A to B
```

A path is material, work or information moving through places or stages. `back to` sends something upstream.

### 4.6 Sequence (rule 2)

```
collect data, clean, analyze, publish results
```

Comma-listed **actions** run in order, each starting only after the previous one finishes. No `then` is needed.

### 4.7 Parallel split and join

```
order parallel packing, billing; both done: ship
```

After `parallel`, the comma list holds **branches running at the same time**. `both done:` (two branches) or `all done:` (more) is a **join**: the next step waits for every branch.

### 4.8 Condition (rule 1)

```
X: Y
X: Y, else Z
```

When X holds, Y happens. `else` gives the other case, and its scope runs **to the end of the clause** (the next `;`). The X part can be:

| Kind | Example |
|---|---|
| state | `valid: process` |
| threshold | `temperature over 30: fan on` |
| count | `3 fails: human review` |
| schedule | `each day: backup` |
| comparison result | `speed vs limit; over: brake` |
| join | `all done: ship` |

### 4.9 Comparison

```
room vs target; below: heater on; reached: off
```

`vs` sets up a comparison, and the following conditions use bare comparatives (`below`, `over`, `reached`, `above`) to refer to its result.

### 4.10 Containment (rule 4)

```
X (A, B)          system X contains parts A and B
X (A to B)        X contains A and B, and the internal path runs A then B
city (water (pumps to pipes), power (plant to grid))
```

A path into X enters its **first** part and leaves from its **last**. Nesting has no depth limit.

### 4.11 Consequence and outcome words

These are ordinary English words, not keywords, but they are idiomatic in Terser 2.

| Word | Use | Example |
|---|---|---|
| `so` | introduces a consequence | `lag 2 weeks, so over-order` |
| `swings` | oscillation | `so swings around target` |
| `forever` | unbounded | `runaway forever` |
| `collapse`, `peaks`, `levels off`, `stalls` | behaviour over time | `fish falls, collapse` |

### 4.12 Precedence

`;` is the strongest separator, then `:`, then `,`. Parentheses group a subsystem. The tightest binding is the link: `raises` and `lowers` bind the words immediately around them.

```
valid: process, else reject, tell sender
  = [valid] : [process] , else [reject, tell sender]
```

---

## 5. Reading aloud

Terser 2 is meant to be spoken. Expand each keyword like this:

| Written | Spoken |
|---|---|
| `A raises B` | "A raises B" or "more A, more B" |
| `A lowers B` | "A lowers B" or "more A, less B" |
| `..., runaway` | "a runaway loop" |
| `..., balancing at X` | "a balancing loop, settling at X" |
| `X: Y` | "when X, Y" |
| `a, b, c` | "a, then b, then c" |
| `parallel a, b` | "a and b at once" |
| `lag 2 weeks` | "after a two-week lag" |
| `X stock, A inflow` | "X builds up; A flows in" |
| `X (A to B)` | "X, made of A then B" |

Read aloud, a full text sounds like a very terse engineer:

> `check requests; valid: process, else reject, tell sender`
> "Check requests. Valid: process. Else reject, tell sender."

---

## 6. Style rules and common mistakes

### Style

1. **Structure first, details after.** Declare stocks and paths, then the loops that act on them.
2. **One mechanism per clause.** Each loop gets its own clause and its own tag.
3. **Name the goal of a balancing loop** whenever there is one: `balancing at target`.
4. **Element names are nouns, actions are bare verbs.** Use `queue`, `price`, `wait` for elements and `ship`, `retry`, `notify` for actions.
5. **Never put a keyword inside a name.** Write `their fear`, not `threat to them`, because `to` would be read as a path.
6. **Numbers as digits.** Write `3 fails`, `lag 2 weeks`.

### Common mistakes

| Mistake | Wrong | Right | Why |
|---|---|---|---|
| Tag disagrees with parity | `infection lowers susceptible lowers infection, balancing` | `infection lowers susceptible raises infection, balancing` | Fewer susceptible people means *less* infection, so that link is `raises`. One `lowers` makes it balancing. |
| Link polarity misread | `sales raises hiring raises training load lowers quality lowers sales` | `sales raises hiring raises training load lowers quality raises sales, balancing` | Polarity belongs to each pair on its own: higher quality *raises* sales. |
| Loop not closed | `stress lowers sleep raises mood, runaway` | `stress lowers sleep lowers stress, runaway` | A loop must end on its first word. |
| `else` reaching too far | `full: drop, else queue; notify` | `full: drop, else queue, notify` | `else` stops at `;`. |
| Inflected keyword | `prices raise demand` | `price raises demand` | Keywords keep one form. |

---

## 7. Systems-thinking concepts

Each concept below gives a definition, how Terser 2 expresses it, and an example with its plain-English reading.

### 7.1 System, element and boundary

**Definition.** A *system* is a set of elements connected so that together they produce behaviour that none produces alone. Its *boundary* separates what is modelled from the *environment*, which supplies inputs and receives outputs.

**In Terser 2.** Elements are content words. The boundary is drawn with containment: whatever is inside the parentheses is the system, and anything reached with `from` and `to` outside them is the environment.

```
parts from suppliers to factory (intake to assembly to inspection) to customers
```

_Parts come from suppliers (environment) into the factory system, made of intake, then assembly, then inspection, and leave to customers (environment)._

### 7.2 Causal link and polarity

**Definition.** A *causal link* says a change in one variable causes a change in another. Its *polarity* is **same direction** (+) or **opposite direction** (−).

**In Terser 2.** Same direction is `raises`; opposite direction is `lowers`. Polarity holds both ways: `A raises B` also means *less* A brings *less* B.

```
ads raises sales
price lowers demand
```

### 7.3 Causal chain

**Definition.** A sequence of links through which an effect travels. A chain's overall polarity is the product of its link polarities.

```
rain raises river lowers bridge safety raises traffic
```

_More rain raises the river, which lowers bridge safety, which, being lower, means less traffic._

### 7.4 Feedback loop

**Definition.** A chain that returns to its starting point, so a variable ends up influencing itself. Feedback is the core idea of systems thinking: it explains why systems grow, stabilise, oscillate or collapse on their own.

**In Terser 2.** Rule 3: a chain ending on its first word, closed with a tag.

### 7.5 Reinforcing loop (`runaway`)

**Definition.** A loop with an even number of opposite-direction links. It amplifies change, which produces exponential growth or exponential decline. It is a *virtuous circle* when it runs the way you want and a *vicious circle* when it doesn't.

```
customers raises referrals raises customers, runaway forever
debt raises interest raises debt, runaway
stress lowers sleep lowers stress, runaway
fear lowers trust lowers fear, runaway
```

The last two contain two `lowers` each, so they are still runaway. A loss of sleep feeds stress, which feeds further loss of sleep.

### 7.6 Balancing loop (`balancing`)

**Definition.** A loop with an odd number of opposite-direction links. It resists change and pulls a variable toward a goal, set point or limit. It is the source of stability, homeostasis and control.

```
hunger raises eating lowers hunger, balancing at full
gap raises effort raises progress lowers gap, balancing
price raises supply lowers price, balancing
```

### 7.7 Goal, gap and comparison

**Definition.** Balancing loops compare an actual state with a desired state. The difference, the *gap*, drives corrective action.

**In Terser 2.** `vs` sets up the comparison. Conditions act on the result, and `balancing at X` names the goal.

```
room vs target; below: heater on, warms; reached: off; balancing
```

_Compare the room with the target. If the room is below the target, the heater turns on and warms it; when the target is reached, the heater turns off. This is a balancing loop._

### 7.8 Delay

**Definition.** Time between a cause and its effect. Delays are the most common reason systems overshoot, oscillate or punish quick fixes: the system keeps correcting after the correction is already on its way.

**In Terser 2.** `lag` and an optional duration, placed after whatever is late.

```
inventory lowers orders lag raises inventory, balancing; lag 2 weeks, so swings around target
```

_Low inventory triggers orders, but deliveries arrive two weeks later, so inventory overshoots and swings around the target._

### 7.9 Stock (accumulation)

**Definition.** A quantity that accumulates over time: water in a tank, money in an account, people in a population, trust in a relationship. Stocks are a system's memory. They change only through flows, which is why they create inertia and buffers.

```
tank level stock
```

### 7.10 Flows: inflow and outflow

**Definition.** Rates that fill or drain a stock. The **net flow**, inflow minus outflow, decides whether the stock rises, falls or holds steady.

```
tank level stock, inlet inflow, drain outflow
```

_The tank level is a stock. The inlet fills it and the drain empties it. It rises while inflow exceeds outflow and falls while outflow exceeds inflow._

### 7.11 Conserved flow between stocks (aging chain)

**Definition.** One stock's outflow is another stock's inflow, so material moves through stages without being created or lost.

```
juniors stock, hiring inflow, promotion outflow; seniors stock, promotion inflow, retirement outflow
```

_Promotion drains juniors and fills seniors._

### 7.12 Stock-dependent flow (stocks inside loops)

**Definition.** A flow whose rate depends on the stock it feeds or drains. This is how stocks take part in feedback: interest grows with the balance, and deaths grow with the population.

```
account balance stock, deposits inflow, withdrawals outflow, fees outflow; each month: balance raises interest, interest inflow
```

### 7.13 Dynamic equilibrium

**Definition.** A stock holds steady because inflow equals outflow, even though material keeps moving.

```
lake stock, river inflow, evaporation outflow; lake raises evaporation lowers lake, balancing at river rate
```

### 7.14 Threshold and tipping point

**Definition.** A level past which behaviour changes qualitatively: a rule switches on, or a loop changes dominance. When the change cannot be reversed, it is a *tipping point*.

```
temperature over 30: fan on
temperature lowers ice raises reflection lowers temperature, runaway; temperature over threshold: ice gone, no return
```

_Warming melts ice, less ice reflects less sunlight, and that warms further: a runaway loop. Past the threshold the ice is gone for good._

### 7.15 Process and sequence

**Definition.** An ordered set of steps that transform inputs into outputs. Each step depends on the one before.

```
collect data, clean, analyze, publish results
idea to draft to review to publish
```

The first is a sequence of **actions**. The second is a **path** of stages.

### 7.16 Decision, branch and routing

**Definition.** A point where flow is routed down one of several paths depending on a condition.

```
check requests; valid: process, else reject, tell sender
```

### 7.17 Concurrency: parallel split and join

**Definition.** Work divides into branches that run at the same time. A join waits until all of them are complete.

```
release parallel docs, tests, build; all done: ship
```

### 7.18 Iteration, retry and limits

**Definition.** A step repeats until it succeeds or a limit is reached. The limit stops the loop and usually escalates.

```
try job; fail: wait, retry; 3 fails: human review
```

### 7.19 Rework and return flow

**Definition.** Output that fails a check flows back upstream to be redone. Rework loops are a hidden source of delay and cost.

```
tasks to work to review; errors: back to work
```

### 7.20 Schedule and periodic events

**Definition.** Actions or flows triggered by time rather than by state.

```
each day: backup
each month: balance raises interest, interest inflow
```

### 7.21 Hierarchy and subsystems

**Definition.** Systems are made of subsystems, which are made of their own subsystems. Each level has its own behaviour and boundary.

```
company (sales, product (design to build), support)
city (water (pumps to pipes), power (plant to grid))
```

### 7.22 Loop dominance

**Definition.** When several loops act on the same variable, behaviour depends on which one is strongest at the time. A shift in dominance produces S-curves, peaks and collapses.

**In Terser 2.** State each loop in its own clause, then the outcome:

```
births raises population raises births, runaway; population lowers rations lowers deaths lowers population, balancing at capacity
```

The runaway loop dominates at first and the balancing loop takes over near capacity. Together they make an S-curve.

---

## 8. How the concepts combine

The 11 keywords combine into several families of model. Every model in the table below is written in the same language and can be mixed into the others.

| Model family | Constructs used | Typical diagram it replaces |
|---|---|---|
| **Causal loop models** | `raises`, `lowers`, `runaway`, `balancing`, `lag` | causal loop diagram (CLD) |
| **Stock-and-flow models** | `stock`, `inflow`, `outflow`, plus loops | stock-and-flow diagram |
| **Control systems** | `vs`, conditions, `balancing at`, `lag` | control or feedback block diagram |
| **Process flows** | sequences, `to`, conditions, `else` | flowchart |
| **Workflows** | `parallel`, `all done:`, `back to`, counts | BPMN or activity diagram |
| **Architectures** | `( )` containment, `to` paths | system or context diagram |
| **Hybrid models** | all of the above in one text | several diagrams at once |

The power of the language is that these families mix in one text. A factory can be described as an architecture, a process, a rework loop and a capacity stock in a single sentence.

---

## 9. System archetypes

*System archetypes* are the classic recurring structures of systems thinking, as catalogued by Senge, Meadows and Kim. Each one below gives its structure, the Terser 2 form and how it reads.

### 9.1 Limits to growth

**Structure.** A reinforcing loop drives growth until a balancing loop, triggered by some limit, slows it down. The result is S-shaped growth.

```
births raises population raises births, runaway; population lowers rations lowers deaths lowers population, balancing at capacity
```

**Business version:**

```
demand raises sales raises demand, runaway; demand raises backlog lowers quality raises demand, balancing
```

### 9.2 Fixes that fail

**Structure.** A quick fix relieves the symptom (balancing), but its side effects, after a delay, make the problem worse (reinforcing).

```
problem raises fix lowers problem, balancing; problem raises fix raises side effects lag raises problem, runaway
```

_The fix lowers the problem now; through its side effects it raises the problem later._

### 9.3 Shifting the burden

**Structure.** A symptomatic fix competes with a slower fundamental solution. Relying on the quick fix weakens the capacity for the real one.

```
problem raises quick fix lowers problem, balancing; problem raises real fix lag lowers problem, balancing; quick fix raises reliance lowers real fix
```

### 9.4 Eroding goals

**Structure.** When the gap won't close, pressure lowers the goal instead of raising performance.

```
goal vs actual; gap raises action raises actual lowers gap, balancing; gap raises pressure lowers goal raises gap, balancing; so goal drifts down
```

### 9.5 Escalation

**Structure.** Each party's action is a threat to the other, who responds in kind. Two balancing intentions form one runaway loop.

```
our arms raises their fear raises their arms raises our fear raises our arms, runaway
```

### 9.6 Success to the successful

**Structure.** Two parties compete for a shared resource. Early success earns more resources, which brings more success, at the other party's expense.

```
our share raises our resources raises our success raises our share, runaway; our resources lowers their resources
```

### 9.7 Tragedy of the commons

**Structure.** Each user's growth loop draws on a shared stock. The stock's regeneration loop responds too late.

```
grass stock, regrowth inflow, grazing outflow; each herder: herd raises profit raises herd, runaway; herds raises grazing lowers grass raises yield lag raises herds, balancing; lag long: grass collapses
```

### 9.8 Growth and underinvestment

**Structure.** Growth hits a capacity limit. Investment in capacity could relieve it, but the investment is delayed or withheld, so growth stalls.

```
demand raises sales raises demand, runaway; demand raises backlog lowers quality raises demand, balancing; backlog raises investment lag raises capacity lowers backlog, balancing; investment late: growth stalls
```

### 9.9 Overshoot and collapse

**Structure.** A reinforcing loop draws down a stock faster than it regenerates. Without a timely balancing loop, the stock collapses.

```
fish stock, births inflow, catch outflow; fleet raises catch raises profit raises fleet, runaway; catch over births: fish falls, collapse
```

### 9.10 Oscillation (delayed balancing)

**Structure.** A balancing loop with a long delay keeps correcting after it should stop, so it overshoots both ways.

```
inventory lowers orders lag raises inventory, balancing; lag 2 weeks, so swings around target
```

---

## 10. Systems from other fields

### Ecology: predator and prey

```
rabbits raises rabbit births raises rabbits, runaway; rabbits raises foxes lag lowers rabbits, balancing; so both swing
```

_Rabbits breed (runaway). More rabbits feed more foxes, which later eat more rabbits (balancing, delayed). Both populations oscillate._

### Epidemiology: the SIR model

```
susceptible stock, infection outflow; infected stock, infection inflow, recovery outflow; recovered stock, recovery inflow; infected raises infection raises infected, runaway; infection lowers susceptible raises infection, balancing; so infected rises, peaks, falls
```

_Three stocks linked by two flows. Contagion is a runaway loop, and the depletion of susceptible people is a balancing loop. Together they make the epidemic curve._

### Climate: ice-albedo feedback

```
temperature lowers ice raises reflection lowers temperature, runaway; temperature over threshold: ice gone, no return
```

### Economics: market price

```
demand exceeds supply: price rises; price lowers demand raises price, balancing at equilibrium; price raises supply lag lowers price, balancing at equilibrium
```

### Finance: compound interest

```
account balance stock, deposits inflow, withdrawals outflow, fees outflow; each month: balance raises interest, interest inflow
```

### Supply chain: the bullwhip effect

```
shop to wholesaler to factory; each stage: orders vs stock, lag 1 week; so swings grow upstream
```

### Software: a queue with backpressure

```
requests to queue to workers to storage; queue full: reject; queue raises wait lowers requests raises queue, balancing
```

### Software: a CI/CD pipeline

```
commit to build to tests; tests fail: back to author, else deploy
```

### Software: fan-out and fan-in

```
job parallel shard 1, shard 2, shard 3; all done: merge, report
```

### Operations: manufacturing with rework

```
parts from suppliers to factory (intake to assembly to inspection) to customers; defects back to assembly
```

### Projects: the rework spiral

```
tasks to work to review; errors: back to work; errors raises rework raises pressure raises errors, runaway
```

### Organisations: structure and incentives

```
company (sales, product (design to build), support); reward raises effort raises results raises reward, runaway
```

### People: a learning habit

```
practice raises skill raises confidence raises practice, runaway
```

### Reliability: retry with escalation

```
try job; fail: wait, retry; 3 fails: human review
```

---

## 11. Behaviour over time

The structures in Terser 2 produce a small set of characteristic behaviours. The outcome words on the right are ordinary English, used idiomatically after `so`.

| Behaviour | Structure that produces it | Outcome words |
|---|---|---|
| Exponential growth or decline | a dominant `runaway` loop | `runaway forever`, `grows`, `spirals` |
| Goal-seeking | a dominant `balancing at X` loop | `settles`, `reached` |
| Oscillation | `balancing` + `lag` | `swings`, `swings around target` |
| S-shaped growth | `runaway`, then `balancing at capacity` | `levels off` |
| Overshoot and collapse | `runaway` draining a slow-renewing `stock` | `collapse`, `crashes` |
| Peak and decline | `runaway` + depletion `balancing` | `rises, peaks, falls` |
| Equilibrium | `inflow` equals `outflow` | `holds`, `steady` |
| Tipping point | threshold condition + `runaway` | `no return` |

---

## 12. Limits of the language

Terser 2 is deliberately small. These things are outside its core and are expressed with content words when needed:

- **Link strength and functional form.** `raises` says direction, not size. For nonlinearity, use a threshold: `price over 100: demand falls fast`.
- **Probability and uncertainty.** Use content words: `rarely`, `maybe`.
- **Units.** Use content words: `lag 2 weeks`, `3 fails`, `30 degrees`.
- **Variables shared across clauses.** An element is identified by its name, so keep names exact. `account balance` and `balance` are only treated as the same element when the meaning is obvious.
- **Several goals for one loop.** Write one `balancing at` loop per goal.
- **Keywords inside names.** `to` and `back to` cannot appear inside an element's name (§6, style rule 5).

---

## 13. Quick reference card

```
LINKS     A raises B        same direction          A lowers B       opposite direction
LOOPS     A ... A, runaway  even number of lowers   A ... A, balancing [at goal]   odd number
TIME      lag [2 weeks]     delay                   each day: Y      schedule
STOCKS    X stock, A inflow, B outflow
PATHS     A to B to C       C back to A             from A to X (P to Q) to B
STEPS     a, b, c           in order                parallel a, b; all done: c
CHOICE    X: Y, else Z      threshold, count, state, or vs-result
COMPARE   A vs B; below: Y; over: Z
NEST      X (A, B)          X (A to B)
CLAUSES   ;  between independent statements
```

Every sentence in this document passes the language checker (`tools/arena.py` word and punctuation rules) and a loop validator, which checks that each loop closes on its first word and that its tag matches the parity of its `lowers`.
