#!/usr/bin/env python3
"""
Synthesize the sung vocal of song.json.

Method: a neural male speaking voice (Piper, en-US "ryan") is driven at the phoneme level, one
lyric syllable at a time. Each syllable is analysed with the WORLD vocoder, its vowel is
time-stretched to the note length, and its pitch contour is replaced by the exact Morsiri
frequency of the note (from song.json, i.e. 220 Hz * ratio[degree] * (12/5)^k) with vibrato,
portamento and a small onset scoop. The spectral envelope (the formants, the "who") is kept,
so the result is the same man singing. A second pass with slightly shifted formants makes
the harmony voice of the final chorus.

Outputs vocal.wav and harmony.wav (44.1 kHz mono).
"""
import json, glob, sys, wave, math
import numpy as np, pyworld as pw
from piper import PiperVoice
from piper.config import SynthesisConfig

SONG = json.load(open("song.json")); PULSE = SONG["pulse"]
OUT_SR = 44100; FP = 5.0                                  # WORLD frame period, ms
voice = PiperVoice.load(glob.glob("voices/*.onnx")[0]); SR = voice.config.sample_rate
TOTAL = int((SONG["bars"] * 7 * PULSE + 5) * SR)
WORD_FIX = {"evry": "every"}
VOWELS = set("aeiouæɐɑɒɔəɚɛɜɝɪʊʌɨɵøyɘɤɞɯʉᵻɨ"); OFFGLIDE = set("ɪʊə")
rng = np.random.default_rng(7)

def units(phs):
    """attach stress and length marks to their phonemes -> list of (base, string)"""
    out, pending = [], ""
    for p in phs:
        if p in ("ˈ", "ˌ"): pending += p; continue
        if p in ("ː", "ˑ") and out: out[-1] = (out[-1][0], out[-1][1] + p); continue
        if p in (" ", ",", ".", "'", "-", "?", "!"): continue
        out.append((p, pending + p)); pending = ""
    return out

def syllabify(phs):
    u = units(phs); isv = [b in VOWELS for b, _ in u]
    nuclei, i = [], 0
    while i < len(u):
        if isv[i]:
            j = i
            if j + 1 < len(u) and isv[j + 1] and u[j + 1][0] in OFFGLIDE and u[j][0] not in OFFGLIDE: j += 1  # diphthong
            nuclei.append((i, j)); i = j + 1
        else: i += 1
    if not nuclei: return [[s for _, s in u]]
    starts = []
    for k, (a, b) in enumerate(nuclei):
        if k == 0: starts.append(0)
        else:
            gap = a - nuclei[k - 1][1] - 1                  # consonants between the nuclei
            starts.append(nuclei[k - 1][1] + 1 + (1 if gap >= 2 else 0))
    return [[s for _, s in u[starts[k]:(starts[k + 1] if k + 1 < len(starts) else len(u))]] for k in range(len(starts))]

def synth_phonemes(phs):
    flat = [c for unit in phs for c in unit]              # "ˈɛ" -> ["ˈ", "ɛ"]: Piper wants single phonemes
    x = voice.phoneme_ids_to_audio(voice.phonemes_to_ids(flat), SynthesisConfig(length_scale=1.4)).astype(np.float64)
    env = np.abs(x); idx = np.where(env > env.max() * 0.02)[0]
    return x[max(0, idx[0] - 150): min(len(x), idx[-1] + 300)]

def analyze(x):
    f0, t = pw.dio(x, SR, frame_period=FP, f0_floor=60, f0_ceil=400)
    f0 = pw.stonemask(x, f0, t, SR)
    return f0, pw.cheaptrick(x, f0, t, SR), pw.d4c(x, f0, t, SR)

def warp_formants(sp, factor):
    nb = sp.shape[1]; src = np.clip(np.arange(nb) / factor, 0, nb - 1); base = np.arange(nb)
    return np.array([np.interp(src, base, row) for row in sp])

def frame_energy_db(x, n):
    hop = int(SR * FP / 1000)
    e = np.array([np.sqrt((x[i * hop:(i + 1) * hop] ** 2).mean()) if (i + 1) * hop <= len(x) else 0 for i in range(n)])
    return 20 * np.log10(e + 1e-9)

