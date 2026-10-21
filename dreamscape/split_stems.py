#!/usr/bin/env python3
"""Split the 18-channel Csound render into stereo stem files.

    python3 split_stems.py dreamscape_multitrack.wav OUT_DIR
"""
import os
import sys

import soundfile as sf

STEMS = ["master", "pads", "bass", "star_keys", "theremin", "oscilloscope", "drums", "drone", "fx_returns"]

src, out_dir = sys.argv[1], sys.argv[2]
os.makedirs(out_dir, exist_ok=True)
x, sr = sf.read(src, dtype="float32")
for i, name in enumerate(STEMS):
    sf.write(os.path.join(out_dir, f"{i:02d}_{name}.wav"), x[:, 2 * i:2 * i + 2], sr, subtype="FLOAT")
    print("wrote", name)
