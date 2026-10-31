#!/usr/bin/env python3
"""Synthesise the 60 s background music: a light plucked C-G-Am-F loop at 104 BPM.

Usage (from kata-ganti/):  python3 tools/music.py
Writes assets/music/bed.mp3. Deterministic: same file every run.
"""
import subprocess
import wave

import numpy as np

SR = 44100
BPM = 104
LENGTH = 61.0
BEAT = 60 / BPM

CHORDS = [  # (root midi, chord tones)
    (48, [60, 64, 67]),  # C
    (43, [59, 62, 67]),  # G
    (45, [60, 64, 69]),  # Am
    (41, [60, 65, 69]),  # F
]
MELODY = [76, 74, 72, 74, 76, 76, 76, None, 74, 74, 74, None, 76, 79, 79, None]


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def pluck(freq, dur, seed):
    """Karplus-Strong string, seeded so the output never changes."""
    n = int(SR * dur)
    period = max(2, int(SR / freq))
    rng = np.random.default_rng(seed)
    buf = rng.uniform(-1, 1, period)
    out = np.empty(n)
    for i in range(n):
        out[i] = buf[i % period]
        buf[i % period] = 0.5 * (buf[i % period] + buf[(i + 1) % period]) * 0.996
    return out


def bell(freq, dur):
    t = np.arange(int(SR * dur)) / SR
    env = np.exp(-t * 4.5)
    return env * (np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * freq * 3 * t))


def place(track, sig, at, gain):
    i = int(at * SR)
    if i >= len(track):
        return
    j = min(len(track), i + len(sig))
    track[i:j] += sig[: j - i] * gain


def main():
    track = np.zeros(int(SR * LENGTH))
    t, bar, seed = 0.0, 0, 1
    while t < LENGTH:
        root, tones = CHORDS[bar % 4]
        place(track, pluck(hz(root), BEAT * 4, seed), t, 0.35)
        seed += 1
        for k, step in enumerate([0, 1, 2, 1, 0, 1, 2, 1]):  # eighth-note arpeggio
            place(track, pluck(hz(tones[step]), BEAT * 1.5, seed), t + k * BEAT / 2, 0.22)
            seed += 1
        if bar % 8 >= 4:  # a quiet glockenspiel line every other phrase
            for k in range(4):
                note = MELODY[(bar % 4) * 4 + k]
                if note:
                    place(track, bell(hz(note), BEAT * 1.2), t + k * BEAT, 0.08)
        t += BEAT * 4
        bar += 1
    fade = int(SR * 2.5)
    track[-fade:] *= np.linspace(1, 0, fade)
    track[: int(SR * 0.5)] *= np.linspace(0, 1, int(SR * 0.5))
    track /= np.max(np.abs(track)) * 1.12
    pcm = (track * 32767).astype(np.int16)
    with wave.open("assets/music/bed.wav", "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "assets/music/bed.wav", "-b:a", "160k", "assets/music/bed.mp3"], check=True)
    subprocess.run(["rm", "assets/music/bed.wav"], check=True)
    print("assets/music/bed.mp3")


main()
