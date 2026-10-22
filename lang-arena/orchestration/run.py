#!/usr/bin/env python3
"""Lang-arena orchestration: everything between "spawn an agent" steps.

The agents themselves (designers, testers, judge, vocab proposers and raters) are spawned
by whoever drives the arena, e.g. a Claude Code session using its Agent tool. This script
writes their prompt files and moves their outputs around. See ../HANDOFF.md for the loop.

Paths:
  ROOT  = this lang-arena folder (auto-detected)
  WORK  = $ARENA_WORK, default ~/arena-work. A private scratch area that designers never see:
          tester packets, blind judge files, the held-out set.
  HELDOUT = $ARENA_HELDOUT, default WORK/heldout.json, then benchmark/heldout.json (published,
          so designers may have seen it; write a fresh one for new rounds).

Arena round N:
  run.py designers N            -> WORK/prompts/rN_A.md, rN_B.md  (spawn 2 designer agents)
  run.py prep N                 -> tester prompts in WORK/rN/{A,B}/ (spawn 4 tester agents)
  run.py collect N              -> judge prompt in WORK/rN/judge/  (spawn 1 judge agent)
  run.py score N [--publish]    -> rounds/rN/score.md + stopping-rule check
Vocabulary loop iteration N:
  run.py vocab-propose N        -> WORK/prompts/vocab_iN_prop_{L,S}.md (spawn 2 proposers)
  run.py vocab-rate N           -> WORK/prompts/vocab_iN_rater_{0..3}.md (spawn 4 raters)
  python3 vocab/vocab.py score vocab/iN
Checks:
  run.py validate FILE          -> loop closure + parity + word rules, one sentence per line
"""
import json
import os
import random
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = Path(os.environ.get("ARENA_WORK", Path.home() / "arena-work")).resolve()
PROMPTS = ROOT / "orchestration" / "prompts"
PY = sys.executable
STOP_GAIN = 6.0  # points out of 100 an agent must gain on its own previous total

BIAS = {
    "A": ("learnability first, concision second",
          "When ease of learning and shortness conflict, choose ease of learning: common words, transparent literal "
          "meanings, few rules, readable cold. But every word still has to earn its place."),
    "B": ("concision first, learnability second",
          "When shortness and ease of learning conflict, choose shortness: dense structural words, minimal tokens and "
          "characters. But stay within plain English words and keep literal sense, because an unreadable language "
          "fails on fidelity and learnability."),
}


def fill(template, **kw):
    t = (PROMPTS / template).read_text()
    for k, v in {"ROOT": str(ROOT), "WORK": str(WORK), **kw}.items():
        t = t.replace("{" + k + "}", str(v))
    return t


def heldout_path():
    p = Path(os.environ.get("ARENA_HELDOUT", WORK / "heldout.json"))
    if p.exists():
        return p
    print("warning: using the published benchmark/heldout.json; designers can see it. "
          "Write a fresh held-out set to WORK/heldout.json for new rounds.", file=sys.stderr)
    return ROOT / "benchmark" / "heldout.json"


def arena(*args):
    subprocess.run([PY, str(ROOT / "tools" / "arena.py"), *map(str, args)], check=True)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    print("wrote", path)


# ---------------------------------------------------------------- arena rounds

def designers(n):
    n = int(n)
    for ag in "AB":
        (ROOT / "rounds" / f"r{n}" / ag).mkdir(parents=True, exist_ok=True)
    if n == 1:
        prev = None
        ctx = "- Round 1: there is no base version. Design from scratch."
    else:
        prev = json.loads((ROOT / "rounds" / f"r{n-1}" / "score.json").read_text())
        base, p = prev["winner"], n - 1
        ctx = (f"- **Round {n}: you are NOT starting from scratch.** The round {p} winner is "
               f"`rounds/r{p}/{base}/language.json`, and it is the shared base for both designers. Copy it into your "
               "folder and improve it, guided by your bias. You may restructure it freely, but explain every change in notes.md.\n"
               f"- Study round {p}: `rounds/r{p}/score.md`, `rounds/r{p}/feedback.md`, both designers' `notes.md`, and the "
               f"tester outputs in `rounds/r{p}/A/tests/` and `rounds/r{p}/B/tests/`. You may read every earlier round folder.\n"
               "- **Stopping rule:** the arena ends if either designer fails to beat its OWN previous total by at least "
               f"{STOP_GAIN:g} points. Your previous total was {{PREV}}, so you need at least {{TARGET}}.")
    for ag in "AB":
        c = ctx if prev is None else ctx.replace("{PREV}", f"{prev[ag]['total']:.2f}").replace(
            "{TARGET}", f"{prev[ag]['total'] + STOP_GAIN:.2f}")
        text = fill("designer_prompt.md", CONTEXT=c, ROUND=n, AGENT=ag, BIAS=BIAS[ag][0], BIAS_DETAIL=BIAS[ag][1])
        write(WORK / "prompts" / f"r{n}_{ag}.md", text)


