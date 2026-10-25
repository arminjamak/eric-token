#!/usr/bin/env python3
"""
"Where the Slow Moon Goes" — a 3-minute song in the Morsiri scale (period 12/5, 9 notes).

This file is the single source of truth for the song: tuning, groove, chords, bass, arpeggio,
melody and lyrics. It validates the score against the scale's rules and writes song.json,
which morsiri_song.scd (instruments, SuperCollider) and sing.py (voice) both read.

Pitch notation used in the melody tables: a degree letter followed by a period shift.
    V Vum (tonic)  T Tol  S Siri  K Kun  M Mor (pillar)  O Ovit  H Hilu  Z Zish (spicy)  N Nimo
    "V0" = Vum in the tonic period (220 Hz), "N-" = Nimo one period down (205.5 Hz, the leading tone),
    "M-" = Mor one period down (137.2 Hz).  Every pitch is looked up in RATIOS; nothing else.
"""
import json, math, sys
from fractions import Fraction

# ------------------------------------------------------------------ tuning (same as morsiri.scd)
TONIC = 220.0
PERIOD = 12 / 5
GEN = ((8 / 7) * (12 / 5)) ** (1 / 5)
_chain = []
for k in range(9):
    r = GEN ** k
    while r >= PERIOD: r /= PERIOD
    _chain.append(r)
RATIOS = sorted(_chain)                                     # the frequency array (as ratios)
NAMES = ["Vum", "Tol", "Siri", "Kun", "Mor", "Ovit", "Hilu", "Zish", "Nimo"]
LETTER = {"V": 0, "T": 1, "S": 2, "K": 3, "M": 4, "O": 5, "H": 6, "Z": 7, "N": 8}
CHAIN_POS = {RATIOS.index(r): k for k, r in enumerate(_chain)}   # degree -> generator count
POS_DEG = {v: k for k, v in CHAIN_POS.items()}

def hz(deg, per=0):
    return TONIC * RATIOS[deg] * PERIOD ** per

def tok(t):
    """'V0' -> (deg, per);  'N-' -> (deg, -1);  'M+' -> (deg, +1)"""
    deg = LETTER[t[0]]
    per = {"0": 0, "-": -1, "+": 1, "=": -2}[t[1]]
    return deg, per

def cents(a, b):  # interval in cents from pitch a to pitch b, each (deg, per)
    return 1200 * math.log2(hz(*b) / hz(*a))

# ------------------------------------------------------------------ time
PULSE = 0.30            # seconds; 7 pulses per bar grouped 3+2+2 (bar = 2.1 s)
BAR = 7

# ------------------------------------------------------------------ chords
# Quintal triads built from the scale's most consonant intervals: root, root+Mor (3/2), root+Nimo (9/4).
# A chord on generator position p uses positions p, p+2, p+4. Roots are placed one period down.
def quintal(root_letter):
    deg = LETTER[root_letter]; p = CHAIN_POS[deg]
    tones = []
    for q in (p, p + 2, p + 4):
        d = POS_DEG[q]
        # chain positions 5..8 (Tol, Kun, Ovit, Zish) fall in the period above the root's
        per = -1 + (1 if q >= 5 else 0)
        tones.append((d, per))
    return tones

CHORDS = {
    "Vum":  [(0, -1), (4, -1), (0, 0)],         # tonic frame     1 : 3/2 : 12/5
    "Sept": [(0, -1), (3, -1), (0, 0)],         # septimal colour 1 : 7/5 : 12/5
    "Mor":  quintal("M"),                       # 1 : 3/2 : 9/4 on the pillar (contains the leading tone Nimo)
    "Hilu": quintal("H"),
    "Siri": quintal("S"),
}
# sanity: every quintal chord really is 1 : 3/2 : 9/4
for name in ("Mor", "Hilu", "Siri"):
    r, a, b = CHORDS[name]
    assert abs(cents(r, a) - 698.7) < 0.5 and abs(cents(r, b) - 1397.5) < 0.5, (name, cents(r, a), cents(r, b))

