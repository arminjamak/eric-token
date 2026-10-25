#!/usr/bin/env python3
"""
The crooner. Synthesizes the vocal of song.json.

A neural male speaking voice (Piper, en-US "ryan") is synthesized one WORD at a time, so the
consonant-to-vowel transitions inside words are the voice's own. Each word is analysed with the
WORLD vocoder and segmented into its syllables at the dips of a sonority curve. Every vowel is
time-stretched (only its steady middle) to the note length and its pitch contour is replaced by
the exact Morsiri frequency from song.json, with a crooner's phrasing: late, lazy onsets, a scoop
into phrase starts, a fall-off at phrase ends, slow vibrato that arrives late, portamento inside
words, and a breath before each phrase. The spectral envelope is kept (slightly warmed), so it is
the same man throughout. Output: vocal.wav, 44.1 kHz mono.
"""
import json, glob, sys, wave
import numpy as np, pyworld as pw
from piper import PiperVoice
from piper.config import SynthesisConfig

SONG = json.load(open("song.json")); UNIT = SONG["pulse"]
OUT_SR = 44100; FP = 5.0; HOP = None
voice = PiperVoice.load(glob.glob("voices/*.onnx")[0]); SR = voice.config.sample_rate; HOP = int(SR * FP / 1000)
TOTAL = int((SONG["bars"] * SONG["units_per_bar"] * UNIT + 6) * SR)
WORD_FIX = {"evry": "every"}
VOWELS = set("aeiouæɐɑɒɔəɚɛɜɝɪʊʌɨɵøyɘɤɞɯʉᵻ"); OFFGLIDE = set("ɪʊə")
rng = np.random.default_rng(11)
FORMANT = 0.96          # a slightly longer vocal tract: warmer baritone
VIB_HZ, VIB_C, VIB_ON = 4.8, 9.0, 0.25

def phonemes(word):
    return [p for p in voice.phonemize(word)[0] if p not in (" ", ",", ".", "?", "!", "-")]

def count_syllables(phs):
    """number of vowel nuclei, with off-glides merged into diphthongs"""
    n = 0; prev_v = False; prev_base = ""
    for p in phs:
        if p in VOWELS:
            if not (prev_v and p in OFFGLIDE and prev_base not in OFFGLIDE): n += 1
            prev_v, prev_base = True, p
        elif p not in ("ˈ", "ˌ", "ː", "ˑ"): prev_v = False
    return n

def synth_word(phs, length_scale=1.3):
    x = voice.phoneme_ids_to_audio(voice.phonemes_to_ids(phs), SynthesisConfig(length_scale=length_scale)).astype(np.float64)
    env = np.abs(x); idx = np.where(env > env.max() * 0.015)[0]
    return x[max(0, idx[0] - 200): min(len(x), idx[-1] + 400)]

def analyze(x):
    f0, t = pw.dio(x, SR, frame_period=FP, f0_floor=60, f0_ceil=400)
    f0 = pw.stonemask(x, f0, t, SR)
    return f0, pw.cheaptrick(x, f0, t, SR), pw.d4c(x, f0, t, SR)

def energy_db(x, n):
    e = np.array([np.sqrt((x[i * HOP:(i + 1) * HOP] ** 2).mean()) if (i + 1) * HOP <= len(x) else 0 for i in range(n)])
    return 20 * np.log10(e + 1e-9)

def sonority(sp, edb):
    """low-band loudness: vowels are loud and low, consonants are not"""
    nb = sp.shape[1]; lo = int(nb * 1000 / (SR / 2))
    s = 10 * np.log10(sp[:, :lo].sum(axis=1) + 1e-12)
    s = np.convolve(s, np.ones(5) / 5, mode="same")
    return s

def segment(sp, edb, k):
    """split a word's frames into k syllables -> list of (start, end) frame ranges"""
    n = len(edb)
    if k == 1: return [(0, n)]
    son = sonority(sp, edb)
    peaks = [i for i in range(1, n - 1) if son[i] >= son[i - 1] and son[i] > son[i + 1] and son[i] > son.max() - 18]
    chosen = []
    for i in sorted(peaks, key=lambda i: -son[i]):
        if all(abs(i - c) >= 9 for c in chosen): chosen.append(i)
        if len(chosen) == k: break
    chosen.sort()
    if len(chosen) < k:                                     # fallback: equal split of the loud region
        loud = np.where(edb > edb.max() - 14)[0]; a, b = loud[0], loud[-1]
        cuts = [0] + [int(a + (b - a) * j / k) for j in range(1, k)] + [n]
        return [(cuts[j], cuts[j + 1]) for j in range(k)]
    bounds = [0]
    for p, q in zip(chosen, chosen[1:]): bounds.append(p + int(np.argmin(son[p:q])))
    bounds.append(n)
    return [(bounds[j], bounds[j + 1]) for j in range(k)]