def prep(n):
    n = int(n)
    rd, wd = ROOT / "rounds" / f"r{n}", WORK / f"r{n}"
    mapping = {"X": "A", "Y": "B"} if random.random() < 0.5 else {"X": "B", "Y": "A"}
    write(wd / "map.json", json.dumps(mapping))
    held = json.loads(heldout_path().read_text())["items"]
    jd = wd / "judge"
    jd.mkdir(parents=True, exist_ok=True)
    shutil.copy(ROOT / "benchmark" / "benchmark.json", jd)
    (jd / "heldout.json").write_text(json.dumps({"items": held}, indent=1))
    for ag in "AB":
        arena("check", rd / ag / "language.json")
        t = wd / ag
        arena("render", rd / ag / "language.json", t)
        shutil.copy(t / "spec.md", rd / ag / "spec.md")
        write(t / "cold_prompt.md", fill("cold_prompt.md", PACKET=t / "cold_packet.md", OUT=t / "cold.md"))
        hs = {i["id"].upper(): i["english"] for i in held}
        write(t / "spec_prompt.md", fill("spec_prompt.md", PACKET=t / "spec_packet.md", OUT=t / "spec_learner.md", **hs))
    for label, ag in mapping.items():
        (jd / label).mkdir(exist_ok=True)
        shutil.copy(wd / ag / "spec.md", jd / label)
    write(jd / "judge_prompt.md", fill("judge_prompt.md", ROUND=n, DIR=jd))
    print("blind map:", mapping, "\nnext: spawn cold readers + spec learners on", wd / "A", "and", wd / "B")


def collect(n):
    wd = WORK / f"r{int(n)}"
    mapping = json.loads((wd / "map.json").read_text())
    for label, ag in mapping.items():
        for f in ("cold.md", "spec_learner.md"):
            shutil.copy(wd / ag / f, wd / "judge" / label / f)
    print("next: spawn the judge on", wd / "judge" / "judge_prompt.md")


def judge_by_agent(wd):
    blind = json.loads((wd / "judge" / "judge_blind.json").read_text())
    mapping = json.loads((wd / "map.json").read_text())

    def item(v):
        return max(0.0, sum(v["facts"]) - 0.5 * v.get("wrong", 0)) / len(v["facts"])

    out = {}
    for label, ag in mapping.items():
        d = blind[label]
        out[ag] = {
            "cold": {k: round(item(v), 4) for k, v in d["cold"].items()},
            "spec": {k: round(item(v), 4) for k, v in d["spec"].items()},
            "encode": {k: {"coverage": sum(v["facts"]) / len(v["facts"]), "validity": v["validity"]}
                       for k, v in d["encode"].items()},
            "comments": d.get("comments", ""),
            "raw": d,
        }
    return out


def score(n, *flags):
    n = int(n)
    rd, wd = ROOT / "rounds" / f"r{n}", WORK / f"r{n}"
    full = judge_by_agent(wd)
    (rd / "judge.json").write_text(json.dumps(full, indent=2))
    arena("score", rd)
    publish = "--publish" in flags
    for ag in "AB":
        td = rd / ag / "tests"
        td.mkdir(parents=True, exist_ok=True)
        shutil.copy(wd / ag / "cold.md", td)
        learner = (wd / ag / "spec_learner.md").read_text()
        if not publish:  # keep held-out encodings away from future designers
            learner = re.sub(r"## Encode.*?(?=DIFFICULTY)", "", learner, flags=re.S)
        (td / "spec_learner.md").write_text(learner)
    if not publish:
        for a in full.values():
            a["raw"].pop("encode", None)
            a["raw"].pop("comments", None)
            a.pop("comments", None)
        (rd / "judge.json").write_text(json.dumps(full, indent=2))
    shutil.copy(wd / "map.json", rd / "blind_map.json")
    s = json.loads((rd / "score.json").read_text())
    prev_f = ROOT / "rounds" / f"r{n-1}" / "score.json"
    if prev_f.exists():
        prev = json.loads(prev_f.read_text())
        for ag in "AB":
            gain = s[ag]["total"] - prev[ag]["total"]
            print(f"{ag}: {prev[ag]['total']} -> {s[ag]['total']}  gain {gain:+.2f}  "
                  f"{'ok' if gain >= STOP_GAIN else 'BELOW ' + str(STOP_GAIN) + ': ARENA STOPS'}")
    print("now write rounds/r%d/feedback.md (summarise judge comments from %s without held-out details)"
          % (n, wd / "judge" / "judge_blind.json"))


