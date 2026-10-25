#!/usr/bin/env python3
"""
Exhaustive search for non-octave MOS scales that satisfy the brief:

  * period P in (1.9, 3.2), not 2/1
  * 5..9 notes per period, exactly two step sizes L and s with 1.4 <= L/s <= 2.6
  * generator not within 15 c of 3/2, 4/3, 5/4, 6/5 or any multiple of 100 c
  * >= 4 intervals from the tonic within 8 c of a just ratio with n*d <= 100,
    >= 2 of them ratios that 12-TET does NOT approximate well (> 15 c off)
  * >= 60 % of intervals from the tonic > 15 c from every 12-TET interval
  * exactly one "spicy" interval 20..40 c from anything familiar, nothing > 40 c
  * a small step s adjacent to the tonic (leading tone)

Everything is measured in cents from the tonic.  Run:  python3 scale_search.py
"""
import math
from fractions import Fraction
from itertools import product

C = 1200 / math.log(2)
def cents(r): return C * math.log(r)

# ---------- "familiar" reference sets ----------
JUST = {}
for n in range(1, 101):
    for d in range(1, 101):
        if n * d <= 100 and math.gcd(n, d) == 1 and 1 < n / d <= 3.3:
            JUST[Fraction(n, d)] = cents(n / d)

def nearest_just(c):
    best = min(JUST.items(), key=lambda kv: abs(kv[1] - c))
    return best[0], best[1] - c           # ratio, error (just - actual)

def dist_12tet(c):
    return abs(c - 100 * round(c / 100))

def tet_approximates_well(frac):
    return dist_12tet(JUST[frac]) <= 15

FORBIDDEN_GEN = [cents(3/2), cents(4/3), cents(5/4), cents(6/5)]
def generator_ok(g):
    if dist_12tet(g) < 15: return False
    return all(abs(g - f) >= 15 for f in FORBIDDEN_GEN)

# ---------- MOS machinery ----------
def mos_scale(P, g, n):
    """Return sorted degrees (cents, 0 included, period excluded) and step list,
    or None if n notes of generator g do not form a 2-step-size MOS."""
    degs = sorted((k * g) % P for k in range(n))
    steps = [b - a for a, b in zip(degs, degs[1:])] + [P - degs[-1]]
    sizes = sorted(set(round(s, 4) for s in steps))
    if len(sizes) != 2: return None
    return degs, steps, sizes[1], sizes[0]     # L, s

def rotations(steps):
    n = len(steps)
    for r in range(n):
        yield r, steps[r:] + steps[:r]

def evaluate_mode(P, steps):
    """Metrics for one mode (step pattern starting at the tonic)."""
    degs = [0.0]
    for st in steps[:-1]: degs.append(degs[-1] + st)
    ivals = degs[1:] + [P]                      # all intervals from tonic incl. period
    cons, septimal, novel, spicy, toofar = [], 0, 0, [], 0
    rows = []
    for c in ivals:
        frac, err = nearest_just(c)
        d12 = dist_12tet(c)
        fam = min(abs(err), d12)                # distance to anything familiar
        if abs(err) <= 8:
            cons.append((c, frac, err))
            if not tet_approximates_well(frac): septimal += 1
        if d12 > 15: novel += 1
        if 20 <= fam <= 40: spicy.append((c, frac, err))
        if fam > 40: toofar += 1
        rows.append((c, frac, err, d12, fam))
    return dict(degs=degs, ivals=ivals, cons=cons, septimal=septimal,
                novel=novel / len(ivals), spicy=spicy, toofar=toofar, rows=rows)

PERIODS = {
    "3/1": 3.0, "5/2": 2.5, "7/3": 7/3, "8/3": 8/3, "9/4": 2.25, "11/4": 2.75,
    "12/5": 2.4, "11/5": 2.2, "13/5": 2.6, "phi+1": (1 + 5 ** 0.5) / 2 + 1,
}

def search(verbose=True):
    results = []
    for pname, P in PERIODS.items():
        Pc = cents(P)
        g = 40.0
        while g < Pc / 2:
            if generator_ok(g):
                for n in range(5, 10):
                    m = mos_scale(Pc, g, n)
                    if not m: continue
                    degs, steps, L, s = m
                    if not (1.4 <= L / s <= 2.6): continue
                    nL = sum(1 for st in steps if abs(st - L) < 1e-3)
                    if nL < 2 or n - nL < 2: continue          # both step sizes used >= 2 times
                    if pname == "3/1" and abs(g - cents(9/7)) < 25: continue   # Bohlen-Pierce Lambda family
                    for r, pat in rotations(steps):
                        # leading tone: s adjacent to tonic (first or last step)
                        if not (abs(pat[0] - s) < 1e-3 or abs(pat[-1] - s) < 1e-3): continue
                        ev = evaluate_mode(Pc, pat)
                        if len(ev["cons"]) < 4 or ev["septimal"] < 2: continue
                        if ev["novel"] < 0.6: continue
                        if len(ev["spicy"]) != 1 or ev["toofar"]: continue
                        # the generator itself should be in the mode's intervals (pillar candidate)
                        # Tenney-weighted consonance: simpler ratios and smaller errors score more
                        tw = sum((7 - math.log2(f.numerator * f.denominator)) * (1 - abs(e) / 10)
                                 for _, f, e in ev["cons"] if f != Fraction(int(round(P)), 1) or True)
                        score = tw + ev["septimal"] * 1.5 + ev["novel"] * 4
                        results.append((score, pname, P, g, n, r, L, s, pat, ev))
            g += 0.5
    results.sort(key=lambda t: -t[0])
    return results

def pattern_string(pat, L):
    return "".join("L" if abs(p - L) < 1e-3 else "s" for p in pat)

def report(res):
    score, pname, P, g, n, r, L, s, pat, ev = res
    print(f"\n=== period {pname} ({cents(P):.1f} c)  generator {g:.1f} c  "
          f"{n} notes  mode {r}  pattern {pattern_string(pat, L)}  "
          f"L={L:.1f} s={s:.1f} L/s={L/s:.2f}  score {score:.1f}")
    print(f"  consonant {len(ev['cons'])} (12-TET-alien {ev['septimal']}), "
          f"novel {ev['novel']*100:.0f} %, spicy {[round(c,1) for c,_,_ in ev['spicy']]}")
    for c, frac, err, d12, fam in ev["rows"]:
        tag = "CONS " if abs(err) <= 8 else ("SPICY" if 20 <= fam <= 40 else "     ")
        print(f"   {c:8.1f} c  nearest {str(frac):>6} ({JUST[frac]:7.1f}, err {err:+6.1f})  "
              f"12TET dist {d12:5.1f}  {tag}")

if __name__ == "__main__":
    res = search()
    print(f"{len(res)} qualifying (period, generator, size, mode) combinations")
    seen = set()
    shown = 0
    for r in res:
        key = (r[1], round(r[3]), r[4])
        if key in seen: continue
        seen.add(key)
        report(r)
        shown += 1
        if shown >= 12: break
