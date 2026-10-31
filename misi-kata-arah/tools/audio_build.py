#!/usr/bin/env python3
"""Bina semua audio video Misi Angkasa: Ekspedisi Kata Arah.

Usage (dari misi-kata-arah/):
    pip install edge-tts numpy
    python3 tools/audio_build.py            # jana suara yang belum ada, muzik, SFX, campuran
    python3 tools/audio_build.py --regen    # jana semula semua suara TTS

Hasil:
  audio/vo/<id>.wav       satu fail bagi setiap baris (boleh diganti dengan rakaman sendiri)
  audio/vo/chant_*.wav    perkataan chant
  audio/music/bgm.wav     muzik latar ciptaan kod (deterministik)
  audio/sfx/*.wav         kesan bunyi ciptaan kod (deterministik)
  audio/cues.json         masa mula setiap baris + masa setiap perkataan (untuk visual & kapsyen)
  audio/campuran.wav/.mp3 campuran akhir, -16 LUFS
Suara ms-MY Microsoft (edge-tts) memerlukan rangkaian ke speech.platform.bing.com.
Semua fail selain suara dijana tanpa rangkaian dan sama setiap kali.
"""
import asyncio
import json
import os
import subprocess
import sys
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from skrip import CHANT, LINES  # noqa: E402

SR = 48000
BPM = 96
BEAT = 60.0 / BPM
VOICE = "ms-MY-OsmanNeural"
# penutur -> (kadar edge-tts, pic rubberband, tempo)
SPK = {
    "N": ("-10%", 1.00, 1.00),   # pencerita: Osman asli
    "W": ("-5%", 1.20, 1.00),    # Wafiy: Osman, pic +3 semiton (budak lelaki)
    "G": ("-5%", 1.45, 1.06),    # Gogo: Osman, pic tinggi, sedikit laju (comel)
}
POST = 0.35  # jeda selepas setiap baris
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = lambda *p: os.path.join(ROOT, "audio", *p)  # noqa: E731


# ---------------------------------------------------------------- util
def write_wav(path, x):
    x = np.clip(x, -1, 1)
    data = (x * 32767).astype("<i2")
    ch = 1 if data.ndim == 1 else data.shape[1]
    with wave.open(path, "wb") as w:
        w.setnchannels(ch)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())


def read_wav(path):
    with wave.open(path, "rb") as w:
        sr, ch, n = w.getframerate(), w.getnchannels(), w.getnframes()
        x = np.frombuffer(w.readframes(n), dtype="<i2").astype(np.float32) / 32768
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)
    if sr != SR:
        raise SystemExit(f"{path}: kadar sampel {sr}, perlu {SR}")
    return x


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


# ---------------------------------------------------------------- TTS
async def tts(text, rate, mp3, proxy):
    import edge_tts
    words = []
    com = edge_tts.Communicate(text, VOICE, rate=rate, proxy=proxy, boundary="WordBoundary")
    with open(mp3, "wb") as f:
        async for c in com.stream():
            if c["type"] == "audio":
                f.write(c["data"])
            elif c["type"] == "WordBoundary":
                words.append({"w": c["text"], "t": round(c["offset"] / 1e7, 3), "d": round(c["duration"] / 1e7, 3)})
    return words


def make_voice(vid, spk, text, regen, proxy, timing):
    wav = A("vo", f"{vid}.wav")
    if os.path.exists(wav) and not regen and vid in timing:
        return
    rate, pitch, tempo = SPK[spk]
    mp3 = A("vo", "_tmp.mp3")
    words = asyncio.run(tts(text, rate, mp3, proxy))
    af = f"rubberband=pitch={pitch}:tempo={tempo}," if (pitch != 1 or tempo != 1) else ""
    # buang senyap di hujung sahaja (jeda dalam ayat dikekalkan), kemudian 48 kHz mono
    ffmpeg("-i", mp3, "-af", af + "areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.08,areverse,aresample=48000", "-ac", "1", wav)
    os.remove(mp3)
    for w in words:
        w["t"] = round(w["t"] / tempo, 3)
        w["d"] = round(w["d"] / tempo, 3)
    timing[vid] = {"spk": spk, "text": text, "words": words}


