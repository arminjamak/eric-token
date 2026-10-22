You are a VOCABULARY PROPOSER. Follow these steps exactly. Your style is {STYLE}.

Context: "Terser" is a notation for describing systems. It reuses English words as keywords. We want each keyword to be **as self-explanatory as possible**, so that a stranger guesses its meaning from the word alone, while also being **as short as possible**. Fitness = D - 0.03 per character over 3, where D is how often blind raters guess the meaning correctly from the word alone, weighted by their confidence.

Step 1. Read {ROOT}/vocab/meanings.json. It lists 12 meanings, each with an id, the current word ("incumbent"), a usage frame ("frame") and two descriptions.
Step 2. {HISTORY}
Step 3. For EACH of the 12 meaning ids, propose exactly 5 NEW candidate keywords. Rules:
  - Each candidate is a real, common English word, or a 2-word phrase only if no single word works. At most 12 characters.
  - It must read naturally in its frame. For example, for POS, "A ___ B" with the candidate filled in should read as plain English.
  - It must clearly differ from the other meanings' words. In particular, POS and NEG should be a natural opposite pair, IN and OUT should be a pair, and REINF and BAL should be clearly distinguishable.
  - Avoid symbols, abbreviations and made-up words.
  - {STYLE_RULE}
Step 4. Write ONLY this JSON to {OUT}:
{"POS": ["w1","w2","w3","w4","w5"], "NEG": [...], "REINF": [...], "BAL": [...], "CMP": [...], "FLOW": [...], "BACK": [...], "DELAY": [...], "STOCK": [...], "IN": [...], "OUT": [...], "SPLIT": [...]}
Step 5. Check that the file parses: python3 -c "import json;json.load(open('{OUT}'))". Then reply "done".
Do not read or modify any other files.
