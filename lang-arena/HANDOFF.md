# Handoff: how to pick up and continue Lang Arena

Everything needed to continue this project is in this folder. This file covers what exists, how the machinery works, and how to resume. A ready-to-paste prompt for a new Claude Code session is at the end.

## 1. What this project is

Two AI designer agents competed to build a constructed language made of plain English words for describing systems: loops, flows, stocks, delays, branches, parallel work and subsystems. The guiding principle was **less but more**: literal concepts, no filler.

- **Agent A** put learnability first. **Agent B** put concision first.
- Each round: both designers reach a milestone → blind testers decode and encode → a blind judge grades → `tools/arena.py` scores out of 100 (50 concision, 50 learnability).
- The round winner becomes the base for both designers in the next round.
- **Stopping rule:** the arena ends when either agent fails to beat its *own* previous total by at least 6 points.
- A **vocabulary loop** then optimised each keyword for descriptiveness against word length.

## 2. Current state

**Current language: Terser 2.** The one-page guide is `TERSER.md`, the full reference is `LANGUAGE.md`, and the machine-readable definition is `rounds/r3/B/language.json`.

| Stage | Result |
|---|---|
| Arena round 1 | B "Terse" 87.28 beat A "Plain Loop" 77.86 |
| Arena round 2 | B "Terser" 93.12 beat A "Terse Plain" 89.33. B gained only +5.84, so **the arena stopped** |
| Balance check | Terser was best on concision × learnability (min, product and harmonic mean) |
| Vocabulary loop | i1 +48.8%, i2 +3.6%, so the loop stopped. Words changed: lift→raises, cut→lowers, grows→runaway, seeks→balancing, in/out→inflow/outflow, split→parallel |
| Round 3 (validation) | Terser 2 93.83 beat Terser 93.48 (learnability 49.75 vs 48.38) |
| Reference doc | `LANGUAGE.md`: 22 concepts, 10 archetypes, cross-field examples. All examples pass `orchestration/run.py validate` |

## 3. File map

```
README.md                 arena rules and scoring formula
HANDOFF.md                this file
TERSER.md                 one-page Terser 2 guide
LANGUAGE.md               full language reference
RESULTS.md                arena history, scoreboards, known weak spots
benchmark/benchmark.json  10 public benchmark systems + atomic facts (used for scoring)
benchmark/heldout.json    4 held-out encode systems. PUBLISHED, so designers can see them now (see §6)
tools/arena.py            check | render | score: the scoring engine
orchestration/run.py      every step between agent spawns (prompts, packets, blind maps, scoring, stop rule)
orchestration/prompts/    prompt templates for designer, cold reader, spec learner, judge, vocab proposer and rater
rounds/rN/{A,B}/          language.json, notes.md, spec.md (what testers saw), tests/ (tester outputs)
rounds/rN/                judge.json, blind_map.json, score.json, score.md, feedback.md
rounds/r3/                validation round: A = Terser (control), B = Terser 2
vocab/meanings.json       the 12 core meanings + incumbent words
vocab/vocab.py            packets | score for the vocabulary loop
vocab/iN/                 proposals, candidates, rater packets/answers, leaderboard.md
vocab/RESULTS.md          vocabulary loop write-up
```

## 4. Setup

```bash
python3 --version            # 3.12 or newer (arena.py uses PEP 701 f-strings)
pip install wordfreq         # used to check that every word is real English
export ARENA_WORK=~/arena-work   # private scratch area; designers must never see it
mkdir -p "$ARENA_WORK"
python3 tools/arena.py check rounds/r3/B/language.json   # should print errors: [] and length_ratio 0.3829
```

## 5. How to run things

Agents are spawned by whoever drives the arena. In this project that was a Claude Code session using its Agent tool. Each agent gets a one-line prompt: *"Read your full instructions from `<prompt file>` and follow them exactly."* `orchestration/run.py` writes those prompt files and handles everything between spawns.

### 5.1 An arena round N