def core_of(son, a, b):
    """the vowel of a syllable: the frames within 12 dB of the syllable's peak LOW-BAND loudness
    (fricatives are loud but not low, so an 's' or 'ks' no longer counts as vowel)"""
    seg = son[a:b]; loud = np.where(seg > seg.max() - 12)[0]
    return a + loud[0], a + loud[-1]

def render_word(x, syls, phrase_start, phrase_end):
    """syls: list of [(hz, seconds), ...] per syllable (several entries = melisma).
    Returns (audio, seconds by which the word's first consonants precede its first vowel)."""
    f0, sp, ap = analyze(x)
    sp = np.array([np.interp(np.clip(np.arange(sp.shape[1]) / FORMANT, 0, sp.shape[1] - 1), np.arange(sp.shape[1]), row) for row in sp])
    n = len(f0); edb = energy_db(x, n); son = sonority(sp, edb)
    ranges = segment(sp, edb, len(syls))
    cores = [core_of(son, a, b) for a, b in ranges]
    # level the syllables of a word: an unstressed vowel may sit at most 4 dB under the loudest one
    peak = max(son[i0:i1 + 1].mean() for i0, i1 in cores)
    for (a, b), (i0, i1) in zip(ranges, cores):
        gain_db = min(max(peak - 4 - son[i0:i1 + 1].mean(), 0), 10)
        sp[a:b] *= 10 ** (gain_db / 10)
    # if the tracker missed voicing in a vowel core, force it
    for (i0, i1) in cores:
        if (f0[i0:i1 + 1] > 0).mean() < 0.5:
            m0, m1 = i0 + (i1 - i0) // 5, i1 - (i1 - i0) // 5
            ap[m0:m1 + 1] = np.minimum(ap[m0:m1 + 1], 0.12)
    # a little air in the top of the voice
    nb = sp.shape[1]; hi = int(nb * 4000 / (SR / 2))
    ap[:, hi:] = np.maximum(ap[:, hi:], 0.3)
    idx_all, f0_all = [], []
    for j, ((a, b), (i0, i1), notes) in enumerate(zip(ranges, cores, syls)):
        onset = i0 - a                                     # consonant frames before this vowel (natural length)
        coda = b - 1 - i1
        next_onset = (cores[j + 1][0] - ranges[j + 1][0]) if j + 1 < len(syls) else 0
        total = sum(d for _, d in notes)
        N = int(round(total * 1000 / FP)) - (7 if (j == len(syls) - 1 and phrase_end) else 0)
        core = max(N - coda - next_onset, 6)               # the vowel fills the note minus its coda and the next consonants
        edge = min(6, max((i1 - i0) // 3, 1), core // 3)
        head = np.arange(i0, i0 + edge); tail = np.arange(i1 - edge + 1, i1 + 1)
        mid = np.linspace(i0 + edge, i1 - edge, max(core - 2 * edge, 0))
        idx = np.concatenate([np.arange(a, i0), head, mid, tail, np.arange(i1 + 1, b)]).round().astype(int)
        # pitch for this syllable's frames: its notes across the core, consonants take the neighbouring pitch
        m = len(idx); tgt = np.zeros(m); cum = 0.0
        tgt[:onset] = notes[0][0]; tgt[onset + core:] = notes[-1][0]
        prev_hz = notes[0][0]
        for q, (hz_, d) in enumerate(notes):
            s0 = onset + int(round(cum / total * core)); cum += d; s1 = onset + int(round(cum / total * core))
            tgt[s0:s1] = hz_
            if q > 0:                                      # glide between melisma notes
                g = min(8, s1 - s0)
                tgt[s0:s0 + g] = np.exp(np.linspace(np.log(prev_hz), np.log(hz_), g))
            prev_hz = hz_
        idx_all.append(idx); f0_all.append(tgt)
    idx = np.concatenate(idx_all); tgt = np.concatenate(f0_all); N = len(idx)
    logf = np.log2(np.maximum(tgt, 1))
    # portamento into each syllable after the first (from the previous syllable's last pitch)
    pos = 0
    for j in range(1, len(syls)):
        pos += len(idx_all[j - 1]); on = cores[j][0] - ranges[j][0]
        g = min(9, N - pos - on)
        if g > 1: logf[pos + on: pos + on + g] = np.linspace(logf[pos - 1], logf[pos + on + g], g)
    cents = np.zeros(N); first_on = cores[0][0] - ranges[0][0]
    tt = (np.arange(N) - first_on) * FP / 1000
    if phrase_start:                                       # the crooner's scoop
        g = min(18, N - first_on); cents[first_on:first_on + g] += np.linspace(-70, 0, g) ** 1
    if phrase_end:                                         # fall-off at the end of the phrase
        g = min(24, N); cents[N - g:] += np.linspace(0, -30, g)
    depth = np.clip((tt - VIB_ON) / 0.35, 0, 1) * VIB_C
    cents += depth * np.sin(2 * np.pi * (VIB_HZ + rng.normal(0, 0.12)) * tt + rng.uniform(0, 6.28))
    cents += np.convolve(rng.normal(0, 1, N), np.ones(30) / 30, mode="same") * 3.0
    f0new = 2 ** (logf + cents / 1200)
    y = pw.synthesize(f0new, sp[idx], ap[idx], SR, FP)
    fi = int(0.01 * SR); fo = int((0.16 if phrase_end else 0.04) * SR)
    y[:fi] *= np.linspace(0, 1, fi)
    if fo < len(y): y[-fo:] *= np.linspace(1, 0, fo) ** 1.4
    return y, first_on * FP / 1000

def breath(dur=0.32):
    n = int(dur * SR); x = rng.normal(0, 1, n)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1 / SR)
    X *= np.exp(-((np.log(np.maximum(f, 1)) - np.log(1500)) ** 2) / (2 * 0.6 ** 2))
    x = np.fft.irfft(X, n); env = np.sin(np.linspace(0, np.pi, n)) ** 1.5
    return x / np.abs(x).max() * env

def group(events):
    syls = []
    for ev in events:
        if ev.get("melisma"): syls[-1]["notes"].append((ev["f"][0], ev["d"] * UNIT)); syls[-1]["end"] = ev["t"] + ev["d"]
        else: syls.append(dict(text=ev["syl"], t=ev["t"], end=ev["t"] + ev["d"], notes=[(ev["f"][0], ev["d"] * UNIT)]))
    words, cur = [], []
    for s in syls:
        cur.append(s)
        if not s["text"].endswith("-"): words.append(cur); cur = []
    return words, syls

def sing(events):
    track = np.zeros(TOTAL)
    words, syls = group(events)
    for wi, w in enumerate(words):
        text = "".join(s["text"].rstrip("-") for s in w); text = WORD_FIX.get(text.lower(), text)
        phs = phonemes(text)
        k_lyric, k_phon = len(w), count_syllables(phs)
        syl_notes = [s["notes"] for s in w]
        if k_phon != k_lyric:
            print(f"   '{text}': lyric {k_lyric} syllables, phonemizer {k_phon}; using {k_phon} with the notes redistributed", file=sys.stderr)
            if k_phon < k_lyric:   # merge trailing note groups into the last phonetic syllable (melisma)
                syl_notes = syl_notes[:k_phon - 1] + [sum(syl_notes[k_phon - 1:], [])]
            else:                  # more phonetic syllables than notes: give the extras to the last note, split evenly
                extra = k_phon - k_lyric; last = syl_notes[-1]
                total = sum(d for _, d in last)
                syl_notes = syl_notes[:-1] + [[(last[0][0], total / (extra + 1))] for _ in range(extra + 1)]
                if len(last) > 1: syl_notes[-1] = last[1:] + syl_notes[-1][1:]
        x = synth_word(phs)
        t_start = w[0]["t"]; t_end = w[-1]["end"]
        nxt_t = next((o["t"] for o in syls if o["t"] >= t_end), None)
        phrase_end = nxt_t is None or nxt_t > t_end + 1e-6
        phrase_start = wi == 0 or words[wi - 1][-1]["end"] < t_start - 1e-6
        y, onset_s = render_word(x, syl_notes, phrase_start, phrase_end)
        # lazy timing: the crooner sits behind the beat, more so at the start of a phrase
        late = rng.normal(0.075, 0.02) if phrase_start else rng.normal(0.035, 0.012)
        start = int((t_start * UNIT - onset_s + max(late, 0)) * SR)
        end = min(start + len(y), TOTAL); track[start:end] += y[:end - start]
        if phrase_start and (wi == 0 or t_start - words[wi - 1][-1]["end"] >= 2):
            b = breath(); bs = int((t_start * UNIT - 0.38) * SR)
            track[bs:bs + len(b)] += b * 0.028
    return track

def write(path, x):
    x = x / max(np.abs(x).max(), 1e-9) * 0.9
    t_in = np.arange(len(x)) / SR; t_out = np.arange(int(len(x) * OUT_SR / SR)) / OUT_SR
    y = np.interp(t_out, t_in, x)
    w = wave.open(path, "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(OUT_SR)
    w.writeframes((y * 32767).astype(np.int16).tobytes()); w.close()
    print(f"wrote {path}: {len(y)/OUT_SR:.1f} s")

if __name__ == "__main__":
    write("vocal.wav", sing(SONG["events"]["vocal"]))
