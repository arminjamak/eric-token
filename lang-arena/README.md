# Lang Arena: a literal language for systems thinking

Two designer agents compete to build a constructed language made only of plain written English words. It describes systems: loops, flows, stocks, delays, branches, parallel paths and nested subsystems. The guiding principle is **less but more**. Read aloud, a sentence should sound like someone speaking with extreme concision: literal concepts and no filler.

| Agent | Bias |
|---|---|
| **A: Learnability-first** | Easy to learn and readable cold. Concision comes second. |
| **B: Concision-first** | As short as possible. Learnability comes second. |

## Round protocol

1. **Build.** Both designers work in parallel. Each one stops when it declares a **milestone** by writing `rounds/rN/<A|B>/language.json`. Neither is scored until both have finished.
2. **Test.** For each language, four blind testers run:
   - a **cold reader** sees only the 10 translated sentences, with no spec, and decodes them into English;
   - a **spec learner** reads the generated `spec.md`, decodes the same 10 sentences, then **encodes** 4 held-out systems that the designers never saw.
3. **Judge.** A judge grades every decoding against the benchmark's atomic facts. It grades every encoding for fact coverage and for rule validity. Languages are shown to it under shuffled labels.
4. **Score.** `tools/arena.py score` combines the results into a score out of 100.
5. **Next version.** The winning language becomes the shared base for the next round. Both agents fork it and keep their own bias.
6. **Stop.** The arena ends when either agent fails to raise its own total by **at least 6 points** over its previous round. There is a safety cap of 8 rounds.

## Score: 100 points

**Concision: 50 points.** `50 × compression × fidelity`

- `length_ratio = ½·(words_lang / words_english) + ½·(chars_lang / chars_english)` over the 10 benchmark items.
- Each hyphenated part counts as a word. Each `. , : ; ( )` counts as half a word, so punctuation cannot become free syntax.
- `compression = clamp((1 − length_ratio) / 0.7, 0, 1)`. Text that is 70% shorter than plain English earns full marks.
- `fidelity` is the spec learner's decode accuracy. Shortness that loses meaning earns nothing.

**Learnability: 50 points.**

- 15 × cold-read accuracy: does it make literal sense with no spec?
- 15 × spec-decode accuracy.
- 10 × encode quality: mean of (fact coverage × rule validity) on the held-out systems.
- 10 × economy: `clamp((70 − core_size) / 55, 0, 1)`, where `core_size = lexicon entries + rules`. A core of 15 or fewer earns full marks.

**Hard constraints.** These are checked by `arena.py check`, and any violation halves the score:

- Only letters, digits, spaces and `. , : ; ( ) ' -` are allowed.
- Every word must be a recognised English word.
- The spec is generated from the JSON, and each field has a length cap, so a language cannot hide rules in prose.

## Layout

```
benchmark/benchmark.json   public benchmark (10 systems + atomic facts)
benchmark/heldout.json     held-out encode set (published after the arena ends)
tools/arena.py             check / render / score
rounds/rN/{A,B}/           language.json, notes.md, spec.md, tester packets and outputs
rounds/rN/judge.json       judge grades
rounds/rN/score.md         round scoreboard
RESULTS.md                 full history and final language
```
