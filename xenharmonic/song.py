#!/usr/bin/env python3
"""
"Where the Slow Moon Goes" — a slow swing ballad in the Morsiri scale, in the manner of a 1930s
Hoagy Carmichael song: AABA form, piano comping, upright bass in two, brushes, a clarinet-like
lead, and a crooned vocal. 76 bpm, swung eighths on a triplet grid (12 units per 4/4 bar).

This file is the single source of truth: tuning, key, form, harmony, comping, melody and lyrics.
It validates the score against the scale's rules and writes song.json, which morsiri_song.scd
(instruments, SuperCollider) and sing.py (voice) both read.

Pitch tokens in the melody tables: degree letter + period shift.
    V Vum (tonic)  T Tol  S Siri  K Kun  M Mor (pillar)  O Ovit  H Hilu  Z Zish (spicy)  N Nimo
    "V0" Vum in the tonic period, "N-" Nimo one period down (the leading tone), "M-" Mor one period down.
Every frequency is 'KEY * RATIOS[degree] * PERIOD**k'. Nothing else is ever used as a pitch.
"""
import json, math

# ------------------------------------------------------------------ tuning
TABLE_TONIC = 220.0                        # the reference tonic of the Morsiri tuning table
KEY = TABLE_TONIC * 3 / 4                  # the song's key: tonic 165 Hz, a 4/3 below the table, a baritone's range
PERIOD = 12 / 5
GEN = ((8 / 7) * (12 / 5)) ** (1 / 5)
_chain = []
for k in range(9):
    r = GEN ** k
    while r >= PERIOD: r /= PERIOD
    _chain.append(r)
RATIOS = sorted(_chain)
NAMES = ["Vum", "Tol", "Siri", "Kun", "Mor", "Ovit", "Hilu", "Zish", "Nimo"]
LETTER = {"V": 0, "T": 1, "S": 2, "K": 3, "M": 4, "O": 5, "H": 6, "Z": 7, "N": 8}
CHAIN_POS = {RATIOS.index(r): k for k, r in enumerate(_chain)}
POS_DEG = {v: k for k, v in CHAIN_POS.items()}

def hz(deg, per=0): return KEY * RATIOS[deg] * PERIOD ** per
def tok(t): return LETTER[t[0]], {"0": 0, "-": -1, "+": 1}[t[1]]
def cents(a, b): return 1200 * math.log2(hz(*b) / hz(*a))

# ------------------------------------------------------------------ time
BPM = 76
UNIT = 60 / BPM / 3                        # a triplet eighth: 0.263 s; swung eighths are 2 + 1 units
BAR = 12

# ------------------------------------------------------------------ chords (root one period down)
def quintal(letter):
    p = CHAIN_POS[LETTER[letter]]
    return [(POS_DEG[q], -1 + (1 if q >= 5 else 0)) for q in (p, p + 2, p + 4)]
CHORDS = {
    "Vum":  [(0, -1), (4, -1), (0, 0)],    # tonic frame      1 : 3/2 : 12/5
    "Sept": [(0, -1), (3, -1), (0, 0)],    # septimal colour  1 : 7/5 : 12/5
    "Mor":  quintal("M"),                  # 1 : 3/2 : 9/4 on the pillar; holds the leading tone
    "Hilu": quintal("H"),
    "Siri": quintal("S"),
}
for nm in ("Mor", "Hilu", "Siri"):
    r, a, b = CHORDS[nm]
    assert abs(cents(r, a) - 698.7) < 0.5 and abs(cents(r, b) - 1397.5) < 0.5

# ------------------------------------------------------------------ form and harmony
# per bar: "Name" or "A:len,B:len" (units). Cadence bars push the tonic chord on the and-of-two: "Mor:5,Vum:7".
CAD = "Mor:5,Vum:7"
A_H  = ["Vum", "Hilu", "Siri", CAD, "Sept", "Siri", "Hilu", CAD]
A3_H = ["Vum", "Siri", "Hilu", "Hilu", "Vum", CAD, "Hilu", CAD]            # bar 5 of A3 holds the frame under Zish
B_H  = ["Hilu", "Siri", "Hilu", CAD, "Siri", "Siri", "Sept:7,Mor:5", "Vum"]
INTRO_H = ["Vum", "Hilu", "Siri", CAD]
INST_H  = ["Vum", "Siri", "Mor", "Hilu:5,Mor:4,Vum:3"]   # roots up the generator chain: a cycle of neutral thirds
TAG_H   = ["Vum", "Hilu:6,Siri:6", CAD, "Vum"]
B2_H = ["Hilu", "Siri", "Hilu", CAD, "Siri", "Sept", "Sept:7,Mor:5", "Vum"]
SECTIONS = [("intro", INTRO_H), ("A1", A_H), ("A2", A_H), ("B", B_H), ("A3", A3_H),
            ("interlude", INST_H), ("B'", B2_H), ("A3'", A3_H), ("tag", TAG_H)]