# ---------------------------------------------------------------- SFX (sintesis)
def env(n, a, r):
    e = np.ones(n)
    a, r = int(a * SR), int(r * SR)
    if a: e[:a] = np.linspace(0, 1, a)
    if r: e[-r:] *= np.linspace(1, 0, r) ** 2
    return e


def onepole(x, coef):
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc += coef[i] * (x[i] - acc)
        y[i] = acc
    return y


def sfx_whoosh(seed, dur):
    n = int(SR * dur)
    rng = np.random.default_rng(seed)
    x = rng.uniform(-1, 1, n)
    t = np.linspace(0, 1, n)
    cut = 0.02 + 0.25 * np.sin(np.pi * t) ** 2
    lo = onepole(x, cut)
    hp = lo - onepole(lo, np.full(n, 0.01))
    e = np.sin(np.pi * t) ** 1.6
    return hp * e * 2.2


def sfx_pop(f0, f1):
    n = int(SR * 0.16)
    t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 40)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 28) * 0.8


def sfx_klik():
    n = int(SR * 0.09)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * 1700 * t) * np.exp(-t * 90)
    thump = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 45)
    return (body * 0.5 + thump * 0.6)


def sfx_laser():
    n = int(SR * 0.45)
    t = np.arange(n) / SR
    f = 2200 * np.exp(-t * 6) + 240 + 30 * np.sin(2 * np.pi * 28 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    sq = np.tanh(3 * np.sin(ph))
    return sq * env(n, 0.005, 0.25) * 0.35


def sfx_radio():
    out = np.zeros(int(SR * 0.7))
    for k, st in enumerate([0.0, 0.32]):
        n = int(SR * 0.16)
        t = np.arange(n) / SR
        b = np.tanh(2 * np.sin(2 * np.pi * (1320 if k == 0 else 1180) * t)) * env(n, 0.005, 0.04) * 0.35
        i = int(st * SR)
        out[i:i + n] += b
    return out


def bell(freq, dur, amp=1.0):
    n = int(SR * dur)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * freq * 2.76 * t) * np.exp(-t * 6)
    return s * np.exp(-t * 4.5) * amp


def sfx_fanfare():
    out = np.zeros(int(SR * 2.2))
    for k, m in enumerate([72, 76, 79, 84, 88]):
        b = bell(hz(m), 1.4, 0.3)
        i = int(k * 0.11 * SR)
        out[i:i + len(b)] += b
    rng = np.random.default_rng(7)
    sp = rng.uniform(-1, 1, len(out))
    sp = sp - onepole(sp, np.full(len(out), 0.3))
    out += sp * env(len(out), 0.05, 1.6) * 0.06
    return out


def sfx_rumble():
    n = int(SR * 2.6)
    rng = np.random.default_rng(3)
    x = rng.uniform(-1, 1, n)
    lo = onepole(x, np.full(n, 0.012))
    lo = onepole(lo, np.full(n, 0.03))
    return lo * env(n, 0.6, 1.2) * 9


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def build_sfx():
    s = {
        "whoosh1": sfx_whoosh(11, 0.9), "whoosh2": sfx_whoosh(12, 1.1), "whoosh3": sfx_whoosh(13, 0.8),
        "pop1": sfx_pop(900, 420), "pop2": sfx_pop(760, 360), "klik": sfx_klik(),
        "laser": sfx_laser(), "radio": sfx_radio(), "fanfare": sfx_fanfare(), "rumble": sfx_rumble(),
    }
    for k, v in s.items():
        v = v / max(1e-6, np.max(np.abs(v))) * 0.9
        s[k] = v
        write_wav(A("sfx", f"{k}.wav"), v)
    return s