| Step | Command / action | Agents (models used so far) |
|---|---|---|
| 1 | `python3 orchestration/run.py designers N` | spawn 2 designers on `$ARENA_WORK/prompts/rN_A.md` and `rN_B.md`. Default model. **Wait for both to report MILESTONE.** |
| 2 | `python3 orchestration/run.py prep N` | spawn 4 testers: a cold reader and a spec learner for each of A and B (`$ARENA_WORK/rN/{A,B}/{cold,spec}_prompt.md`). Sonnet in r1–r2, Haiku in r3. |
| 3 | `python3 orchestration/run.py collect N` | spawn 1 judge on `$ARENA_WORK/rN/judge/judge_prompt.md`. Default model in r1–r2, Sonnet in r3. |
| 4 | `python3 orchestration/run.py score N` | prints the scoreboard and the 6-point check. Add `--publish` once the arena is over to include held-out encodings. |
| 5 | write `rounds/rN/feedback.md` | summarise the judge's comments **without** held-out specifics. |
| 6 | commit | if both agents gained ≥ 6, go to round N+1. Otherwise stop. |

To change the comparison, edit `rounds/rN/{A,B}/language.json` directly before `prep` (round 3 did this for validation).

### 5.2 A vocabulary loop iteration N

| Step | Command / action | Agents |
|---|---|---|
| 1 | `python3 orchestration/run.py vocab-propose N` | spawn 2 Haiku proposers (`vocab_iN_prop_L.md`, `vocab_iN_prop_S.md`) |
| 2 | `python3 orchestration/run.py vocab-rate N` | spawn 4 Haiku raters (`vocab_iN_rater_{0..3}.md`) |
| 3 | `python3 vocab/vocab.py score vocab/iN` | continue while `gain_pct` ≥ 6 |

Fitness = D − 0.03 × (letters − 3), where D is the confidence-weighted rate of correct blind guesses from the word alone. A champion replaces a keyword only if it also fits the keyword's sentence frame. That is why `to`, `back to` and `vs` survived (see `vocab/RESULTS.md`).

### 5.3 Checking sentences

```bash
python3 orchestration/run.py validate examples.txt    # one sentence per line
```

This checks allowed characters, real English words, loop closure (the chain ends on its first word) and parity (an even count of `lowers` means `runaway`, odd means `balancing`). It **cannot** check that each `raises`/`lowers` matches reality, so read link polarity by hand.

## 6. Things to know before continuing

- **The held-out set is burned.** `benchmark/heldout.json` was published after the arena ended, so future designers can read it. Before another arena round, write 4 fresh systems in the same format (`{"items":[{"id":"h1","english":...,"facts":[...]}]}`) to `$ARENA_WORK/heldout.json`, outside this folder. `run.py` uses that file automatically.
- **Learnability is near its ceiling** with LLM testers: cold reads score 0.98 to 1.00. Haiku testers discriminate better than Sonnet. Consider several cold readers per language and averaging them, since one reader per round is noisy (margins of 0.3 points are within noise).
- **Interpretations made** (from the original request):
  - "6% or more added up score" means each agent must gain ≥ 6 of 100 points over its own previous total.
  - "Next version based on the winning principle" means both agents fork the round winner and keep their own bias.
  - There is a safety cap of 8 rounds.
- **Hard constraints:** only letters, digits, spaces and `. , : ; ( ) ' -`; every word must be real English (wordfreq zipf ≥ 2.0, with simple stemming); hyphen parts count as separate words; each punctuation mark counts as half a word.

## 7. Open ideas

1. **Test the parity tip.** The "count the lowers" hint is in `TERSER.md` and `LANGUAGE.md` but not in the tested spec (`rounds/r3/B/language.json`). Add it as a rule and run a validation round.
2. **Run the vocabulary loop on rule-level words.** `else`, `so`, `both done`/`all done` and the outcome words (`swings`, `levels off`) have not been optimised.
3. **Harder benchmark.** Use multi-loop systems with 3 or more interacting loops, nested delays and stocks inside subsystems, to separate the languages again.
4. **Human testing.** Give `TERSER.md` to people and time how long it takes them to read and write it.
5. **A parser.** Turn Terser 2 into causal-loop or stock-and-flow diagrams automatically. The grammar in `LANGUAGE.md` §4 is regular enough.

## 8. Resume prompt for a new Claude Code session

> I'm continuing the Lang Arena project in `lang-arena/`. Read `lang-arena/HANDOFF.md` first, then `README.md`, `TERSER.md` and `RESULTS.md`. Set up per §4 (`pip install wordfreq`, `ARENA_WORK=~/arena-work`). Then [run another arena round starting from Terser 2 / run vocabulary-loop iteration 3 / test the parity-tip rule / …]. Use `orchestration/run.py` for every step between agent spawns, spawn agents with one-line "read your instructions from <file>" prompts, wait for all agents in a stage before moving on, and commit after each stage.