HARMONY = [h for _, hs in SECTIONS for h in hs]
NBARS = len(HARMONY); assert NBARS == 60

def bar_chords(h):
    if ":" not in h: return [(h, 0, BAR)]
    out, pos = [], 0
    for part in h.split(","):
        nm, ln = part.split(":"); out.append((nm, pos, int(ln))); pos += int(ln)
    assert pos == BAR, h
    return out

def chord_at(bar, unit):
    return [c for c in bar_chords(HARMONY[bar]) if c[1] <= unit < c[1] + c[2]][0][0]

# ------------------------------------------------------------------ melody + lyrics  (each line = 2 bars = 24 units)
def L(*items):
    out = []
    for it in items:
        if isinstance(it, int): out.append((None, [("rest", it)]))
        else: out.append((it[0], [(n[:2], int(n[2:])) for n in it[1]]))
    total = sum(d for _, ns in out for _, d in ns); assert total <= 24, (total, items)
    if total < 24:                                    # the line's closing rest absorbs the remainder
        if out[-1][0] is None: out[-1] = (None, [("rest", out[-1][1][0][1] + 24 - total)])
        else: out.append((None, [("rest", 24 - total)]))
    return out

# Lines 1 and 3 of each A end open (on Tol over Hilu, or Siri over Siri); lines 2 and 4 cadence Nimo -> Vum.
A1 = [
 L(1, ("Down", ["V03"]), ("where", ["T01"]), ("the", ["S02"]), ("ri-", ["K02"]), ("ver", ["M03"]), ("for-", ["K01"]),
   ("gets", ["S02"]), ("its", ["T01"]), ("own", ["V02"]), ("name", ["T04"]), 2),
 L(2, ("the", ["N-1"]), ("wil-", ["V02"]), ("lows", ["T01"]), ("lean", ["S03"]), ("and", ["T01"]), ("the", ["S02"]),
   ("night", ["M02"]), ("runs", ["K02"]), ("slow", ["T01", "N-1", "V04"]), 2),
 L(1, ("I", ["M-2"]), ("hum", ["H-1"]), ("the", ["N-2"]), ("tune", ["V03"]), ("that", ["T01"]), ("the", ["S02"]),
   ("porch", ["S02"]), ("light", ["T02"]), ("knows", ["S05"]), 3),
 L(1, ("and", ["V01"]), ("the", ["T01"]), ("moon", ["S03"]), ("comes", ["K01"]), ("round", ["M03"]), ("where", ["K01"]),
   ("the", ["S02"]), ("slow", ["T02"]), ("moon", ["V02"]), ("goes", ["N-1", "V05"]), 1),
]
A2 = [
 L(1, ("The", ["V01"]), ("old", ["T02"]), ("pi-", ["S02"]), ("a-", ["K01"]), ("no's", ["M03"]), ("a", ["K01"]),
   ("lit-", ["S02"]), ("tle", ["T01"]), ("off", ["V02"]), ("key", ["T05"]), 2),
 L(2, ("but", ["N-1"]), ("it", ["V01"]), ("still", ["T02"]), ("re-", ["S01"]), ("mem-", ["K02"]), ("bers", ["S02"]),
   ("the", ["T01"]), ("songs", ["S02"]), ("we", ["T01"]), ("sang", ["N-1", "V04"]), 4),
 L(1, ("there's", ["M-1"]), ("a", ["H-1"]), ("train", ["N-2"]), ("some-", ["V02"]), ("where", ["T01"]), ("that", ["S02"]),
   ("was", ["K01"]), ("nev-", ["S02"]), ("er", ["T01"]), ("mine", ["S05"]), 4),
 L(1, ("and", ["V01"]), ("a", ["T01"]), ("screen", ["S02"]), ("door", ["K01"]), ("some-", ["M03"]), ("where", ["K01"]),
   ("that", ["S02"]), ("used", ["T02"]), ("to", ["V02"]), ("bang", ["N-1", "V05"]), 2),
]
B = [
 L(1, ("Oh", ["M03"]), ("slow", ["K02"]), ("moon", ["M03"]), ("car-", ["K01"]), ("ry", ["S02"]), ("me", ["K02"]),
   ("ea-", ["S02"]), ("sy", ["T03"]), 5),
 L(1, ("o-", ["M03"]), ("ver", ["K01"]), ("the", ["S02"]), ("wa-", ["T03"]), ("ter", ["S01"]), ("un-", ["K02"]),
   ("der", ["S02"]), ("the", ["T01"]), ("pine", ["N-1", "V05"]), 2),
 L(1, ("I've", ["T01"]), ("got", ["S02"]), ("a", ["T01"]), ("pock-", ["S02"]), ("et", ["K01"]), ("of", ["S02"]),
   ("yes-", ["M03"]), ("ter-", ["K01"]), ("days", ["S04"]), 6),
 L(1, ("and", ["T01"]), ("ev-", ["S02"]), ("ry", ["T01"]), ("one", ["V03"]), ("of", ["N-1"]), ("them", ["V02"]),
   ("is", ["N-1"]), ("mine", ["V08"]), 4),
]
A3 = [
 L(1, ("And", ["M-2"]), ("if", ["H-1"]), ("you", ["N-2"]), ("won-", ["V03"]), ("der", ["T01"]), ("why", ["S03"]),
   ("I", ["T02"]), ("stay", ["S05"]), 4),
 L(1, ("when", ["S01"]), ("the", ["T01"]), ("paint's", ["S02"]), ("worn", ["K02"]), ("thin", ["M02"]), ("and", ["K01"]),
   ("the", ["S02"]), ("dock's", ["T02"]), ("gone", ["S02"]), ("gray", ["T04"]), 4),
 # the peak: "light" on Zish, the spicy degree, over the tonic frame; it resolves up by the small step to Nimo
 L(1, ("it's", ["T01"]), ("the", ["S02"]), ("way", ["T02"]), ("the", ["V01"]), ("light", ["Z-5"]), ("falls", ["N-2"]),
   ("on", ["V01"]), ("the", ["T01"]), ("bay", ["N-1", "V04"]), 3),
 L(2, ("down", ["V02"]), ("where", ["T01"]), ("the", ["S02"]), ("slow", ["T03"]), ("moon", ["V02"]), ("goes", ["N-1", "V07"]), 4),
]
TAG = [L(2, ("down", ["V03"]), ("where", ["T02"]), ("the", ["S01"]), ("slow", ["T04"]), ("moon", ["V02"]), ("goes", ["N-2", "V07"]), 1),
       L(24)]
