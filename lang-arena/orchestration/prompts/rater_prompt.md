You are a BLIND RATER. Follow these steps exactly.

Step 1. Read ONLY this file: {PACKET}. Do not open any other file.
Step 2. For every keyword listed under "## Keywords", decide which ONE numbered meaning it most likely has, judging only by the word itself. Also give a confidence: 3 = sure, 2 = likely, 1 = guessing. Rate every keyword, with no skipping, and judge each word on its own.
Step 3. Write ONLY a JSON object to {OUT}, with one entry per keyword, using the keyword exactly as written:
{"keyword one": {"meaning": 4, "confidence": 2}, "keyword two": {"meaning": 11, "confidence": 3}}
Step 4. Check that it parses and contains every keyword: python3 -c "import json;d=json.load(open('{OUT}'));print(len(d))". The count must equal the number of keywords in the packet. Then reply "done".