def render(x, notes, prev_hz, phrase_start, phrase_end, formant=1.0, vib_depth=11.0):
    """notes: [(hz, seconds), ...] (several = melisma). Returns (audio, seconds of consonant onset before the vowel)."""
    f0, sp, ap = analyze(x)
    if formant != 1.0: sp = warp_formants(sp, formant)
    n = len(f0)
    # the vowel core is defined by ENERGY (within 14 dB of the loudest frame), not by the pitch tracker,
    # which happily calls a quiet aspiration "voiced"
    edb = frame_energy_db(x, n); loud = np.where(edb > edb.max() - 14)[0]
    i0, i1 = loud[0], loud[-1]
    if (f0[i0:i1 + 1] > 0).mean() < 0.5:                  # tracker missed the voicing (short "zi", "ry"): force it
        mid0, mid1 = i0 + (i1 - i0) // 5, i1 - (i1 - i0) // 5
        ap[mid0:mid1 + 1] = np.minimum(ap[mid0:mid1 + 1], 0.12)
    onset, coda = min(i0, 30), min(n - 1 - i1, 22)
    total = sum(d for _, d in notes); gap = 0.035 if phrase_end else 0.02
    N = max(int(round((total - gap) * 1000 / FP)), 12)
    core = N - onset - coda
    if core < 8:                                           # very short note: squeeze the consonants too
        scale = max(N - 8, 0) / max(onset + coda, 1)
        onset, coda = int(onset * scale), int(coda * scale); core = N - onset - coda
    # stretch only the steady middle of the vowel; its first and last 30 ms keep their natural speed
    edge = min(6, (i1 - i0) // 3, core // 3)
    head = np.arange(i0, i0 + edge); tail = np.arange(i1 - edge + 1, i1 + 1)
    middle = np.linspace(i0 + edge, i1 - edge, core - 2 * edge) if core - 2 * edge > 0 else np.array([])
    idx = np.concatenate([np.arange(i0 - onset, i0), head, middle, tail, np.arange(i1 + 1, i1 + 1 + coda)]).round().astype(int)
    idx = np.clip(idx, 0, n - 1)
    sp2, ap2 = sp[idx], ap[idx]
    N = len(idx)
    # target pitch contour over the core, note by note, with glides between notes
    tgt = np.zeros(N); cum = 0.0; frame_s = FP / 1000
    bounds = []
    for hz_, d in notes:
        a = onset + int(round(cum / total * core)); cum += d
        b = onset + int(round(cum / total * core)); bounds.append((a, b, hz_))
    tgt[:onset] = notes[0][0]; tgt[onset + core:] = notes[-1][0]
    for a, b, hz_ in bounds: tgt[a:b] = hz_
    logf = np.log2(tgt)
    for k in range(1, len(bounds)):                        # glide into each inner note
        a = bounds[k][0]; g = min(10, a - onset, N - a)
        if g > 1: logf[a - g // 2: a - g // 2 + g] = np.linspace(np.log2(bounds[k - 1][2]), np.log2(bounds[k][2]), g)
    cents = np.zeros(N); tt = (np.arange(N) - onset) * frame_s
    if prev_hz is not None:                                # portamento from the previous syllable of the word
        g = min(12, core); cents[onset:onset + g] += np.linspace(1200 * np.log2(prev_hz / notes[0][0]), 0, g)
    elif phrase_start:                                     # a small upward scoop at phrase starts
        g = min(14, core); cents[onset:onset + g] += np.linspace(-35, 0, g)
    depth = np.clip((tt - 0.18) / 0.32, 0, 1) * vib_depth  # vibrato fades in after 180 ms
    cents += depth * np.sin(2 * np.pi * (5.3 + rng.normal(0, 0.15)) * tt + rng.uniform(0, 6.28))
    cents += np.convolve(rng.normal(0, 1, N), np.ones(25) / 25, mode="same") * 2.5
    f0new = 2 ** (logf + cents / 1200)
    y = pw.synthesize(f0new, sp2, ap2, SR, FP)
    fi = int(0.012 * SR); fo = int((0.14 if phrase_end else 0.05) * SR)
    y[:fi] *= np.linspace(0, 1, fi)
    if fo < len(y): y[-fo:] *= np.linspace(1, 0, fo) ** 1.5
    return y, onset * frame_s

def group(events):
    """vocal events -> words -> syllables -> notes"""
    syls = []
    for ev in events:
        if ev.get("melisma"): syls[-1]["notes"].append((ev["f"][0], ev["d"] * PULSE)); syls[-1]["end"] = ev["t"] + ev["d"]
        else: syls.append(dict(text=ev["syl"], t=ev["t"], end=ev["t"] + ev["d"], notes=[(ev["f"][0], ev["d"] * PULSE)]))
    words, cur = [], []
    for s in syls:
        cur.append(s)
        if not s["text"].endswith("-"): words.append(cur); cur = []
    return words, syls

def sing(events, formant=1.0, amp=1.0, label="vocal"):
    track = np.zeros(TOTAL)
    words, syls = group(events)
    for wi, w in enumerate(words):
        text = "".join(s["text"].rstrip("-") for s in w); text = WORD_FIX.get(text.lower(), text)
        phs = [p for p in voice.phonemize(text)[0]]
        parts = syllabify(phs)
        if len(parts) != len(w):
            print(f"   [{label}] '{text}': lyric has {len(w)} syllables, phonemizer {len(parts)} -> adapting", file=sys.stderr)
            if len(parts) > len(w): parts = parts[:len(w) - 1] + [sum(parts[len(w) - 1:], [])]
            else:
                # fewer phonetic syllables than notes groups: merge the remaining note groups into a melisma
                notes_all = [n for s in w for n in s["notes"]]
                w = [dict(w[0], notes=notes_all, end=w[-1]["end"])]
        prev_hz = None
        for si, (s, ph) in enumerate(zip(w, parts)):
            x = synth_phonemes(ph)
            nxt_t = next((o["t"] for o in syls if o["t"] >= s["end"]), None)
            phrase_end = nxt_t is None or nxt_t > s["end"] + 1e-6
            phrase_start = (si == 0) and (wi == 0 or words[wi - 1][-1]["end"] < s["t"] - 1e-6)
            y, onset_s = render(x, s["notes"], prev_hz, phrase_start, phrase_end, formant)
            start = int((s["t"] * PULSE - onset_s) * SR)                 # consonant lands before the beat, vowel on it
            end = min(start + len(y), TOTAL)
            track[start:end] += y[:end - start] * amp
            prev_hz = s["notes"][-1][0]
    return track

def write(path, x):
    x = x / max(np.abs(x).max(), 1e-9) * 0.9
    t_in = np.arange(len(x)) / SR; t_out = np.arange(int(len(x) * OUT_SR / SR)) / OUT_SR
    y = np.interp(t_out, t_in, x)
    w = wave.open(path, "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(OUT_SR)
    w.writeframes((y * 32767).astype(np.int16).tobytes()); w.close()
    print(f"wrote {path}: {len(y)/OUT_SR:.1f} s")

if __name__ == "__main__":
    write("vocal.wav", sing(SONG["events"]["vocal"], 1.0, 1.0, "lead"))
    write("harmony.wav", sing(SONG["events"]["harmony"], 0.94, 1.0, "harmony"))
