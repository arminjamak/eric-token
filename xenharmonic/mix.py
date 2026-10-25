#!/usr/bin/env python3
"""Mix song_instrumental.wav (stereo, from SuperCollider) with vocal.wav and harmony.wav (from sing.py),
add a synthetic room, level, limit, and encode where_the_slow_moon_goes.mp3."""
import wave, subprocess, numpy as np, json

SR = 44100
def load(path):
    w = wave.open(path); n = w.getnframes(); ch = w.getnchannels()
    x = np.frombuffer(w.readframes(n), dtype=np.int16).reshape(-1, ch) / 32768.0
    assert w.getframerate() == SR, path
    return x if ch == 2 else np.repeat(x, 2, axis=1)

def fftconv(x, h):
    n = len(x) + len(h) - 1; N = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, N) * np.fft.rfft(h, N), N)[:n]

def room(x, wet, t60=1.7, predelay=0.025, seed=1):
    """stereo reverb from two decorrelated exponentially decaying noise tails, low-passed"""
    rng = np.random.default_rng(seed); L = int(t60 * SR)
    out = np.zeros_like(x)
    for c in range(2):
        ir = rng.normal(0, 1, L) * np.exp(-np.arange(L) / (t60 * SR / 6.9))
        ir = np.convolve(ir, np.ones(6) / 6, mode="same")                 # darken the tail
        ir = np.concatenate([np.zeros(int(predelay * SR)), ir]); ir /= np.sqrt((ir ** 2).sum())
        y = fftconv(x[:, c], ir)[:len(x)]
        out[:, c] = x[:, c] + wet * y * 0.5
    return out

def highpass(x, fc):
    X = np.fft.rfft(x, axis=0); f = np.fft.rfftfreq(len(x), 1 / SR)
    g = 1 / np.sqrt(1 + (fc / np.maximum(f, 1e-3)) ** 4)
    return np.fft.irfft(X * g[:, None], len(x), axis=0)

def compress(x, thresh_db=-22, ratio=2.5, win=0.04):
    env = np.sqrt(np.convolve((x ** 2).mean(axis=1), np.ones(int(win * SR)) / (win * SR), mode="same")) + 1e-9
    env_db = 20 * np.log10(env)
    over = np.maximum(env_db - thresh_db, 0); gain_db = -over * (1 - 1 / ratio)
    gain = 10 ** (gain_db / 20)
    gain = np.convolve(gain, np.ones(int(0.02 * SR)) / int(0.02 * SR), mode="same")   # smooth
    return x * gain[:, None]

def rms_db(x, active_only=False):
    p = (x ** 2).mean(axis=1)
    if active_only:
        blocks = p[:len(p) // 4410 * 4410].reshape(-1, 4410).mean(axis=1)
        p = blocks[blocks > blocks.max() * 0.01]
    return 10 * np.log10(p.mean() + 1e-12)

inst, voc, har = load("song_instrumental.wav"), load("vocal.wav"), load("harmony.wav")
n = max(map(len, (inst, voc, har)))
pad = lambda a: np.vstack([a, np.zeros((n - len(a), 2))])
inst, voc, har = pad(inst), pad(voc), pad(har)

inst = inst * 10 ** ((-19 - rms_db(inst, True)) / 20)
voc = compress(highpass(voc, 95)); voc = voc * 10 ** ((-18.5 - rms_db(voc, True)) / 20)
har = compress(highpass(har, 110)); har = har * 10 ** ((-25 - rms_db(har, True)) / 20)
# vocal slightly right of centre, harmony slightly left, as two singers at one mic would sit
voc = voc * np.array([0.92, 1.0]); har = har * np.array([1.0, 0.88])

mix = room(inst, 0.10, 1.4, seed=2) + room(voc, 0.26, 1.7, seed=3) + room(har, 0.3, 1.7, seed=4)
mix = highpass(mix, 28)
mix = np.tanh(mix * 1.15 / 0.95) * 0.95                       # gentle soft limiter
mix = mix / np.abs(mix).max() * 0.97

w = wave.open("where_the_slow_moon_goes.wav", "w"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix * 32767).astype(np.int16).tobytes()); w.close()
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "where_the_slow_moon_goes.wav", "-codec:a", "libmp3lame",
                "-b:a", "192k", "-metadata", "title=Where the Slow Moon Goes", "-metadata", "artist=Morsiri scale, synthesized voice",
                "where_the_slow_moon_goes.mp3"], check=True)
song = json.load(open("song.json")); pulse = song["pulse"]
print(f"mix: {len(mix)/SR:.1f} s, peak {np.abs(mix).max():.2f}, rms {rms_db(mix):.1f} dBFS")
b = 0
for name, bars in song["sections"]:
    seg = mix[int(b * 7 * pulse * SR): int((b + bars) * 7 * pulse * SR)]
    print(f"   {name:9} {b*7*pulse:6.1f} s  rms {rms_db(seg):6.1f} dBFS"); b += bars