# ---------------------------------------------------------------- MUZIK (ciptaan kod)
CHORDS = [  # I - vi - IV - V (C major), lembut dan ceria
    (48, [64, 67, 71, 74]),   # Cmaj9
    (45, [64, 67, 69, 72]),   # Am7
    (41, [64, 65, 69, 72]),   # Fmaj7
    (43, [62, 67, 71, 74]),   # G6/9
]
ARP = [0, 1, 2, 3, 2, 1, 2, 3]  # indeks nada kord, lapan not 1/8


def pad(freqs, dur):
    n = int(SR * dur)
    t = np.arange(n) / SR
    s = np.zeros(n)
    for f in freqs:
        for det in (-0.004, 0.004):
            s += np.sin(2 * np.pi * f * (1 + det) * t)
    s /= (2 * len(freqs))
    return s * env(n, 0.8, 0.9)


def pluck_note(freq, dur):
    n = int(SR * dur)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * freq * t) + 0.25 * np.sin(4 * np.pi * freq * t) + 0.1 * np.sin(6 * np.pi * freq * t)
    return s * np.exp(-t * 5.5) * env(n, 0.004, 0.05)


def build_music(length):
    n = int(SR * length)
    L = np.zeros(n)
    R = np.zeros(n)
    bar = 4 * BEAT
    rng = np.random.default_rng(42)
    nbars = int(length / bar) + 1
    for b in range(nbars):
        t0 = b * bar
        root, tones = CHORDS[b % 4]
        i0 = int(t0 * SR)
        p = pad([hz(m) for m in tones], bar + 0.6) * 0.16
        seg = p[: max(0, min(len(p), n - i0))]
        L[i0:i0 + len(seg)] += seg
        R[i0:i0 + len(seg)] += seg
        if b < 2:
            continue  # intro: pad sahaja
        # bass lembut
        bs = pluck_note(hz(root), bar * 0.9) * 0.22
        seg = bs[: max(0, min(len(bs), n - i0))]
        L[i0:i0 + len(seg)] += seg
        R[i0:i0 + len(seg)] += seg
        # arpeggio "bintang" berselang kiri-kanan
        for k, idx in enumerate(ARP):
            ti = t0 + k * BEAT / 2
            j = int(ti * SR)
            note = pluck_note(hz(tones[idx] + 12), BEAT * 1.2) * 0.12
            seg = note[: max(0, min(len(note), n - j))]
            pan = 0.35 if k % 2 else -0.35
            L[j:j + len(seg)] += seg * (1 - pan)
            R[j:j + len(seg)] += seg * (1 + pan)
        # pengocak lembut pada off-beat
        for k in range(4):
            j = int((t0 + k * BEAT + BEAT / 2) * SR)
            m = int(SR * 0.05)
            sh = rng.uniform(-1, 1, m) * np.exp(-np.arange(m) / SR * 80) * 0.03
            sh = sh - np.concatenate([[0], sh[:-1]])
            seg = sh[: max(0, min(m, n - j))]
            L[j:j + len(seg)] += seg
            R[j:j + len(seg)] += seg
    fade = int(SR * 3)
    L[-fade:] *= np.linspace(1, 0, fade)
    R[-fade:] *= np.linspace(1, 0, fade)
    m = np.stack([L, R], axis=1)
    m /= np.max(np.abs(m)) / 0.8
    return m


