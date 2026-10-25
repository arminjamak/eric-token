#!/usr/bin/env python3
"""Mix the band (song_instrumental.wav, from SuperCollider) with the voice (vocal.wav, from sing.py)
through a 1930s-flavoured chain: band-limited, gently saturated, a short warm plate, voice up front.
Writes where_the_slow_moon_goes.wav and .mp3 and prints levels per section."""
import wave, subprocess, json, os, numpy as np

SR = 44100
def load(path):
    w = wave.open(path); n = w.getnframes(); ch = w.getnchannels()
    x = np.frombuffer(w.readframes(n), dtype=np.int16).reshape(-1, ch) / 32768.0
    assert w.getframerate() == SR, path
    return x if ch == 2 else np.repeat(x, 2, axis=1)

def fftconv(x, h):
    n = len(x) + len(h) - 1; N = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, N) * np.fft.rfft(h, N), N)[:n]

def room(x, wet, t60=1.3, predelay=0.02, seed=1, damp=8):
    rng = np.random.default_rng(seed); L = int(t60 * SR); out = np.zeros_like(x)
    for c in range(2):
        ir = rng.normal(0, 1, L) * np.exp(-np.arange(L) / (t60 * SR / 6.9))
        ir = np.convolve(ir, np.ones(damp) / damp, mode="same")
        ir = np.concatenate([np.zeros(int(predelay * SR)), ir]); ir /= np.sqrt((ir ** 2).sum())
        out[:, c] = x[:, c] + wet * fftconv(x[:, c], ir)[:len(x)] * 0.5
    return out

def eq(x, hp=None, lp=None, presence=None):
    X = np.fft.rfft(x, axis=0); f = np.fft.rfftfreq(len(x), 1 / SR); g = np.ones_like(f)
    if hp: g *= 1 / np.sqrt(1 + (hp / np.maximum(f, 1e-3)) ** 4)
    if lp: g *= 1 / np.sqrt(1 + (f / lp) ** 6)
    if presence:                                   # (centre Hz, dB) broad bell
        fc, db = presence; g *= 10 ** (db / 20 * np.exp(-((np.log2(np.maximum(f, 1)) - np.log2(fc)) ** 2) / 1.2))
    return np.fft.irfft(X * g[:, None], len(x), axis=0)

def compress(x, thresh_db=-24, ratio=3.0, win=0.03):
    env = np.sqrt(np.convolve((x ** 2).mean(axis=1), np.ones(int(win * SR)) / (win * SR), mode="same")) + 1e-9
    over = np.maximum(20 * np.log10(env) - thresh_db, 0); gain = 10 ** (-over * (1 - 1 / ratio) / 20)
    gain = np.convolve(gain, np.ones(int(0.025 * SR)) / int(0.025 * SR), mode="same")
    return x * gain[:, None]

def rms_db(x, active_only=False):
    p = (x ** 2).mean(axis=1)
    if active_only:
        blocks = p[:len(p) // 4410 * 4410].reshape(-1, 4410).mean(axis=1); p = blocks[blocks > blocks.max() * 0.01]
    return 10 * np.log10(p.mean() + 1e-12)

inst, voc = load("song_instrumental.wav"), load("vocal.wav")
n = max(len(inst), len(voc)); pad = lambda a: np.vstack([a, np.zeros((n - len(a), 2))])
inst, voc = pad(inst), pad(voc)

inst = eq(inst, hp=35, lp=11000); inst *= 10 ** ((-20.5 - rms_db(inst, True)) / 20)
voc = compress(eq(voc, hp=90, lp=9000, presence=(2800, 2.5))); voc *= 10 ** ((-17.5 - rms_db(voc, True)) / 20)
voc = voc * np.array([0.97, 1.0])

mix = room(inst, 0.14, 1.3, seed=2) + room(voc, 0.22, 1.5, seed=3, damp=12)
mix = np.tanh(mix * 1.25) / np.tanh(1.25) * 0.9           # tape-like saturation
mix = eq(mix, hp=30, lp=12500)
mid = mix.mean(axis=1, keepdims=True); mix = mid + (mix - mid) * 0.8   # a slightly narrow, old-record image
mix = mix / np.abs(mix).max() * 0.97

w = wave.open("where_the_slow_moon_goes.wav", "w"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix * 32767).astype(np.int16).tobytes()); w.close()
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "where_the_slow_moon_goes.wav", "-codec:a", "libmp3lame", "-b:a", "192k",
                "-metadata", "title=Where the Slow Moon Goes", "-metadata", "artist=Morsiri scale, synthesized voice",
                "where_the_slow_moon_goes.mp3"], check=True)
song = json.load(open("song.json")); unit = song["pulse"]; upb = song["units_per_bar"]
print(f"mix: {len(mix)/SR:.1f} s, peak {np.abs(mix).max():.2f}, rms {rms_db(mix):.1f} dBFS")
b = 0
for name, bars in song["sections"]:
    seg = mix[int(b * upb * unit * SR): int((b + bars) * upb * unit * SR)]
    print(f"   {name:9} {b*upb*unit:6.1f} s  rms {rms_db(seg):6.1f} dBFS"); b += bars
