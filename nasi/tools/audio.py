import json, sys, numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

SR = 44100
ev = json.load(open(sys.argv[1]))
TOTAL = ev['total']; starts = ev['starts']
N = int(SR * (TOTAL + 0.5))
rng = np.random.default_rng(7)

def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'bandpass', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'lowpass', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'highpass', fs=SR, output='sos'), x)
def tt(d): return np.arange(int(SR * d)) / SR
def add(buf, t0, sig, g=1.0):
    i = int(t0 * SR)
    if i >= len(buf): return
    j = min(len(buf), i + len(sig)); buf[i:j] += sig[:j - i] * g
mf = lambda m: 440 * 2 ** ((m - 69) / 12)

# ---------------- MUSIC ----------------
music = np.zeros(N); drums = np.zeros(N); bells = np.zeros(N)
BPM = 84; beat = 60 / BPM; bar = beat * 4
chords = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]
roots = [41, 40, 38, 36]
penta = [72, 74, 76, 79, 81, 84]
def ep(f, d, v):
    t = tt(d); env = np.exp(-t * 1.6) * np.minimum(1, t / 0.008)
    s = sum(a * np.sin(2 * np.pi * f * k * t + k) for k, a in [(1, 1), (2, .38), (3, .12), (4, .06)])
    s += .25 * np.sin(2 * np.pi * f * 7 * t) * np.exp(-t * 18)
    rel = np.ones_like(t); r = int(.12 * SR); rel[-r:] = np.linspace(1, 0, r)
    return s * env * rel * (1 + .1 * np.sin(2 * np.pi * 4.2 * t)) * v
def bell(f, v):
    t = tt(2.2); return v * (np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * f * 3.01 * t) * np.exp(-t * 4)) * np.exp(-t * 2.2) * np.minimum(1, t / .004)
def bass(f, d, v):
    t = tt(d); env = np.minimum(1, t / .01) * np.exp(-t * 1.2); rel = np.ones_like(t); r = int(.08 * SR); rel[-r:] = np.linspace(1, 0, r)
    return v * (np.sin(2 * np.pi * f * t) + .25 * np.sin(4 * np.pi * f * t)) * env * rel
kick_t = tt(.35); KICK = np.sin(2 * np.pi * (45 * kick_t + 60 / 18 * (1 - np.exp(-kick_t * 18)) * 1.0) * 1) * 0
f_inst = 50 + 90 * np.exp(-kick_t * 25); KICK = np.sin(2 * np.pi * np.cumsum(f_inst) / SR) * np.exp(-kick_t * 9)
SN = bp(rng.standard_normal(int(.22 * SR)), 900, 5000) * np.exp(-tt(.22) * 22)
HAT = hp(rng.standard_normal(int(.05 * SR)), 7000) * np.exp(-tt(.05) * 90)

end_soft = starts[13]
nbars = int(TOTAL / bar) + 2
mr = np.random.default_rng(3)
for b in range(nbars):
    t0 = b * bar; ci = b % 4; soft = t0 >= end_soft - .01
    if t0 > TOTAL + .2: break
    vol = .55 if soft else .8
    for m in chords[ci]: add(music, t0, ep(mf(m), beat * 2.4, .16 * vol))
    if not soft:
        for m in chords[ci][1:]: add(music, t0 + beat * 2.5, ep(mf(m), beat * 1.4, .10 * vol))
        add(music, t0, bass(mf(roots[ci]), beat * 1.8, .32)); add(music, t0 + beat * 2, bass(mf(roots[ci] + 7 if ci % 2 else roots[ci]), beat * 1.6, .26))
    # drums from scene 1 until soft ending
    if starts[1] - .01 <= t0 and not soft:
        add(drums, t0, KICK, .55); add(drums, t0 + beat * 2.5, KICK, .38)
        add(drums, t0 + beat, SN, .16); add(drums, t0 + beat * 3, SN, .16)
        for k in range(8): add(drums, t0 + k * beat / 2 + (.07 if k % 2 else 0), HAT, .07 if k % 2 else .1)
    # bell motif every other bar, and every bar in soft ending
    if b % 2 == 1 or soft or b == 0:
        for k in range(3 if soft else 2):
            add(bells, t0 + beat * (k * 1.5 + .5), bell(mf(penta[mr.integers(0, len(penta))]), .07))
mus = lp(music + bells, 5200) + lp(drums, 9000)
# vinyl crackle + hiss
crk = np.zeros(N); idx = rng.integers(0, N, int(TOTAL * 6)); crk[idx] = rng.uniform(-.25, .25, len(idx)); crk = hp(crk, 1500)
mus += crk * .25 + lp(rng.standard_normal(N), 3000) * .004
# fade in / out
fi = int(.4 * SR); mus[:fi] *= np.linspace(0, 1, fi)
fo_start = int((TOTAL - 1.2) * SR); mus[fo_start:] *= np.linspace(1, 0, N - fo_start) ** 1.5

# ---------------- SFX ----------------
sfx = np.zeros(N)
def whoosh():
    d = .55; t = tt(d); n = rng.standard_normal(len(t)); env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
    a = bp(n, 300, 1500); b2 = bp(n, 1500, 6000); k = t / d
    return (a * (1 - k) + b2 * k) * env * .9
def stamp():
    t = tt(.3); return np.sin(2 * np.pi * (70 + 60 * np.exp(-t * 30)) * t) * np.exp(-t * 16) * 1.0 + bp(rng.standard_normal(len(t)), 800, 6000) * np.exp(-t * 120) * .5
