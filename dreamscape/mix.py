#!/usr/bin/env python3
"""Overlay the separated lead + backing vocals onto the Csound dreamscape.

    python3 mix.py BACKING.wav LEAD.wav BACKVOX.wav OUT_DIR

BACKING  stereo master rendered by dreamscape.csd (already on the vocal grid)
LEAD     lead vocal from the karaoke split
BACKVOX  backing vocals from the karaoke split

The vocals are kept at their original timing. The backing track gets a
vocal-keyed dynamic EQ: its 250 Hz - 5 kHz band dips (up to ~3.5 dB) only
while the singer is singing, so the voice sits *in* the dream rather than on
top of it.
"""
import os
import sys

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
import soxr
from pedalboard import (Chorus, Compressor, Delay, HighpassFilter, HighShelfFilter, LowpassFilter,
                        PeakFilter, Pedalboard, Reverb)
from scipy.ndimage import minimum_filter1d
from scipy.signal import butter, resample_poly, sosfilt, sosfiltfilt

SR = 48000
BEAT = 60 / 112.2034
TARGET_LUFS = -14.0


def load(path, channels):
    x, sr = sf.read(path, dtype="float32", always_2d=True)
    x = x[:, :2]
    if sr != SR:
        x = soxr.resample(x, sr, SR, quality="VHQ")
    if channels == 1:
        return x.mean(axis=1, keepdims=True)
    return x if x.shape[1] == 2 else np.repeat(x, 2, axis=1)


def fit(x, n):
    return x[:n] if len(x) >= n else np.pad(x, ((0, n - len(x)), (0, 0)))


def run(board, x):
    return board(x.T.copy(), SR).T


def lr4(x, fc, kind):
    """Linkwitz-Riley 4th order (two cascaded Butterworths) - bands sum flat."""
    sos = butter(2, fc, btype=kind, fs=SR, output="sos")
    return sosfilt(sos, sosfilt(sos, x, axis=0), axis=0)


def envelope(x, attack, release):
    """Peak-ish envelope follower with separate attack/release (seconds)."""
    rect = np.abs(x).max(axis=1)
    rect = sosfiltfilt(butter(2, 30, fs=SR, output="sos"), rect)
    hop = SR // 1000                       # run the follower at 1 kHz
    ctl = rect[::hop]
    a_up, a_dn = np.exp(-1 / (attack * 1000)), np.exp(-1 / (release * 1000))
    env = np.empty_like(ctl)
    e = 0.0
    for i, v in enumerate(ctl):
        coef = a_up if v > e else a_dn
        e = coef * e + (1 - coef) * v
        env[i] = e
    return np.interp(np.arange(len(rect)), np.arange(len(ctl)) * hop, env)