# ------------------------------------------------------------------ form and harmony
# One entry per bar: a chord name, or "Mor>Vum" for a cadence bar (Mor 4 pulses, Vum 3 pulses).
VERSE_H  = ["Vum", "Hilu", "Siri", "Mor>Vum",   "Vum", "Sept", "Hilu", "Mor>Vum",
            "Siri", "Hilu", "Vum", "Mor>Vum",   "Sept", "Siri", "Hilu", "Mor>Vum"]
CHORUS_H = ["Hilu", "Siri", "Hilu", "Siri",     "Vum", "Sept", "Hilu", "Mor>Vum",
            "Hilu", "Siri", "Mor", "Vum"]
BRIDGE_H = ["Siri", "Hilu", "Siri", "Siri>Mor", "Vum", "Mor>Vum", "Vum", "Mor>Vum"]
INTRO_H  = [None, None, "Vum", "Vum"]
OUTRO_H  = ["Vum", "Hilu", "Siri", "Mor>Vum", "Vum", "Vum"]

SECTIONS = [("intro", INTRO_H), ("verse 1", VERSE_H), ("chorus 1", CHORUS_H), ("verse 2", VERSE_H),
            ("chorus 2", CHORUS_H), ("bridge", BRIDGE_H), ("chorus 3", CHORUS_H), ("outro", OUTRO_H)]
HARMONY = [h for _, hs in SECTIONS for h in hs]
NBARS = len(HARMONY)
assert NBARS == 86

def bar_chords(h):
    """-> list of (chord name, start pulse within bar, pulses)"""
    if h is None: return []
    if ">" in h:
        a, b = h.split(">")
        return [(a, 0, 4), (b, 4, 3)]
    return [(h, 0, 7)]

# ------------------------------------------------------------------ groove: a 14-pulse (two-bar) cycle
# kick = period-tuned thump, clap = noise burst, hat = short noise on every half pulse.
# bar one accents 3+2+2 (pulses 0,3,5); bar two answers with 3+3+1 (7,10,13 as a pickup) and an
# extra kick on 12 so the cycle leans into its own downbeat.
KICK = [0, 3, 7, 10, 12]
CLAP = [5, 9, 13]
HAT_ACCENT = [0, 3, 5, 7, 10, 12]
# bass: root on the kicks, a pillar-above passing tone on 9, the next root anticipated on 13
BASS_CYCLE = [(0, "root", 3), (3, "root", 2), (7, "root", 2), (9, "fifth", 1), (10, "root", 2), (12, "root", 1), (13, "next", 1)]
# arpeggio (pluck): chord-tone index per half pulse, 14 half-pulses per bar
ARP = [0, None, 1, 2, None, 1, 0, None, 2, None, 1, 0, 2, None]

# ------------------------------------------------------------------ melody + lyrics
# Each line: list of (lyric syllable or None for rest, [(pitch token, pulses), ...]) ; a syllable with several
# pitches is a melisma. Every line is exactly 4 bars = 28 pulses (verse/chorus) so lines align with harmony.
def L(*items):
    out = []
    for it in items:
        if isinstance(it, int): out.append((None, [("rest", it)]))
        else:
            syl, notes = it
            out.append((syl, [(n[:2], int(n[2:])) if isinstance(n, str) else n for n in notes]))
    return out

def n(tokdur):  # "V02" -> ("V0", 2)
    return (tokdur[:2], int(tokdur[2:]))

