#!/usr/bin/env python3
"""Lang-arena harness: validate a language, render tester packets, score a round.

  arena.py check  <language.json>             # validity + concision/economy metrics (designers may run this)
  arena.py render <language.json> <out_dir>   # spec.md + cold/spec tester packets
  arena.py score  <round_dir>                 # combine metrics + judge.json -> score.json / score.md
"""
import json
import re
import sys
from pathlib import Path

from wordfreq import zipf_frequency

ROOT = Path(__file__).resolve().parent.parent
BENCH = json.loads((ROOT / "benchmark" / "benchmark.json").read_text())["items"]

ALLOWED = re.compile(r"^[A-Za-z0-9 .,:;()'\-\n]*$")
WORD = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z]+)?")
PUNCT = re.compile(r"[.,:;()]")
MIN_ZIPF = 2.0
CAPS = {"meaning": 20, "rule": 40, "example": 25, "reads_as": 30, "tagline": 25}


def is_english(w):
    w = w.lower()
    stems = [w] + [w[: -len(suf)] + add for suf, add in
                   (("ies", "y"), ("es", ""), ("s", ""), ("ed", ""), ("ed", "e"), ("ing", ""), ("ing", "e"))
                   if w.endswith(suf)]
    return any(zipf_frequency(x, "en") >= MIN_ZIPF for x in stems if x == w or len(x) > 1)


def nwords(s):
    return len(WORD.findall(s))


def text_cost(s):
    """Words (hyphen parts count separately) + 0.5 per structural punctuation mark."""
    return nwords(s) + 0.5 * len(PUNCT.findall(s))


def chars(s):
    return len(re.sub(r"\s+", " ", s.strip()))


def check(lang):
    errors = []
    for key in ("name", "tagline", "lexicon", "rules", "translations"):
        if key not in lang:
            errors.append(f"missing key: {key}")
    if errors:
        return {"errors": errors}

    if nwords(lang["tagline"]) > CAPS["tagline"]:
        errors.append("tagline too long")
    for e in lang["lexicon"]:
        if nwords(e["meaning"]) > CAPS["meaning"]:
            errors.append(f"lexicon '{e['word']}': meaning over {CAPS['meaning']} words")
        if nwords(e["word"]) > 3:
            errors.append(f"lexicon '{e['word']}': entries are at most 3 words")
    for i, r in enumerate(lang["rules"], 1):
        for f in ("rule", "example", "reads_as"):
            if nwords(r.get(f, "")) > CAPS[f]:
                errors.append(f"rule {i}: {f} over {CAPS[f]} words")

    bad_words = set()
    w_lang = c_lang = w_eng = c_eng = 0.0
    per_item = {}
    for item in BENCH:
        t = lang["translations"].get(item["id"], "")
        if not t.strip():
            errors.append(f"missing translation {item['id']}")
            continue
        if not ALLOWED.match(t):
            errors.append(f"{item['id']}: illegal characters {sorted(set(re.sub(r'[A-Za-z0-9 .,:;()\'\\-\\n]', '', t)))}")
        for w in WORD.findall(t):
            if w.isdigit():
                continue
            if not is_english(w):
                bad_words.add(w)
        wl, cl = text_cost(t), chars(t)
        we, ce = text_cost(item["english"]), chars(item["english"])
        per_item[item["id"]] = {"words": wl, "eng_words": we, "chars": cl, "eng_chars": ce}
        w_lang += wl; c_lang += cl; w_eng += we; c_eng += ce
    if bad_words:
        errors.append(f"not recognised as English words: {sorted(bad_words)}")

    ratio = 0.5 * (w_lang / w_eng) + 0.5 * (c_lang / c_eng) if w_eng else 1.0
    compression = max(0.0, min(1.0, (1 - ratio) / 0.7))
    n_core = len(lang["lexicon"]) + len(lang["rules"])
    economy = max(0.0, min(1.0, (70 - n_core) / 55))
    return {
        "errors": errors,
        "length_ratio": round(ratio, 4),
        "compression": round(compression, 4),
        "core_size": n_core,
        "economy": round(economy, 4),
        "words_lang": w_lang, "words_eng": w_eng,
        "chars_lang": c_lang, "chars_eng": c_eng,
        "per_item": per_item,
    }


def spec_md(lang):
    out = [f"# {lang['name']}", "", f"_{lang['tagline']}_", "", "## Core words", "",
           "| word | meaning |", "|---|---|"]
    out += [f"| `{e['word']}` | {e['meaning']} |" for e in lang["lexicon"]]
    out += ["", "## Rules", ""]
    for i, r in enumerate(lang["rules"], 1):
        out += [f"{i}. {r['rule']}", f"   - e.g. `{r['example']}`", f"   - reads as: {r['reads_as']}", ""]
    out += ["Any other English word is an ordinary content word (a thing, quantity, actor or action) with its usual meaning.", ""]
    return "\n".join(out)


def render(lang, out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "spec.md").write_text(spec_md(lang))
    sentences = "\n\n".join(f"[{i['id']}] {lang['translations'][i['id']]}" for i in BENCH)
    (out / "cold_packet.md").write_text(
        "# Ten system descriptions\n\nEach line describes one system in an unfamiliar, terse notation built from English words.\n\n"
        + sentences + "\n")
    (out / "spec_packet.md").write_text(spec_md(lang) + "\n---\n\n# Sentences to decode\n\n" + sentences + "\n")


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else 0.0


def score(round_dir):
    rd = Path(round_dir)
    judge = json.loads((rd / "judge.json").read_text())
    result = {}
    for agent in ("A", "B"):
        lang = json.loads((rd / agent / "language.json").read_text())
        m = check(lang)
        j = judge[agent]
        K = mean(j["cold"].values())          # cold-read accuracy (no spec)
        F = mean(j["spec"].values())          # decode accuracy with spec (fidelity)
        E = mean(v["coverage"] * v["validity"] for v in j["encode"].values())
        concision = 50 * m["compression"] * F
        learn = 15 * K + 15 * F + 10 * E + 10 * m["economy"]
        if m["errors"]:
            concision *= 0.5
            learn *= 0.5
        result[agent] = {
            "name": lang["name"],
            "cold_read": round(K, 4), "spec_decode": round(F, 4), "encode": round(E, 4),
            "compression": m["compression"], "length_ratio": m["length_ratio"],
            "core_size": m["core_size"], "economy": m["economy"], "errors": m["errors"],
            "concision_score": round(concision, 2), "learnability_score": round(learn, 2),
            "total": round(concision + learn, 2),
        }
    a, b = result["A"]["total"], result["B"]["total"]
    result["winner"] = "A" if a >= b else "B"
    (rd / "score.json").write_text(json.dumps(result, indent=2))
    rows = ["| | A | B |", "|---|---|---|"]
    for k in ("name", "length_ratio", "compression", "spec_decode", "cold_read", "encode", "core_size",
              "economy", "concision_score", "learnability_score", "total"):
        rows.append(f"| {k} | {result['A'][k]} | {result['B'][k]} |")
    (rd / "score.md").write_text("\n".join(rows) + f"\n\nWinner: **{result['winner']}**\n")
    print("\n".join(rows))
    print("winner:", result["winner"])


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "check":
        r = check(json.loads(Path(sys.argv[2]).read_text()))
        r.pop("per_item")
        print(json.dumps(r, indent=2))
    elif cmd == "render":
        render(json.loads(Path(sys.argv[2]).read_text()), sys.argv[3])
    elif cmd == "score":
        score(sys.argv[2])
