# Event Horizon Lullaby — dreamscape re-score

A new backing track, written as a **Csound** program, for the vocal take
`recording01_04_1_Armin_Clean`. The vocal is split into lead and backing
parts and laid over the new music.

| file | what it is |
|---|---|
| `dreamscape.csd` | The whole backing track as Csound code: harmony, form, every instrument, and the FX/mix bus |
| `separate_vocals.sh` | Splits the vocal stem into **lead** and **backing vocals** with a Mel-Band-Roformer karaoke model |
| `split_stems.py` | Splits Csound's 18-channel render into stereo stems |
| `mix.py` | Vocal processing and the overlay onto the new track |
| `output/*.mp3` | Rendered results: combined mix, backing track only, lead and backing vocals |
| `oscilloscope_xy.png` | The oscilloscope voice drawn on a real X/Y scope (L = x, R = y) |

## The music

* **Locked to the vocal.** The original is 112.2 BPM, with its first downbeat at 0.258 s. The vocal is pitch-tracked
  as E♭ major with lydian A-naturals, sung about +7 cents sharp, so everything is tuned to A4 = 442 Hz.
  The chords in bars 4–24 were picked against the melody to fit it. One example is the long B♭ in bars 15–16,
  held over C♭maj7♯11 and then B♭7sus.
* **Dream pop / dark pop.** Detuned saw pads run through a Moog ladder with tape-wobble drift. Borrowed dark
  chords appear (G♭maj7, C♭maj7, A♭m6, E♭m9). The drums are a half-time groove that grows into a dark-pop
  drive with sidechain pumping and hat rolls. There is a shimmer reverb (the tail is pitched up an octave and
  fed back) and a dotted-8th ping-pong delay.
* **Motives shift with the form.** The glassy FM "starlight" arpeggio changes shape in each section:
  * intro/verse A: an airy 8th-note wave
  * verse B: a dotted-8th line that drifts against the bar
  * voyage: 16ths with a 3-against-5 cycle
  * dissolve: falling triplets with octave leaps
  * outro: the intro wave played backwards
* **Theremin.** One continuous voice that glides between notes. Its vibrato only deepens while the pitch
  holds still, as a real player's hand would. It answers the singer in the gaps, carries the melody in the
  instrumental "voyage", and dives through the surreal E-major drift. It is mixed about 10 dB under the vocal
  and pads.
* **Oscilloscope.** Three sounds:
  * Lissajous voices: stereo sine pairs (L = f, R = f × 3/2, 5/4, 2 …) with slow detune, so the figure turns
    on an X/Y scope
  * trace "pings" on the 16th grid
  * time-base sweeps that rise into section changes

Form (bars of 2.139 s): intro 0–3 · verse A 4–16 · verse B 17–24 · voyage 25–40 ·
dissolve 41–52 · outro 53–61.

## Reproduce

```bash
apt-get install csound ffmpeg
pip install "audio-separator[cpu]" pedalboard pyloudnorm soundfile soxr scipy

./separate_vocals.sh vocals_KITS.wav sep/          # lead + backing vocals
csound dreamscape.csd                              # -> dreamscape_multitrack.wav (18 ch)
python3 split_stems.py dreamscape_multitrack.wav stems/
python3 mix.py stems/00_master.wav "sep/<lead>.wav" "sep/<backing>.wav" out/
```

`mix.py` keeps the vocals at their original timing. It adds a vocal-keyed dynamic EQ that dips the
backing's 250 Hz–5 kHz band by up to 3.5 dB, only while someone is singing. It also applies gentle bus
glue and a look-ahead limiter at −1 dBFS, and sets loudness to −14 LUFS.