# ---------------------------------------------------------------- vocabulary loop

def vocab_propose(n):
    n = int(n)
    V = ROOT / "vocab"
    (V / f"i{n}").mkdir(parents=True, exist_ok=True)
    M = json.loads((V / "meanings.json").read_text())["meanings"]
    if n == 1:
        base = {m["id"]: m["incumbent"] for m in M}
        hist = "This is iteration 1, so there is no history. The incumbents in meanings.json are the words to beat."
    else:
        lb = json.loads((V / f"i{n-1}" / "leaderboard.json").read_text())
        base = {m: r["word"] for m, r in lb["champions"].items()}
        hist = (f"Read {V}/i{n-1}/leaderboard.md, the results of the last test. Learn from what scored high (D) and "
                "what scored low. Do NOT re-propose any word that already appears in that leaderboard.")
    (V / f"i{n}" / "baseline.json").write_text(json.dumps(base, indent=1))
    styles = {"L": ("LITERAL-FIRST", "Prefer the word that states the meaning most literally and unmistakably, even if it is a few letters longer."),
              "S": ("SHORT-FIRST", "Prefer the shortest word, ideally 2 to 5 letters, that still states the meaning literally.")}
    for k, (st, rule) in styles.items():
        write(WORK / "prompts" / f"vocab_i{n}_prop_{k}.md",
              fill("proposer_prompt.md", STYLE=st, STYLE_RULE=rule, HISTORY=hist, OUT=V / f"i{n}" / f"proposals_{k}.json"))


def vocab_rate(n):
    I = ROOT / "vocab" / f"i{int(n)}"
    merged = {}
    for k in "LS":
        for m, ws in json.loads((I / f"proposals_{k}.json").read_text()).items():
            merged.setdefault(m, []).extend(ws)
    (I / "candidates.json").write_text(json.dumps(merged, indent=1))
    subprocess.run([PY, str(ROOT / "vocab" / "vocab.py"), "packets", str(I)], check=True)
    for r in range(4):
        write(WORK / "prompts" / f"vocab_i{n}_rater_{r}.md",
              fill("rater_prompt.md", PACKET=I / f"rater_{r}_packet.md", OUT=I / f"rater_{r}.json"))


# ---------------------------------------------------------------- checks

def validate(path):
    sys.path.insert(0, str(ROOT / "tools"))
    from arena import ALLOWED, WORD, is_english
    bad = 0
    for n, line in enumerate(Path(path).read_text().splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        errs = []
        if not ALLOWED.match(line):
            errs.append("illegal characters")
        nw = [w for w in WORD.findall(line) if not w.isdigit() and not is_english(w)]
        if nw:
            errs.append(f"not English: {nw}")
        for clause in line.split(";"):
            m = re.match(r"^(.*), (runaway|balancing)(?: at .*| forever)?$", clause.strip())
            if not m:
                continue
            chain = m.group(1).split(":", 1)[-1]
            parts = re.split(r"\b(raises|lowers)\b", chain)
            nodes = [re.sub(r"\blag\b.*", "", p).strip() for p in parts[0::2]]
            if nodes[0] != nodes[-1]:
                errs.append(f"loop not closed: {nodes[0]!r} ... {nodes[-1]!r}")
            want = "runaway" if parts[1::2].count("lowers") % 2 == 0 else "balancing"
            if want != m.group(2):
                errs.append(f"parity says {want}")
        if errs:
            bad += 1
            print(f"{n}: {line[:70]}  {errs}")
    print("bad lines:", bad)
    return bad


if __name__ == "__main__":
    cmds = {"designers": designers, "prep": prep, "collect": collect, "score": score,
            "vocab-propose": vocab_propose, "vocab-rate": vocab_rate, "validate": validate}
    if len(sys.argv) < 3 or sys.argv[1] not in cmds:
        print(__doc__)
        sys.exit(1)
    cmds[sys.argv[1]](*sys.argv[2:])