def pop():
    t = tt(.14); f = 520 + 900 * (t / .14); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 30) * .7
def marimba(m, v=1):
    t = tt(.5); f = mf(m); return v * (np.sin(2 * np.pi * f * t) + .25 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 30)) * np.exp(-t * 9) * np.minimum(1, t / .002)
def ring():
    out = np.zeros(int(.6 * SR))
    for k, m in enumerate([88, 92, 95, 92]): add(out, k * .09, marimba(m, .45))
    return out
def connect():
    out = np.zeros(int(.5 * SR)); add(out, 0, marimba(84, .35)); add(out, .08, marimba(91, .35)); return out
def horn(dist=False):
    t = tt(1.6); env = np.minimum(1, t / .15) * np.minimum(1, (1.6 - t) / .35)
    s = sum(np.sin(2 * np.pi * f * k * t) / k for f in (98, 123.5) for k in range(1, 8))
    s = lp(s, 420 if dist else 900) * env * (.10 if dist else .17)
    return s
def click():
    t = tt(.06); return hp(rng.standard_normal(len(t)), 2500) * np.exp(-t * 80) * .6 + np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 60) * .3
def ding():
    t = tt(2.5); return (np.sin(2 * np.pi * 1568 * t) + .5 * np.sin(2 * np.pi * 2352 * t) + .2 * np.sin(2 * np.pi * 3136 * t)) * np.exp(-t * 1.8) * .32
FX = {'whoosh': whoosh, 'stamp': stamp, 'pop': pop, 'ring': ring, 'connect': connect, 'horn': lambda: horn(False), 'horn2': lambda: horn(True), 'click': click, 'ding': ding}
for t0, name in ev['ev']: add(sfx, t0, FX[name]())

# ---------------- AMBIENCE ----------------
amb = np.zeros(N)
def seg(i): return starts[i], (starts[i + 1] if i + 1 < len(starts) else TOTAL)
def bed(i, sig_fn, g):
    a, b = seg(i); n = int((b - a) * SR); s = sig_fn(n); f = int(.25 * SR); env = np.ones(n); env[:f] = np.linspace(0, 1, f); env[-f:] = np.linspace(1, 0, f); add(amb, a, s * env, g)
street = lambda n: lp(rng.standard_normal(n), 600) * (1 + .3 * np.sin(np.arange(n) / SR * 2 * np.pi * .3))
def birds(n):
    out = np.zeros(n)
    for _ in range(int(n / SR * 1.6)):
        t0 = rng.uniform(0, n / SR - .3); d = rng.uniform(.06, .14); t = tt(d); f0 = rng.uniform(2800, 4200)
        f = f0 + 900 * np.sin(2 * np.pi * rng.uniform(12, 25) * t); c = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d)
        for r in range(rng.integers(1, 4)): add(out, t0 + r * (d + .04), c, rng.uniform(.2, .45))
    return out
def crickets(n):
    t = np.arange(n) / SR; car = np.sin(2 * np.pi * 4600 * t); am = (np.sin(2 * np.pi * 28 * t) > .3) * (np.sin(2 * np.pi * .9 * t) > -.2)
    return lp(car * am, 7000) * .35
waves = lambda n: lp(rng.standard_normal(n), 500) * (0.6 + .4 * np.sin(np.arange(n) / SR * 2 * np.pi * .18)) * 1.4
room = lambda n: lp(rng.standard_normal(n), 250) * .8
for i in (0, 1, 2, 3): bed(i, street, .05)
for i in (2, 10, 12): bed(i, birds, .10)
for i in (4, 13): bed(i, crickets, .03)
for i in (8, 9): bed(i, waves, .06)
bed(7, room, .05)

# ---------------- VOICEOVER (placed as separate <audio> clips in index.html) ----------------
# argv: events.json  latar_out.wav  [vo_plan.json]
# vo_plan.json = {"clips": [{"t": seconds, "src": raw wav, "out": wav to write}]}
vo = np.zeros(N); clips = []
if len(sys.argv) > 3:
    for c in json.load(open(sys.argv[3]))['clips']:
        sr_, w = wavfile.read(c['src'])
        w = w.astype(np.float64) / 32768.0
        if w.ndim > 1: w = w.mean(1)
        assert sr_ == SR, (c['src'], sr_)
        add(vo, c['t'], w); clips.append((c, w))
    env = np.abs(vo); win = int(.25 * SR); env = np.convolve(env, np.ones(win) / win, 'same'); env = np.clip(env / (env.max() + 1e-9) * 6, 0, 1)
    duck = 1 - .6 * env
    mus = mus * duck; amb = amb * (1 - .4 * env)
bed = mus * .55 + sfx * .45 + amb
mix = bed + vo * .9
g = .89 / np.max(np.abs(mix))          # one gain for both stems keeps the original balance
bed = np.tanh(bed * g * 1.1) / 1.1
st = np.stack([bed, np.roll(bed, int(.0004 * SR)) * .98], 1)
wavfile.write(sys.argv[2], SR, (st * 32767).astype(np.int16))
for c, w in clips:
    wavfile.write(c['out'], SR, (np.clip(w * .9 * g, -1, 1) * 32767).astype(np.int16))
print('ok', round(TOTAL, 3), 'gain', round(g, 3), 'rms', round(float(np.sqrt(np.mean((bed[:, None] if bed.ndim == 1 else bed) ** 2))), 4))