REST8 = [L(24)] * 4                                 # a silent 8-bar section
# first time through, "light" is sung plainly on Tol; the reprise A3' carries the spicy Zish (the song's one peak)
A3_PLAIN = A3[:2] + [L(1, ("it's", ["T01"]), ("the", ["S02"]), ("way", ["T02"]), ("the", ["V01"]), ("light", ["T05"]), ("falls", ["N-2"]),
                        ("on", ["V01"]), ("the", ["T01"]), ("bay", ["N-1", "V04"]), 3)] + A3[3:]
# B the second time: line 3 climbs by neutral thirds and falls back a step each time (Vum Siri Tol Kun Siri Mor Kun Mor),
# a pattern that exists only in a neutral-third scale; line 4 sings the hook with shrinking durations 4-3-2-1 into the long note
B2 = B[:2] + [
 L(1, ("I've", ["V01"]), ("got", ["S02"]), ("a", ["T01"]), ("pock-", ["K02"]), ("et", ["S01"]), ("of", ["M02"]),
   ("yes-", ["K01"]), ("ter-", ["M02"]), ("days", ["K05"]), 6),
 L(1, ("and", ["T01"]), ("ev-", ["S01"]), ("ry", ["T01"]), ("one", ["V04"]), ("of", ["N-3"]), ("them", ["V02"]),
   ("is", ["N-1"]), ("mine", ["V08"]), 2),
]
VOCAL = [("intro", [L(24)] * 2), ("A1", A1), ("A2", A2), ("B", B), ("A3", A3_PLAIN), ("interlude", [L(24)] * 2),
         ("B'", B2), ("A3'", A3), ("tag", TAG)]
# clarinet-like lead: the "moon goes" line in the intro, lines 3-4 of A in the interlude, a closing figure in the tag
SPIRAL = L(("", ["V02"]), ("", ["S02"]), ("", ["M02"]), ("", ["H02"]), ("", ["N03"]), 1,          # up the generator chain
           ("", ["H02"]), ("", ["O02"]), ("", ["M02"]), ("", ["K02"]), ("", ["S04"]))               # down by scale steps
