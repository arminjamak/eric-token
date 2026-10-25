#!/usr/bin/env python3
"""Measure the pitch actually sung in vocal.wav and compare it with the target table frequencies."""
import json, wave, numpy as np, pyworld as pw
song = json.load(open("song.json")); pulse = song["pulse"]
w = wave.open("vocal.wav"); sr = w.getframerate()
x = (np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16) / 32768.0).astype(np.float64)
f0, t = pw.dio(x, sr, frame_period=5.0, f0_floor=60, f0_ceil=500); f0 = pw.stonemask(x, f0, t, sr)
errs = []
for ev in song["events"]["vocal"]:
    a, b = ev["t"] * pulse + 0.09, (ev["t"] + ev["d"]) * pulse - 0.06
    if b - a < 0.08: continue
    seg = f0[int(a / 0.005): int(b / 0.005)]; seg = seg[seg > 0]
    if len(seg) < 5: continue
    errs.append((1200 * np.log2(np.median(seg) / ev["f"][0]), ev["syl"], ev["f"][0]))
e = np.array([x[0] for x in errs])
print(f"{len(e)} sung notes measured; median |error| {np.median(np.abs(e)):.1f} c, 90th percentile {np.percentile(np.abs(e), 90):.1f} c, "
      f"within 15 c: {np.mean(np.abs(e) < 15)*100:.0f} %")
print("worst:", [(round(a, 1), s, round(f, 1)) for a, s, f in sorted(errs, key=lambda z: -abs(z[0]))[:5]])