# ---------------------------------------------------------------- SUSUN
def main():
    regen = "--regen" in sys.argv
    for d in ("vo", "music", "sfx"):
        os.makedirs(A(d), exist_ok=True)
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    tpath = A("vo", "timing.json")
    timing = json.load(open(tpath)) if os.path.exists(tpath) else {}

    for _, rows in LINES:
        for vid, spk, text, _pre, _sfx in rows:
            make_voice(vid, spk, text, regen, proxy, timing)
    chant_words = [w for w in CHANT if w]
    for w in chant_words:
        for spk in ("N", "W"):
            vid = f"chant_{spk}_{w.lower()}"
            old = SPK[spk]
            SPK[spk] = ("+25%", old[1], old[2])  # chant: lebih laju supaya muat satu rentak
            make_voice(vid, spk, w + "!", regen, proxy, timing)
            SPK[spk] = old
    json.dump(timing, open(tpath, "w"), ensure_ascii=False, indent=1)

    # ---- garis masa
    t = 0.0
    cues = {"bpm": BPM, "lines": [], "sections": [], "chant": []}
    placed_vo, placed_sfx = [], []
    for sec, rows in LINES:
        sec_start = t
        for vid, spk, text, pre, sfx in rows:
            x = read_wav(A("vo", f"{vid}.wav"))
            t += pre
            start = round(t, 3)
            dur = len(x) / SR
            words = [{"w": w["w"], "t": round(start + w["t"], 3), "d": w["d"]} for w in timing.get(vid, {}).get("words", [])]
            cues["lines"].append({"id": vid, "section": sec, "spk": spk, "text": text, "start": start, "dur": round(dur, 3), "words": words, "sfx": [[s, round(start + o, 3)] for s, o in sfx]})
            placed_vo.append((start, x))
            for s, o in sfx:
                placed_sfx.append((s, start + o))
            t = start + dur + POST
        if sec == "rumusan":
            # chant pada grid rentak: mulakan pada bar seterusnya
            bar = 4 * BEAT
            t = (np.ceil((t + 0.4) / bar)) * bar
            for k, w in enumerate(CHANT):
                bt = round(t + k * BEAT, 3)
                if w:
                    xs = [read_wav(A("vo", f"chant_{s}_{w.lower()}.wav")) for s in ("N", "W")]
                    mix = np.zeros(max(len(v) for v in xs))
                    for v in xs:
                        mix[: len(v)] += v * 0.62
                    placed_vo.append((bt, mix))
                    cues["chant"].append({"w": w, "t": bt})
                    placed_sfx.append(("pop1" if k % 2 == 0 else "pop2", bt))
            t = t + len(CHANT) * BEAT + 0.4
        cues["sections"].append({"id": sec, "start": round(sec_start, 3), "end": round(t, 3)})
    total = t + 2.5
    cues["total"] = round(total, 3)

    # ---- muzik & sfx
    sfx = build_sfx()
    music = build_music(total)
    write_wav(A("music", "bgm.wav"), music)

    n = int(total * SR)
    vo = np.zeros(n)
    for st, x in placed_vo:
        i = int(st * SR)
        seg = x[: max(0, min(len(x), n - i))]
        vo[i:i + len(seg)] += seg
    fx = np.zeros(n)
    for name, st in placed_sfx:
        i = max(0, int(st * SR))
        x = sfx[name] * (0.32 if name.startswith("pop") or name == "klik" else 0.38)
        seg = x[: max(0, min(len(x), n - i))]
        fx[i:i + len(seg)] += seg

    # ducking muzik apabila ada suara
    win = int(SR * 0.05)
    act = np.convolve(np.abs(vo), np.ones(win) / win, mode="same") > 0.01
    g = np.where(act, 0.10, 0.24).astype(np.float64)
    coef = 1 / (SR * 0.25)
    gs = np.empty_like(g)
    acc = g[0]
    step = 480  # kemas kini setiap 10 ms untuk kelajuan
    for i in range(0, n, step):
        acc += (g[i] - acc) * min(1.0, coef * step * 4)
        gs[i:i + step] = acc
    mus = music[:n] * gs[:, None]
    mix = mus + (vo * 0.95 + fx)[:, None]
    write_wav(A("campuran_raw.wav"), mix / max(1.0, np.max(np.abs(mix))))
    ffmpeg("-i", A("campuran_raw.wav"), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", A("campuran.wav"))
    ffmpeg("-i", A("campuran.wav"), "-b:a", "192k", A("campuran.mp3"))
    os.remove(A("campuran_raw.wav"))
    json.dump(cues, open(A("cues.json"), "w"), ensure_ascii=False, indent=1)
    print(f"Jumlah tempoh: {total:.1f} s ({int(total // 60)}:{int(total % 60):02d})")
    for s in cues["sections"]:
        print(f"  {s['id']:10s} {s['start']:7.2f} – {s['end']:7.2f}")


if __name__ == "__main__":
    main()