CLIMB  = L(("", ["V01"]), ("", ["S02"]), ("", ["T01"]), ("", ["K02"]), ("", ["S01"]), ("", ["M02"]), ("", ["K01"]),
           ("", ["O02"]), ("", ["M01"]), ("", ["H02"]),                                             # sawtooth: +g, -step
           ("", ["O02"]), ("", ["M01"]), ("", ["K01"]), ("", ["S01"]), ("", ["T01"]), ("", ["N-1"]), ("", ["V02"]))  # quickening fall, cadence
LEAD = [("intro", [L(24), A1[3]]), ("interlude", [SPIRAL, CLIMB]),
        ("tag", [L(24), L(2, ("", ["K02"]), ("", ["S02"]), ("", ["T02"]), ("", ["N-2"]), ("", ["V014"]))])]
LEAD_OFFSET = {"intro": 0, "interlude": 0, "tag": 0}

# ------------------------------------------------------------------ build
def section_start(name):
    b = 0
    for s, hs in SECTIONS:
        if s == name: return b
        b += len(hs)
    raise KeyError(name)

def build():
    ev = {k: [] for k in ("piano", "pianobass", "bass", "brush", "ride", "lead", "vocal", "vibes")}
    # the 7-cycle: chord tones in durations 3 + 2 + 2, looping every 7 units across 12-unit bars, so it realigns with the
    # downbeat only every 7 bars. It sounds in the interlude, the second release and the tag.
    for sec in ("interlude", "B'", "tag"):
        b0 = section_start(sec); nb = dict(SECTIONS)[sec].__len__()
        u0, u1 = b0 * BAR, (b0 + nb) * BAR
        u = u0; k = 0
        while u < u1 - 1:
            off, dur = [(0, 3), (3, 2), (5, 2)][k % 3]
            bar, pos = divmod(u, BAR)
            tones = CHORDS[chord_at(bar, pos)]
            dgp = tones[[1, 2, 0][k % 3]]
            ev["vibes"].append(dict(t=u, d=dur, f=[hz(dgp[0], dgp[1] + 1)], a=0.055))
            u += dur; k += 1
    # ---- rhythm section, bar by bar
    for bar, h in enumerate(HARMONY):
        t0 = bar * BAR
        sec = [s for s, _ in SECTIONS if section_start(s) <= bar][-1]
        loud = 1.15 if sec in ("B'", "A3'") else 1.0
        final = bar == NBARS - 1
        segs = bar_chords(h)
        # piano: chord on beat one, chord pushed on the and-of-two (unit 5) or on beat three; stride bass notes
        for nm, start, ln in segs:
            tones = CHORDS[nm]
            hits = [start] if ln <= 5 else ([start, start + 6] if start == 0 and ln == 12 else [start])
            if start == 5: hits = [5, 9]
            for i, u in enumerate(hits):
                dur = (hits[i + 1] - u) if i + 1 < len(hits) else (start + ln - u)
                ev["piano"].append(dict(t=t0 + u, d=dur, f=[hz(d, p) for d, p in tones], a=(0.16 if u % 6 == 0 else 0.11) * loud))
            root = tones[0]
            ev["pianobass"].append(dict(t=t0 + start, d=min(6, ln), f=[hz(root[0], root[1] - 1)], a=0.2 * loud))
            if ln >= 10: ev["pianobass"].append(dict(t=t0 + start + 6, d=ln - 6, f=[hz(*tones[1]) / PERIOD], a=0.15 * loud))
        # upright bass in two: root on one, pillar on three, a short root again on the and-of-four as the walk-up
        first = segs[0][0]; last = segs[-1][0]
        r1 = CHORDS[first][0]; r2 = CHORDS[last][0]
        ev["bass"].append(dict(t=t0, d=6, f=[hz(*r1)], a=0.5 * loud))
        if len(segs) == 1:
            ev["bass"].append(dict(t=t0 + 6, d=4, f=[hz(*CHORDS[first][1])], a=0.42 * loud))
        else:
            ev["bass"].append(dict(t=t0 + segs[1][1], d=6, f=[hz(*r2)], a=0.46 * loud))
        if not final:
            nxt = bar_chords(HARMONY[bar + 1])[0][0]
            ev["bass"].append(dict(t=t0 + 11, d=1, f=[hz(*CHORDS[nxt][1]) / PERIOD], a=0.3 * loud))  # leads into the next root
        # brushes: swish on two and four; ride ticks on the beats and the swung off-beats
        if not final and bar >= 1:
            for u in (3, 9): ev["brush"].append(dict(t=t0 + u, d=3, f=[0], a=0.5 * loud))
            for u in range(12):
                a = 0.16 if u % 3 == 0 else (0.07 if u % 3 == 2 else 0)
                if a: ev["ride"].append(dict(t=t0 + u, d=1, f=[0], a=a * loud))
        if final:
            ev["brush"].append(dict(t=t0, d=8, f=[0], a=0.6))
    # ---- vocal
    t = 0; zish = steps = leaps = cad = 0; prev = None
    for sec, lines in VOCAL:
        assert t == section_start(sec) * BAR, (sec, t)
        for line in lines:
            pos = t
            for syl, notes in line:
                first_note = True
                for tk, dur in notes:
                    if tk == "rest": prev = None
                    else:
                        d, p = tok(tk)
                        if d == 7: zish += 1
                        if prev is not None:
                            if abs(cents(prev, (d, p))) <= 240: steps += 1
                            else: leaps += 1
                            if prev == (8, p - 1) and d == 0: cad += 1
                        prev = (d, p)
                        ev["vocal"].append(dict(t=pos, d=dur, f=[hz(d, p)], a=1.0, syl=(syl if first_note else None),
                                                melisma=(not first_note), deg=d, per=p, chord=chord_at(pos // BAR, pos % BAR)))
                        first_note = False
                    pos += dur
            t += 24
    assert t == NBARS * BAR, (t, NBARS * BAR)
    # ---- lead (clarinet-like)
    for sec, lines in LEAD:
        pos = section_start(sec) * BAR
        for line in lines:
            for syl, notes in line:
                for tk, dur in notes:
                    if tk != "rest":
                        d, p = tok(tk)
                        ev["lead"].append(dict(t=pos, d=dur, f=[hz(d, p + 1)], a=0.2))   # one period above the voice
                    pos += dur
    # ---- piano fills where the voice rests at line ends (ascending chord tones, swung)
    vocal_busy = set()
    for e in ev["vocal"]:
        for u in range(int(e["t"]), int(e["t"] + e["d"])): vocal_busy.add(u)
    lead_busy = {u for e in ev["lead"] for u in range(int(e["t"]), int(e["t"] + e["d"]))}
    for line_start in range(0, NBARS * BAR, 24):
        tail = [u for u in range(line_start + 18, line_start + 24) if u not in vocal_busy and u not in lead_busy]
        if len(tail) >= 4 and line_start // BAR >= 1:
            tones = CHORDS[chord_at(tail[0] // BAR, tail[0] % BAR)]
            for i, u in enumerate(tail[-4:-1]):
                dgp = tones[i % 3]
                ev["piano"].append(dict(t=u, d=1.5, f=[hz(dgp[0], dgp[1] + 1)], a=0.09))
    stats = dict(zish_uses=zish, steps=steps, leaps=leaps, cadences=cad, bars=NBARS, seconds=round(NBARS * BAR * UNIT, 1))
    return ev, stats

if __name__ == "__main__":
    events, stats = build()
    song = dict(title="Where the Slow Moon Goes", scale="Morsiri", table_tonic=TABLE_TONIC, key_tonic=KEY, period=PERIOD,
                generator=GEN, ratios=RATIOS, names=NAMES, pulse=UNIT, bpm=BPM, units_per_bar=BAR, bars=NBARS,
                sections=[(s, len(h)) for s, h in SECTIONS], harmony=HARMONY, events=events, stats=stats)
    json.dump(song, open("song.json", "w"), indent=0)
    print("stats:", stats)
    table = {round(hz(d, p), 6) for d in range(9) for p in range(-4, 4)}
    pitched = [f for trk in events.values() for e in trk for f in e["f"] if f]
    print("pitched events:", len(pitched), " not from the table:", sum(1 for f in pitched if round(f, 6) not in table))
    print("Zish outside the voice:", sum(1 for k, trk in events.items() if k != "vocal" for e in trk for f in e["f"]
                                        if any(abs(f - hz(7, p)) < 1e-6 for p in range(-4, 4))))
    print("vocal notes:", len(events["vocal"]), " range:", round(min(e["f"][0] for e in events["vocal"]), 1), "-",
          round(max(e["f"][0] for e in events["vocal"]), 1), "Hz")
    b = 0
    for s, hs in SECTIONS:
        print(f"   {s:9} bars {b+1:2}-{b+len(hs):2}  {b*BAR*UNIT:6.1f} s"); b += len(hs)
