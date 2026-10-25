#!/usr/bin/env python3
"""Check the rendered piece: duration, level, and that every strong spectral peak is a
table frequency (degree x period shift) times one of the declared partial ratios."""
import wave, sys, numpy as np, math
import timbre as T

path = sys.argv[1] if len(sys.argv) > 1 else "morsiri.wav"
w = wave.open(path); sr = w.getframerate(); n = w.getnframes()
x = np.frombuffer(w.readframes(n), dtype=np.int16).reshape(-1, w.getnchannels()).mean(axis=1) / 32768
print(f"duration {n/sr:.1f} s   sample rate {sr}   peak {np.abs(x).max():.3f}   rms {np.sqrt((x**2).mean()):.3f}")

# allowed partial frequencies: tonic 220 * ratio[deg] * 2.4^per * partial, per in -2..2
PART = [r for r, a in T.PARTIALS]
allowed = sorted({220 * r * 2.4 ** per * p for r in T.ratios for per in range(-2, 3) for p in PART})
allowed = np.array([f for f in allowed if 30 < f < 8000])

win = 8192; hop = sr // 2   # one analysis frame every 0.5 s
bad = 0; checked = 0; worst = 0.0
for start in range(0, len(x) - win, hop):
    seg = x[start:start + win] * np.hanning(win)
    spec = np.abs(np.fft.rfft(seg)); freqs = np.fft.rfftfreq(win, 1 / sr)
    thresh = spec.max() * 0.2
    if spec.max() < 1.0: continue
    peaks = [i for i in range(2, len(spec) - 2) if spec[i] > thresh and spec[i] > spec[i-1] and spec[i] > spec[i+1] and freqs[i] > 40]
    for i in peaks:
        # parabolic interpolation for a better frequency estimate
        a, b, c = np.log(spec[i-1] + 1e-12), np.log(spec[i] + 1e-12), np.log(spec[i+1] + 1e-12)
        off = 0.5 * (a - c) / (a - 2*b + c) if (a - 2*b + c) != 0 else 0
        f = (i + off) * sr / win
        err = np.min(np.abs(1200 * np.log2(allowed / f)))
        checked += 1; worst = max(worst, err)
        if err > 12: bad += 1; print(f"   unexplained peak {f:.1f} Hz at {start/sr:.1f} s ({err:.1f} c from nearest allowed)")
print(f"spectral peaks checked: {checked}, unexplained (>12 c from any table frequency x partial): {bad}, worst match {worst:.1f} c")

# section-wise loudness (bars of 7 pulses x 0.27 s)
bar = 7 * 0.27
sections = [("intro", 0, 4), ("A", 4, 12), ("B", 12, 20), ("A'", 20, 28), ("ending", 28, 33)]
for name, b0, b1 in sections:
    seg = x[int(b0 * bar * sr): int(b1 * bar * sr)]
    print(f"   {name:7} bars {b0:2}-{b1:2}  {b0*bar:5.1f}-{b1*bar:5.1f} s   rms {np.sqrt((seg**2).mean()):.3f}")
