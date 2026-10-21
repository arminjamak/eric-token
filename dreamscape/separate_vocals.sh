#!/usr/bin/env bash
# Split an isolated vocal stem into lead and backing vocals with a
# Mel-Band-Roformer karaoke model (pip install "audio-separator[cpu]").
#   ./separate_vocals.sh VOCALS.wav OUT_DIR
set -euo pipefail
in="$1"; out="$2"
mkdir -p "$out"
ffmpeg -loglevel error -y -i "$in" -ac 2 -ar 44100 "$out/vocals_stereo.wav"
audio-separator "$out/vocals_stereo.wav" \
  -m mel_band_roformer_karaoke_aufr33_viperx_sdr_10.1956.ckpt \
  --output_format WAV --output_dir "$out"
# -> *_(Vocals)_*.wav = lead vocal, *_(Instrumental)_*.wav = backing vocals
