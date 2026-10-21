#!/usr/bin/env python3
"""Vocabulary loop: descriptiveness vs word length for Terser's core words.

  vocab.py packets <iter_dir>   # candidates.json -> 4 blind rater packets (shuffled, 2 option wordings)
  vocab.py score   <iter_dir>   # rater_*.json -> leaderboard.json / leaderboard.md + champion set

fitness = D - 0.03 * max(0, chars - 3)
D = mean over raters of (1 if the rater picked the right meaning else 0) * confidence / 3
"""
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from arena import is_english  # noqa: E402

HERE = Path(__file__).resolve().parent
MEANINGS = json.loads((HERE / "meanings.json").read_text())["meanings"]
IDS = [m["id"] for m in MEANINGS]
LEN_COST = 0.03
N_RATERS = 4


def fitness(word, d):
    return d - LEN_COST * max(0, len(word) - 3)


def load_candidates(it):
    """candidates.json: {meaning_id: [word, ...]} merged from all proposers; validated + deduped."""
    raw = json.loads((it / "candidates.json").read_text())
    out, rejected = {}, []
    for mid in IDS:
        seen = []
        for w in raw.get(mid, []):
            w = " ".join(w.lower().split())
            ok = 0 < len(w) <= 12 and len(w.split()) <= 2 and all(is_english(p) for p in w.split())
            if not ok:
                rejected.append((mid, w))
            elif w not in seen:
                seen.append(w)
        out[mid] = seen
    return out, rejected


def packets(it):
    it = Path(it)
    cands, rejected = load_candidates(it)
    base = json.loads((it / "baseline.json").read_text())
    for m in IDS:  # the previous champions are always re-rated
        if base[m] not in cands[m]:
            cands[m].insert(0, base[m])
    (it / "candidates.json").write_text(json.dumps(cands, indent=1))
    words = sorted({w for ws in cands.values() for w in ws})
    for r in range(N_RATERS):
        rng = random.Random(1000 * int(it.name.lstrip("i") or 0) + r)
        opts = MEANINGS[:]
        rng.shuffle(opts)
        key = "d1" if r % 2 == 0 else "d2"
        ws = words[:]
        rng.shuffle(ws)
        lines = ["# Word meaning test", "",
                 "A new technical notation for describing systems reuses short English words as keywords.",
                 "For EACH keyword below, guess which ONE meaning (1-12) it most likely has, judging only by the word itself.",
                 "Several keywords may share a meaning. Give your confidence: 3 sure, 2 likely, 1 guessing.", "",
                 "## Meanings", ""]
        lines += [f"{i}. {m[key]}" for i, m in enumerate(opts, 1)]
        lines += ["", "## Keywords", ""] + [f"- {w}" for w in ws]
        (it / f"rater_{r}_packet.md").write_text("\n".join(lines) + "\n")
        (it / f"rater_{r}_key.json").write_text(json.dumps({str(i): m["id"] for i, m in enumerate(opts, 1)}))
    if rejected:
        print("rejected:", rejected)
    print(f"{len(words)} unique words across {len(IDS)} meanings")


def score(it):
    it = Path(it)
    cands, _ = load_candidates(it)
    ratings = []
    for r in range(N_RATERS):
        key = json.loads((it / f"rater_{r}_key.json").read_text())
        ans = json.loads((it / f"rater_{r}.json").read_text())
        ans = {" ".join(k.lower().split()): v for k, v in ans.items()}
        ratings.append((key, ans))
    board = {}
    for mid in IDS:
        rows = []
        for w in cands[mid]:
            hits = []
            for key, ans in ratings:
                a = ans.get(w)
                if not a:
                    hits.append(0.0)
                    continue
                picked = key.get(str(a.get("meaning")))
                hits.append((picked == mid) * max(1, min(3, int(a.get("confidence", 1)))) / 3)
            d = sum(hits) / len(hits)
            rows.append({"word": w, "D": round(d, 3), "chars": len(w), "fitness": round(fitness(w, d), 3)})
        rows.sort(key=lambda x: (-x["fitness"], x["chars"]))
        board[mid] = rows
    # champion set: greedy, distinct words, best fitness first
    champs, used = {}, set()
    for mid, row in sorted(((m, r) for m in IDS for r in board[m]), key=lambda t: -t[1]["fitness"]):
        if mid not in champs and row["word"] not in used:
            champs[mid] = row
            used.add(row["word"])
    total = round(sum(champs[m]["fitness"] for m in IDS if m in champs), 3)
    # previous champion set, re-rated in this iteration, so the comparison uses the same raters
    base = json.loads((it / "baseline.json").read_text())
    base_total = round(sum(next(r["fitness"] for r in board[m] if r["word"] == base[m]) for m in IDS), 3)
    gain = round(100 * (total - base_total) / abs(base_total), 2) if base_total else 0.0
    json.dump({"board": board, "champions": champs, "total": total, "baseline_total": base_total,
               "gain_pct": gain}, open(it / "leaderboard.json", "w"), indent=2)
    md = [f"# Leaderboard {it.name}", "",
          f"Champion-set fitness: **{total}**. Previous set, re-rated: {base_total}. Gain: **{gain}%**", "",
          "| meaning | champion | D | chars | fitness | runners-up |", "|---|---|---|---|---|---|"]
    for m in IDS:
        c = champs.get(m, {"word": "-", "D": 0, "chars": 0, "fitness": 0})
        ru = ", ".join(f"{r['word']} ({r['fitness']})" for r in board[m] if r["word"] != c["word"])
        md.append(f"| {m} | **{c['word']}** | {c['D']} | {c['chars']} | {c['fitness']} | {ru} |")
    (it / "leaderboard.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    {"packets": packets, "score": score}[sys.argv[1]](sys.argv[2])
