#!/usr/bin/env python3
"""
Matched-spectrum timbre for the chosen scale (candidate A) and its Sethares roughness curve.

Partials are placed on the scale's own period (12/5), on the pillar degree (the tempered 3/2, ratio r4),
on pillar*period, pillar^2*period (= the 9/4 degree one period up) and on the 7/5 degree one period up,
so that two tones a pillar, a period, a 7/5 or a 9/4 apart share partials and therefore do not beat.
"""
import math
import candidates as C
import scale_search as S

P = 12/5
G = (S.cents(8/7) + S.cents(12/5)) / 5                  # generator, cents
Pc = S.cents(P)
NAMES = ["Vum", "Tol", "Siri", "Kun", "Mor", "Ovit", "Hilu", "Zish", "Nimo"]
degs_c = [0.0]
pat = C.mode_from(P, G, 9, 0)[1]
for st in pat[:-1]: degs_c.append(degs_c[-1] + st)
ratios = [2 ** (c / 1200) for c in degs_c]           # scale degree ratios r0..r8
r3, r4 = ratios[3], ratios[4]

# partial ratio (relative to the fundamental), relative amplitude.
# The spectrum is the scale's frame: period and pillar, iterated (variant i in the search log).
# A draft that also carried the 9/4 degree and 7/5-degree partials was rejected because two
# partials 118 c apart made every single tone rough (intrinsic roughness 0.054 vs 0.011 here).
PARTIALS = [
    (1.0,            1.00),   # fundamental
    (r4,             0.55),   # pillar  (tempered 3/2, 698.7 c)
    (P,              0.50),   # period  12/5
    (r4 * P,         0.35),   # pillar + period
    (P * P,          0.22),   # 2 periods
    (r4 * P * P,     0.12),   # pillar + 2 periods
    (P * P * P,      0.06),   # 3 periods
]

def sethares_pair(f1, f2, a1, a2):
    # Sethares (1993/2005) roughness between two sinusoids
    dstar, s1, s2, b1, b2 = 0.24, 0.0207, 18.96, 3.5, 5.75
    fmin = min(f1, f2); s = dstar / (s1 * fmin + s2); x = abs(f2 - f1)
    return min(a1, a2) * (math.exp(-b1 * s * x) - math.exp(-b2 * s * x))

def roughness(partials_a, partials_b):
    tot = 0.0
    allp = partials_a + partials_b
    for i in range(len(allp)):
        for j in range(i + 1, len(allp)):
            tot += sethares_pair(allp[i][0], allp[j][0], allp[i][1], allp[j][1])
    return tot

def tone(f0): return [(f0 * r, a) for r, a in PARTIALS]
def harmonic_tone(f0, n=9): return [(f0 * k, 1.0 / k) for k in range(1, n + 1)]

def curve(f0=220.0, maker=tone, lo=0.0, hi=Pc + 40, step=2.0):
    pts = []
    c = lo
    while c <= hi:
        pts.append((c, roughness(maker(f0), maker(f0 * 2 ** (c / 1200)))))
        c += step
    return pts

if __name__ == "__main__":
    print("Partials (ratio, amplitude):")
    for r, a in PARTIALS: print(f"   {r:7.4f}  ({S.cents(r):7.1f} c)  amp {a:.2f}")
    self_r = roughness(tone(220.0), []) 
    print(f"\nIntrinsic roughness of one tone at 220 Hz: {self_r:.3f}   (harmonic 9-partial tone: {roughness(harmonic_tone(220.0), []):.3f})")
    pts = curve()
    vals = dict(pts)
    base = roughness(tone(220.0), tone(220.0))
    print(f"\nRoughness of the designed timbre against itself at every scale interval (unison = {base:.3f}):")
    for i, c in enumerate(degs_c[1:] + [Pc], start=1):
        # local minimum test within +-40 c
        nb = [v for cc, v in pts if abs(cc - c) <= 40]
        here = roughness(tone(220.0), tone(220.0 * 2 ** (c / 1200)))
        tag = "local minimum" if here <= min(nb) + 1e-9 else ""
        print(f"   {NAMES[i % 9]:>6} {c:8.1f} c   roughness {here:.3f}   {tag}")
    # the strongest minima in the curve
    mins = [(c, v) for (c0, v0), (c, v), (c2, v2) in zip(pts, pts[1:], pts[2:]) if v < v0 and v < v2 and c > 30]
    mins.sort(key=lambda t: t[1])
    print("\nDeepest minima of the curve (cents, roughness):", [(round(c), round(v, 3)) for c, v in mins[:8]])
    # compare: same scale with a plain harmonic timbre
    print("\nSame intervals with a plain harmonic 9-partial timbre:")
    for i, c in enumerate(degs_c[1:] + [Pc], start=1):
        here = roughness(harmonic_tone(220.0), harmonic_tone(220.0 * 2 ** (c / 1200)))
        print(f"   {NAMES[i % 9]:>6} {c:8.1f} c   roughness {here:.3f}")
