#!/usr/bin/env python3
"""Evaluate the three shortlisted candidates in full and run the novelty (subset-of-known-system) test."""
import math
from fractions import Fraction
import scale_search as S

def mode_from(P, g, n, mode):
    Pc = S.cents(P)
    degs, steps, L, s = S.mos_scale(Pc, g, n)
    pat = steps[mode:] + steps[:mode]
    return Pc, pat, L, s, S.evaluate_mode(Pc, pat)

CANDS = {
 "A  neutral-third chain, period 12/5": dict(P=12/5, g=(S.cents(8/7)+S.cents(12/5))/5, n=9, mode=0),
 "B  undecimal heptatonic, period 11/4": dict(P=11/4, g=778.0, n=7, mode=3),
 "C  tritave octatonic, period 3/1":     dict(P=3.0,  g=737.0, n=8, mode=0),
}

# known systems: equal grids (cents per step) and Partch's 43 (octave-reduced ratios)
GRIDS = {"12-EDO":100, "19-EDO":1200/19, "22-EDO":1200/22, "31-EDO":1200/31,
         "Bohlen-Pierce 13-ED3":S.cents(3)/13, "Carlos alpha":78.0, "Carlos beta":63.8, "Carlos gamma":35.1}
PARTCH = [Fraction(*p) for p in [(1,1),(81,80),(33,32),(21,20),(16,15),(12,11),(11,10),(10,9),(9,8),(8,7),(7,6),
          (32,27),(6,5),(11,9),(5,4),(14,11),(9,7),(21,16),(4,3),(27,20),(11,8),(7,5),(10,7),(16,11),(40,27),(3,2),
          (32,21),(14,9),(11,7),(8,5),(18,11),(5,3),(27,16),(12,7),(7,4),(16,9),(9,5),(20,11),(11,6),(15,8),
          (40,21),(64,33),(160,81)]]
PARTCH_C = [S.cents(float(r)) for r in PARTCH]

def subset_report(ivals):
    out = []
    for name, step in GRIDS.items():
        worst = max(abs(c - step*round(c/step)) for c in ivals)
        out.append(f"{name}: worst deviation {worst:.1f} c")
    worst = max(min(abs((c % 1200) - p) for p in PARTCH_C + [1200]) for c in ivals)
    out.append(f"Partch 43 (octave-reduced): worst deviation {worst:.1f} c")
    return out

if __name__ == "__main__":
    for name, k in CANDS.items():
        Pc, pat, L, s, ev = mode_from(**k)
        print("="*78); print(name, f"  generator {k['g']:.2f} c, {k['n']} notes, pattern {S.pattern_string(pat, L)}, L={L:.1f} s={s:.1f} L/s={L/s:.2f}")
        print(f"  generator ok: {S.generator_ok(k['g'])}   consonances: {len(ev['cons'])} (12-TET-alien {ev['septimal']})   "
              f"novel: {ev['novel']*100:.0f} %   spicy: {[round(c,1) for c,_,_ in ev['spicy']]}   >40c-from-anything: {ev['toofar']}")
        for c, frac, err, d12, fam in ev["rows"]:
            tag = "CONS" if abs(err) <= 8 else ("SPICY" if 20 <= fam <= 40 else "-")
            print(f"    {c:8.1f} c  ratio {220*2**(c/1200):8.3f}  nearest {str(frac):>5} err {err:+5.1f}  12TET {d12:4.1f}  {tag}")
        for line in subset_report(ev["ivals"]): print("    " + line)
