You are the JUDGE for round {ROUND} of a constructed-language test. Two languages appear under blind labels X and Y. Grade them strictly, consistently and identically. You do not know which designer made which, and you must not try to find out: do not open {ROOT}.

Read these files in {DIR}:
- benchmark.json: the 10 benchmark systems (b1 to b10). Each has an `english` original and a `facts` list.
- heldout.json: the 4 held-out systems (h1 to h4), with their facts.
- For L in X and Y: L/spec.md (the language spec), L/cold.md (a cold reader's decoding with no spec) and L/spec_learner.md (a learner's decoding with the spec, plus their encodings of h1 to h4).

Grading:
1. Decodings: for each of cold.md and spec_learner.md and each item bN, grade every fact in that item's `facts` list in order. Use 1 if clearly and correctly conveyed (a correct "(guess)" counts), 0.5 if partial or vague, and 0 if missing or wrong. Also count `wrong`: the number of confident claims that contradict the original, such as a wrong loop type, wrong direction or wrong order. Plausible elaborations are not wrong.
2. Encodings (spec_learner.md, h1 to h4): `facts` is a 1/0.5/0 vector for the held-out facts, judged by reading the encoding through the spec. `validity` is 1 if it follows the spec's rules and lexicon correctly, 0.5 if there are minor deviations or improvised constructs, and 0 if it mostly ignores the spec.

Write `{DIR}/judge_blind.json` with exactly this shape:
{"X": {"cold": {"b1": {"facts": [..], "wrong": 0}, ... "b10": ...},
       "spec": {"b1": {"facts": [..], "wrong": 0}, ...},
       "encode": {"h1": {"facts": [..], "validity": 1}, ...},
       "comments": "<=60 words: main strengths and failure modes"},
 "Y": {...same...}}
Each facts vector must have exactly as many entries as that item's facts list. Then validate it, for example with python3 -c "import json;json.load(open(...))". Reply "done" plus one line per language with your overall impression.