VERSE1 = [
 L(1, ("Down", ["V03"]), ("where", ["T01"]), ("the", ["S01"]), ("ri-", ["K02"]), ("ver", ["M03"]), ("for-", ["K01"]),
   ("gets", ["S02"]), ("its", ["T01"]), ("own", ["V02"]), ("name", ["N-1", "V04"]), 6),
 L(1, ("the", ["N-1"]), ("wil-", ["V02"]), ("lows", ["T01"]), ("lean", ["S03"]), ("and", ["T01"]), ("the", ["S01"]),
   ("night", ["M02"]), ("runs", ["K02"]), ("slow", ["T01", "N-1", "V04"]), 8),
 L(2, ("I", ["M-1"]), ("hum", ["H-2"]), ("the", ["N-1"]), ("tune", ["V03"]), ("that", ["T01"]), ("the", ["S01"]),
   ("porch", ["S02"]), ("light", ["T02"]), ("knows", ["N-1", "V04"]), 8),
 L(1, ("and", ["V01"]), ("the", ["T01"]), ("moon", ["S02"]), ("comes", ["K01"]), ("round", ["M03"]), ("where", ["K01"]),
   ("the", ["S01"]), ("slow", ["T02"]), ("moon", ["V02"]), ("goes", ["N-1", "V05"]), 7),
]
VERSE2 = [
 L(1, ("The", ["V01"]), ("old", ["T02"]), ("pi-", ["S01"]), ("a-", ["K02"]), ("no's", ["M02"]), ("a", ["K01"]),
   ("lit-", ["S02"]), ("tle", ["T01"]), ("off", ["V02"]), ("key", ["N-1", "V04"]), 8),
 L(1, ("but", ["N-1"]), ("it", ["V01"]), ("still", ["T02"]), ("re-", ["S01"]), ("mem-", ["K02"]), ("bers", ["S02"]),
   ("the", ["T01"]), ("songs", ["S02"]), ("we", ["T01"]), ("sang", ["N-1", "V04"]), 9),
 L(2, ("there's", ["M-1"]), ("a", ["H-1"]), ("train", ["N-2"]), ("some-", ["V02"]), ("where", ["T01"]), ("that", ["S01"]),
   ("was", ["K01"]), ("nev-", ["S02"]), ("er", ["T01"]), ("mine", ["N-1", "V04"]), 9),
 L(1, ("and", ["V01"]), ("a", ["T01"]), ("screen", ["S02"]), ("door", ["K01"]), ("some-", ["M02"]), ("where", ["K01"]),
   ("that", ["S01"]), ("used", ["T02"]), ("to", ["V02"]), ("bang", ["N-1", "V05"]), 8),
]
CHORUS = [
 L(1, ("Oh", ["M03"]), ("slow", ["K02"]), ("moon", ["M03"]), ("car-", ["K01"]), ("ry", ["S01"]), ("me", ["K02"]),
   ("ea-", ["S02"]), ("sy", ["T03"]), 10),
 L(1, ("o-", ["M03"]), ("ver", ["K01"]), ("the", ["S01"]), ("wa-", ["T03"]), ("ter", ["S02"]), ("un-", ["K02"]),
   ("der", ["S01"]), ("the", ["T01"]), ("pine", ["N-1", "V05"]), 7),
 L(2, ("I've", ["T01"]), ("got", ["S01"]), ("a", ["T01"]), ("pock-", ["S02"]), ("et", ["K01"]), ("of", ["S01"]),
   ("yes-", ["M02"]), ("ter-", ["K01"]), ("days", ["S02"]), ("and", ["T01"]), ("ev-", ["S01"]), ("ry", ["T01"]),
   ("one", ["V02"]), ("of", ["N-1"]), ("them", ["V01"]), ("is", ["N-1"]), ("mine", ["V06"])),
]
BRIDGE = [
 L(2, ("And", ["M-2"]), ("if", ["H-1"]), ("you", ["N-2"]), ("won-", ["V03"]), ("der", ["T02"]), ("why", ["S03"]),
   ("I", ["T02"]), ("stay", ["S05"]), 6),
 # the peak: "light" sits on Zish, the spicy degree, over the tonic frame, and resolves up by the small step
 L(1, ("it's", ["T01"]), ("the", ["S01"]), ("way", ["T02"]), ("the", ["V01"]), ("light", ["Z-4"]), ("falls", ["N-2"]),
   ("on", ["V01"]), ("the", ["T01"]), ("bay", ["N-1", "V05"]), 8),
]
INTRO_V = [L(28)]                                   # 4 bars, instruments only
OUTRO_V = [L(7), L(7, ("where", ["S01"]), ("the", ["T01"]), ("slow", ["S02"]), ("moon", ["T02"]), ("goes", ["N-1", "V06"]), 8), L(7)]
# chorus 3 ends with "mine" held into the outro: handled by the outro's first bar of rest (the note's release)

