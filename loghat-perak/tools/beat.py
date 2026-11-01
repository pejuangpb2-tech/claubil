# Original, royalty-free background beat for "Orang Perak Je Faham".
# Playful 100 BPM groove: kick, clap, hats, bouncy bass and a marimba-like arpeggio over C-G-Am-F.
# Deterministic (seeded noise), no network, no samples.
#   python3 tools/beat.py assets/music/rentak.wav 58.3
import sys
import numpy as np
import wave

SR = 44100
BPM = 100.0
BEAT = 60.0 / BPM
BAR = BEAT * 4
rng = np.random.default_rng(7)

out_path = sys.argv[1] if len(sys.argv) > 1 else "rentak.wav"
length = float(sys.argv[2]) if len(sys.argv) > 2 else 58.3
N = int(SR * (length + 1.0))
L = np.zeros(N)
R = np.zeros(N)


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def place(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N:
        return
    sig = sig[: N - i] * gain
    L[i : i + len(sig)] += sig * np.cos((pan + 1) * np.pi / 4)
    R[i : i + len(sig)] += sig * np.sin((pan + 1) * np.pi / 4)


def env(n, attack, decay):
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    return a * np.exp(-t / decay)


def kick():
    n = int(0.42 * SR)
    t = np.arange(n) / SR
    f = 45 + 95 * np.exp(-t / 0.045)
    ph = 2 * np.pi * np.cumsum(f) / SR
    click = rng.standard_normal(n) * np.exp(-t / 0.004) * 0.25
    return np.tanh(1.6 * (np.sin(ph) * env(n, 0.001, 0.17) + click))


def clap():
    n = int(0.3 * SR)
    t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    noise = noise - np.concatenate([[0], noise[:-1]]) * 0.6  # brighten
    bursts = sum(np.exp(-np.clip(t - d, 0, None) / 0.012) * (t >= d) for d in (0.0, 0.011, 0.022))
    tail = np.exp(-np.clip(t - 0.03, 0, None) / 0.09) * (t >= 0.03)
    body = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.05) * 0.4
    return (noise * (0.5 * bursts + 0.6 * tail) + body) * 0.55


def hat(open_=False):
    n = int((0.16 if open_ else 0.045) * SR)
    noise = rng.standard_normal(n)
    hp = noise - np.concatenate([[0], noise[:-1]])
    hp = hp - np.concatenate([[0], hp[:-1]])
    return hp * env(n, 0.0005, 0.05 if open_ else 0.012) * 0.18


def bass(note, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = midi(note)
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) + 0.12 * np.sin(2 * np.pi * 3 * f * t)
    e = env(n, 0.004, dur * 0.9) * np.clip((dur - t) / 0.02, 0, 1)
    return np.tanh(1.4 * s * e) * 0.55


def marimba(note, dur=0.5):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = midi(note)
    s = (np.sin(2 * np.pi * f * t) * np.exp(-t / 0.28)
         + 0.45 * np.sin(2 * np.pi * 4.0 * f * t) * np.exp(-t / 0.05)
         + 0.2 * np.sin(2 * np.pi * 9.2 * f * t) * np.exp(-t / 0.015))
    return s * env(n, 0.002, 1.0) * 0.32


# C - G - Am - F (one chord per bar); roots for bass, chord tones for the arpeggio
CHORDS = [(36, [60, 64, 67, 72]), (43, [59, 62, 67, 71]), (45, [57, 60, 64, 69]), (41, [57, 60, 65, 69])]
ARP = [0, 2, 1, 3, 2, 1, 3, 2]          # eighth-note pattern over the chord tones
BASS = [(0, 0, 0.5), (1.5, 0, 0.25), (2, 12, 0.4), (3, 0, 0.25), (3.5, 7, 0.4)]  # (beat, interval, dur in beats)

bars = int(np.ceil(length / BAR)) + 1
kick_s, clap_s = kick(), clap()
for b in range(bars):
    t0 = b * BAR
    root, tones = CHORDS[b % 4]
    intro = b == 0                       # first bar: lighter, so the hook's boom owns the downbeat
    # drums
    for k in (0, 2, 2.5) if b % 2 else (0, 1.75, 2):
        place(kick_s, t0 + k * BEAT, 0.0 if (intro and k == 0) else 0.9)
    for c in (1, 3):
        place(clap_s, t0 + c * BEAT, 0.7, pan=0.05)
    for e in range(8):
        place(hat(open_=(e == 7 and b % 2 == 1)), t0 + e * BEAT / 2 + (0.012 if e % 2 else 0), 0.9 if e % 2 else 0.55, pan=0.3)
    # bass
    for beat, iv, d in BASS:
        place(bass(root + iv, d * BEAT), t0 + beat * BEAT, 0.8)
    # arpeggio (rests on the last eighth of every 4th bar for a breath)
    for e, idx in enumerate(ARP):
        if b % 4 == 3 and e == 7:
            continue
        place(marimba(tones[idx]), t0 + e * BEAT / 2, 0.7, pan=(-0.35 if e % 2 else 0.35))

# light sidechain pump from the kick grid, so the groove breathes
t = np.arange(N) / SR
phase = (t % BEAT) / BEAT
pump = 1 - 0.28 * np.exp(-phase / 0.18)
L *= pump
R *= pump

# master: trim, fades, soft clip, normalise to -1 dBFS
n_out = int(length * SR)
L, R = L[:n_out], R[:n_out]
fade_in = np.clip(np.arange(n_out) / (0.05 * SR), 0, 1)
fade_out = np.clip((n_out - np.arange(n_out)) / (0.8 * SR), 0, 1)
L *= fade_in * fade_out
R *= fade_in * fade_out
L, R = np.tanh(L * 1.2), np.tanh(R * 1.2)
peak = max(np.abs(L).max(), np.abs(R).max())
g = 10 ** (-1 / 20) / peak
pcm = (np.stack([L * g, R * g], axis=1) * 32767).astype("<i2")
with wave.open(out_path, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print(f"wrote {out_path}: {length:.2f}s, {BPM:.0f} BPM, {bars} bars")
