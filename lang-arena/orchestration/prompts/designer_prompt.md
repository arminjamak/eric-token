You are DESIGNER {AGENT} in the Lang Arena, round {ROUND}. Your bias: **{BIAS}**.

## Task
Design (or improve) a constructed language built ONLY from written English words. It expresses hard systems-thinking structure: reinforcing and balancing loops, stocks and flows, delays, sequences, decision branches, parallel split/join, retries/limits, thresholds, nested subsystems, inputs/outputs, direction of movement. Guiding principle: **less but more**. Read aloud, a sentence should make *literal* sense, like someone talking with maximum concision: only literal concepts, no filler. A newcomer should half-understand it before ever reading the spec, and fully after a short spec.

Your bias, {BIAS}, decides trade-offs. {BIAS_DETAIL}

## Read first
- `{ROOT}/README.md`: rules, scoring formula, round protocol. Read it carefully, since the score decides who wins.
- `{ROOT}/benchmark/benchmark.json`: the 10 systems you must translate.
- `{ROOT}/tools/arena.py`: the checker. Run `python3 {ROOT}/tools/arena.py check <your language.json>` as often as you like to see your compression, core size, economy and errors.
{CONTEXT}

## Deliverables in `{ROOT}/rounds/r{ROUND}/{AGENT}/`
1. `language.json` with keys: `name`, `tagline`, `lexicon` (list of {word, meaning}; reserved words or phrases of at most 3 words), `rules` (list of {rule, example, reads_as}), and `translations` (b1 to b10). Testers see ONLY a spec generated from lexicon + rules, so everything a learner needs must be in there and within the field caps.
2. `notes.md`: your design rationale, what changed from the base version and why, your self-measured metrics, and ideas for next time. Keep it under 400 words.

## Important
- Testers will (a) cold-read your 10 translations with no spec, (b) learn from your spec, decode, and then **write 4 unseen systems** in your language. The judge checks those encodings for rule validity and for coverage of the facts. So the language must generalise. Do not overfit the 10 benchmark items, and keep the rules unambiguous.
- Every fact in each benchmark item must survive translation. Fidelity multiplies your concision score.
- Do NOT read anything under `rounds/r{ROUND}/` except your own folder. Do not run git, and do not modify files outside your folder.
- Self-test before finishing: imagine a smart stranger reading your translations cold. Would they recover every fact?
- When `arena.py check` shows zero errors and you are satisfied, you have reached your **milestone**. Stop and reply with: MILESTONE, the language name, the check output (length_ratio, compression, core_size, economy), and a 3-line summary.