VOCAL = [("intro", INTRO_V), ("verse 1", VERSE1), ("chorus 1", CHORUS), ("verse 2", VERSE2), ("chorus 2", CHORUS),
         ("bridge", BRIDGE), ("chorus 3", CHORUS), ("outro", OUTRO_V)]

# ------------------------------------------------------------------ build event lists
def build():
    events = {"pad": [], "bass": [], "pluck": [], "kick": [], "clap": [], "hat": [], "vocal": [], "harmony": []}
    # harmony tracks
    for bar, h in enumerate(HARMONY):
        t0 = bar * BAR
        section = [s for s, hs in SECTIONS if sum(len(x[1]) for x in SECTIONS[:SECTIONS.index((s, hs))]) <= bar][-1]
        lift = 1 if section == "chorus 3" else 0           # final chorus: pads gain a voice one period up
        for name, start, dur in bar_chords(h):
            tones = CHORDS[name]
            freqs = [hz(d, p) for d, p in tones] + ([hz(*tones[0]) * PERIOD ** 1] if lift else [])
            events["pad"].append(dict(t=t0 + start, d=dur, f=freqs, a=0.10 + 0.02 * lift))
            # arpeggio on half pulses
            for hp in range(start * 2, (start + dur) * 2):
                idx = ARP[hp % 14]
                if idx is None or section == "intro" and bar < 2: continue
                f = hz(*tones[idx]) * PERIOD        # plucks live one period above the pad
                events["pluck"].append(dict(t=t0 + hp / 2, d=0.5, f=[f], a=0.07 if hp % 2 == 0 else 0.045))
        # bass follows the chord at each hit; "fifth" = root + Mor interval; "next" = next bar's root
        if h is not None:
            cyc = (bar % 2) * 7
            for p, kind, dur in BASS_CYCLE:
                if not (cyc <= p < cyc + 7): continue
                pos = p - cyc
                chord_here = [c for c in bar_chords(h) if c[1] <= pos < c[1] + c[2]][0][0]
                root = CHORDS[chord_here][0]
                if kind == "root": f = hz(*root)                    # pad root, 91.7 .. 168 Hz
                elif kind == "fifth": f = hz(CHORDS[chord_here][1][0], CHORDS[chord_here][1][1])
                else:
                    nxt = HARMONY[bar + 1] if bar + 1 < NBARS else "Vum"
                    nxt = bar_chords(nxt)[0][0] if nxt else "Vum"
                    f = hz(*CHORDS[nxt][0])
                events["bass"].append(dict(t=t0 + pos, d=dur, f=[f], a=0.22 if kind == "root" else 0.15))
    # drums (not in the first intro bar: the song opens with the hats alone, kicks join in bar 2)
    for bar in range(NBARS):
        t0 = bar * BAR; cyc = (bar % 2) * 7
        final = bar == NBARS - 1
        for p in range(7):
            cp = cyc + p
            if cp in KICK and bar >= 1 and not final: events["kick"].append(dict(t=t0 + p, d=0.5, f=[hz(0, -1)], a=0.5))
            if cp in CLAP and bar >= 2 and not final: events["clap"].append(dict(t=t0 + p, d=0.2, f=[0], a=0.22))
            if not final:
                events["hat"].append(dict(t=t0 + p, d=0.1, f=[0], a=0.12 if cp in HAT_ACCENT else 0.05))
                events["hat"].append(dict(t=t0 + p + 0.5, d=0.1, f=[0], a=0.035))
        if final:  # last bar: one kick on the downbeat only
            events["kick"].append(dict(t=t0, d=0.5, f=[hz(0, -1)], a=0.5))
    # vocal
    t = 0
    zish_uses = 0; steps = leaps = 0; prev = None; cadences = 0
    for section, lines in VOCAL:
        for line in lines:
            line_len = 0
            for syl, notes in line:
                for tk, dur in notes:
                    if tk == "rest":
                        prev = None
                    else:
                        d, p = tok(tk)
                        if d == 7: zish_uses += 1
                        if prev is not None:
                            iv = abs(cents(prev, (d, p)))
                            if iv <= 240: steps += 1
                            else: leaps += 1
                        if prev is not None and prev == (8, p - 1) and d == 0: cadences += 1
                        prev = (d, p)
                        # a syllable with several notes is a melisma: only its first note carries the text
                        first = not any(e["syl"] == syl and e["t"] + e["d"] == t + line_len for e in events["vocal"][-1:])
                        events["vocal"].append(dict(t=t + line_len, d=dur, f=[hz(d, p)], a=1.0,
                                                    syl=(syl if first else None), melisma=(not first), deg=d, per=p))
                    line_len += dur
            if section in ("verse 1", "verse 2", "chorus 1", "chorus 2", "chorus 3", "bridge"):
                assert line_len == 28, (section, line_len)
            t += line_len
    assert t == NBARS * BAR, (t, NBARS * BAR)
    # harmony voice for the final chorus: highest chord tone at least 230 c below the melody (2nd male voice)
    c3_start = sum(len(hs) for s, hs in SECTIONS[:6]) * BAR
    c3_end = c3_start + len(CHORUS_H) * BAR
    for ev in events["vocal"]:
        if c3_start <= ev["t"] < c3_end:
            bar = int(ev["t"] // BAR); pos = ev["t"] - bar * BAR
            ch = [c for c in bar_chords(HARMONY[bar]) if c[1] <= pos < c[1] + c[2]][0][0]
            cands = []
            for d, p in CHORDS[ch]:
                for per in (p, p + 1):
                    f = hz(d, per)
                    if 1200 * math.log2(ev["f"][0] / f) >= 230: cands.append((f, d, per))
            if cands:
                f, d, per = max(cands)
                events["harmony"].append(dict(ev, f=[f], deg=d, per=per, a=0.55))
    stats = dict(zish_uses=zish_uses, steps=steps, leaps=leaps, cadences=cadences,
                 bars=NBARS, seconds=round(NBARS * BAR * PULSE, 1))
    return events, stats

if __name__ == "__main__":
    events, stats = build()
    song = dict(title="Where the Slow Moon Goes", scale="Morsiri", tonic=TONIC, period=PERIOD, generator=GEN,
                ratios=RATIOS, names=NAMES, pulse=PULSE, bars=NBARS, sections=[(s, len(h)) for s, h in SECTIONS],
                harmony=HARMONY, events=events, stats=stats)
    json.dump(song, open("song.json", "w"), indent=0)
    print("stats:", stats)
    # all pitched frequencies must be table frequencies
    table = {round(hz(d, p), 6) for d in range(9) for p in range(-3, 4)}
    bad = [e for trk in events.values() for e in trk for f in e["f"] if f and round(f, 6) not in table]
    print("pitched events:", sum(len(e["f"]) for trk in events.values() for e in trk if e["f"][0]),
          " not from the table:", len(bad))
    print("Zish in pads/plucks/bass:", sum(1 for k in ("pad", "pluck", "bass") for e in events[k] for f in e["f"]
                                           if any(abs(f - hz(7, p)) < 1e-6 for p in range(-3, 4))))
    syls = [e["syl"] for e in events["vocal"] if e["syl"]]
    words = sum(1 for e in events["vocal"] if e["syl"] and not e["syl"].endswith("-"))
    print("words:", words)
    print("vocal notes:", len(events["vocal"]), " syllables:", len(syls), " harmony notes:", len(events["harmony"]))
    print("sections (bar, time):")
    b = 0
    for s, hs in SECTIONS:
        print(f"   {s:9} bars {b+1:2}-{b+len(hs):2}   {b*BAR*PULSE:6.1f} s")
        b += len(hs)