def ride(x, max_boost_db=9.0, max_cut_db=4.0, window=1.5):
    """Phrase-level fader ride: pull each phrase toward the take's typical level."""
    hop = SR // 100
    frames = x[: len(x) // hop * hop, 0].reshape(-1, hop)
    db = 10 * np.log10(np.mean(frames ** 2, axis=1) + 1e-12)
    voiced = db > db.max() - 40
    w = int(window * 100)
    k = np.ones(w)
    num = np.convolve(np.where(voiced, 10 ** (db / 10), 0), k, "same")
    den = np.convolve(voiced.astype(float), k, "same")
    local = np.where(den > 0, 10 * np.log10(num / np.maximum(den, 1) + 1e-12), np.nan)
    target = np.nanpercentile(local[voiced], 75)
    gain_db = np.clip(np.nan_to_num(target - local, nan=0.0), -max_cut_db, max_boost_db)
    gain_db = np.convolve(gain_db, np.ones(50) / 50, "same")     # 0.5 s smoothing
    g = np.interp(np.arange(len(x)), np.arange(len(gain_db)) * hop + hop / 2, 10 ** (gain_db / 20))
    return x * g[:, None].astype(np.float32)


def limit(x,ceiling_db=-1.0, release=0.12):
    """Transparent look-ahead peak limiter (4x oversampled peak detection)."""
    c = 10 ** (ceiling_db / 20)
    peak = np.abs(resample_poly(x, 4, 1, axis=0)).max(axis=1).reshape(-1, 4).max(axis=1)[:len(x)]
    req = np.minimum(1.0, c / np.maximum(peak, 1e-9))
    hop = SR // 1000
    pad = (-len(req)) % hop
    blk = np.pad(req, (0, pad), constant_values=1).reshape(-1, hop).min(axis=1)
    blk = minimum_filter1d(blk, size=7)                 # +-3 ms look-ahead
    a = np.exp(-1 / (release * 1000))
    g = np.empty_like(blk)
    s = 1.0
    for i, v in enumerate(blk):
        s = v if v < s else a * s + (1 - a) * v
        g[i] = s
    g = np.interp(np.arange(len(x)), np.arange(len(g)) * hop + hop / 2, g)
    return np.clip(x * g[:, None], -c, c)


def main(backing_path, lead_path, bvox_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    meter = pyln.Meter(SR)

    backing = load(backing_path, 2)
    n = len(backing)
    lead = fit(load(lead_path, 1), n)
    bvox = fit(load(bvox_path, 2), n)

    # ---- vocal rider: lift the softly sung opening phrases toward the rest
    lead = ride(lead)

    # ---- lead vocal: clean, present, softly glued
    lead_dry = run(Pedalboard([
        HighpassFilter(85),
        PeakFilter(300, -2.5, 1.0),         # de-mud
        PeakFilter(3400, 2.0, 0.8),         # presence
        HighShelfFilter(10000, 2.0, 0.7),   # air
        Compressor(threshold_db=-22, ratio=3.0, attack_ms=6, release_ms=90),
        Compressor(threshold_db=-12, ratio=6.0, attack_ms=1, release_ms=40),  # peak catcher
    ]), lead)
    lead_st = np.repeat(lead_dry, 2, axis=1)

    # ---- backing vocals: thinner, wider, further back
    bvox_dry = run(Pedalboard([
        HighpassFilter(160),
        LowpassFilter(11000),
        PeakFilter(2500, -2.0, 1.0),
        Compressor(threshold_db=-24, ratio=4.0, attack_ms=8, release_ms=120),
        Chorus(rate_hz=0.35, depth=0.18, centre_delay_ms=9, feedback=0.0, mix=0.4),
    ]), bvox)
    haas = int(0.012 * SR)
    bvox_dry[:, 1] = np.concatenate([np.zeros(haas, np.float32), bvox_dry[:-haas, 1]])

    # ---- shared vocal space: dreamy plate-ish reverb + dotted-8th echo
    verb = Pedalboard([HighpassFilter(250), LowpassFilter(8000),
                       Reverb(room_size=0.82, damping=0.55, wet_level=1.0, dry_level=0.0, width=1.0)])
    echo = Pedalboard([HighpassFilter(400), LowpassFilter(4500),
                       Delay(delay_seconds=0.75 * BEAT, feedback=0.32, mix=1.0)])
    vox_bus = lead_st + 0.5 * bvox_dry
    wet = 0.22 * run(verb, lead_st + 0.9 * bvox_dry) + 0.09 * run(echo, lead_st)
    wet[:, 1] = np.concatenate([np.zeros(int(0.019 * SR), np.float32), wet[:-int(0.019 * SR), 1]])
    vox = vox_bus + wet

    # ---- vocal-keyed dynamic EQ on the backing (smooth make-room)
    low = lr4(backing, 250, "low")
    rest = lr4(backing, 250, "high")
    mid = lr4(rest, 5000, "low")
    high = lr4(rest, 5000, "high")
    env = envelope(lead_dry + bvox_dry.mean(axis=1, keepdims=True) * 0.5, attack=0.05, release=0.45)
    key = np.clip(env / (np.percentile(env[env > 1e-4], 70) + 1e-9), 0, 1)
    duck_db = -3.5 * key
    duck = (10 ** (duck_db / 20))[:, None]
    backing_ducked = low + mid * duck + high * (1 - (1 - duck) * 0.4)

    # ---- set vocal level relative to the music during the sung section
    sung = env > 0.02 * env.max()
    seg = np.where(sung)[0]
    a, b = seg[0], seg[-1]
    music_lufs = meter.integrated_loudness(backing_ducked[a:b])
    vox_lufs = meter.integrated_loudness(vox[a:b])
    vox_gain = 10 ** ((music_lufs + 2.5 - vox_lufs) / 20)   # voice ~2.5 LU above the bed
    vox *= vox_gain

    mix = backing_ducked + vox
    master = Pedalboard([
        Compressor(threshold_db=-16, ratio=1.8, attack_ms=25, release_ms=250),
    ])
    mix = run(master, mix)

    def finish(x):
        g = 10 ** ((TARGET_LUFS - meter.integrated_loudness(x)) / 20)
        return limit(x * g)

    out = {
        "dreamscape_combined.wav": finish(mix),
        "dreamscape_backing_track.wav": finish(backing),
        "vocals_lead_processed.wav": vox_gain * (lead_st + 0.22 * run(verb, lead_st)),
        "vocals_backing_processed.wav": vox_gain * 0.5 * bvox_dry,
    }
    for name, x in out.items():
        sf.write(os.path.join(out_dir, name), x, SR, subtype="PCM_24")
        print(f"{name:32s} LUFS {meter.integrated_loudness(x):6.1f}  peak {20*np.log10(np.abs(x).max()):5.1f} dBFS")
    print(f"vocal gain {20*np.log10(vox_gain):+.1f} dB, sung region {a/SR:.1f}-{b/SR:.1f}s, max duck {duck_db.min():.1f} dB")


if __name__ == "__main__":
    main(*sys.argv[1:5])
