"""Bina suara naratif + runut latar untuk video Kak Ros, dan selaraskan tempoh babak.

    python3 tools/bina.py [--voice ef_dora] [--speed 1.05]

1. Jana setiap baris dalam tools/naratif.json dengan Kokoro (sebutan Bahasa Melayu
   dari espeak-ng 'ms').
2. Panjangkan babak yang lebih pendek daripada suaranya, tulis TIMING dan tag
   <audio> ke index.html.
3. Jalankan tools/audio.py: muzik + kesan bunyi + suasana (ditekan bawah suara)
   -> assets/audio/latar.wav, dan klip suara -> assets/audio/narasi/*.wav.

Model Kokoro dimuat turun sekali ke ~/.cache/kokoro (KOKORO_DIR untuk tukar).
"""
import argparse, json, os, re, subprocess, sys, urllib.request
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
INDEX = ROOT / "index.html"
SR = 44100
TAIL = 0.7          # saat senyap selepas suara sebelum babak bertukar
SPLIT_GAP = 0.45    # jeda antara dua baris dalam babak yang sama

ap = argparse.ArgumentParser()
ap.add_argument("--voice", default="ef_dora")
ap.add_argument("--speed", type=float, default=1.05)
args = ap.parse_args()

# ---------- 1. voice ----------
kdir = Path(os.environ.get("KOKORO_DIR", Path.home() / ".cache" / "kokoro"))
kdir.mkdir(parents=True, exist_ok=True)
REL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
for f in ("kokoro-v1.0.onnx", "voices-v1.0.bin"):
    if not (kdir / f).exists():
        print("muat turun", f); urllib.request.urlretrieve(REL + f, kdir / f)

from kokoro_onnx import Kokoro  # noqa: E402

kk = Kokoro(str(kdir / "kokoro-v1.0.onnx"), str(kdir / "voices-v1.0.bin"))
lines = json.load(open(TOOLS / "naratif.json"))["lines"]
raw = ROOT / ".media" / "narasi"; raw.mkdir(parents=True, exist_ok=True)
out = ROOT / "assets" / "audio" / "narasi"; out.mkdir(parents=True, exist_ok=True)
for f in out.glob("*.mp3"): f.unlink()

for n, ln in enumerate(lines, 1):
    a, sr = kk.create(ln["text"], voice=args.voice, lang="ms", speed=args.speed)
    a = resample_poly(a.astype(np.float64), SR, sr)
    a = a / (np.max(np.abs(a)) + 1e-9) * 0.7
    f = 0.012; k = int(f * SR); a[:k] *= np.linspace(0, 1, k); a[-k:] *= np.linspace(1, 0, k)
    ln["id"] = f"n{n:02d}"; ln["len"] = len(a) / SR
    ln["raw"] = str(raw / f"{ln['id']}.wav"); ln["out"] = str(raw / f"{ln['id']}.mix.wav")
    sf.write(ln["raw"], a, SR, subtype="PCM_16")
    print(f"{ln['id']} babak {ln['scene']:2d}  {ln['len']:.2f}s  {ln['text']}")

# ---------- 2. timing ----------
def page_eval(expr):
    js = f"""
const {{chromium}}=require('playwright');
(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{INDEX}');await p.waitForFunction(()=>window.events);
console.log(JSON.stringify(await p.evaluate(()=>{expr})));await b.close()}})();"""
    return json.loads(subprocess.check_output(["node", "-e", js], cwd="/tmp").decode().strip().splitlines()[-1])

base = page_eval("window.__baseDur")
dur = list(base); split = {}; placed = []
for i in range(len(base)):
    t_end = 0.0
    for ln in [l for l in lines if l["scene"] == i]:
        if ln["at"] == "split":
            at = round(t_end + SPLIT_GAP, 2); split[str(i)] = at
        else:
            at = ln["at"]
        placed.append((i, at, ln)); t_end = at + ln["len"]
    dur[i] = round(max(base[i], t_end + TAIL), 2)

html = INDEX.read_text()
html = re.sub(r"/\*TIMING\*/.*?/\*/TIMING\*/",
              "/*TIMING*/const TIMING=" + json.dumps({"dur": dur, "split": split}) + ";/*/TIMING*/", html, flags=re.S)
INDEX.write_text(html)
ev = page_eval("window.events")
starts, total = ev["starts"], round(ev["total"], 3)

tags, plan = [], []
for i, at, ln in placed:
    t = round(starts[i] + at, 3)
    plan.append({"t": t, "src": ln["raw"], "out": ln["out"]})
    tags.append(f'      <audio id="narasi-{ln["id"][1:]}" class="clip" src="assets/audio/narasi/{ln["id"]}.mp3" '
                f'data-start="{t}" data-duration="{ln["len"]:.3f}" data-track-index="2" data-volume="1"></audio>')
tags.insert(0, f'      <audio id="latar" class="clip" src="assets/audio/latar.mp3" data-start="0" '
               f'data-duration="{total}" data-track-index="1" data-volume="1"></audio>')
html = INDEX.read_text()
html = re.sub(r"<!--AUDIO-->.*?<!--/AUDIO-->", "<!--AUDIO-->\n" + "\n".join(tags) + "\n      <!--/AUDIO-->", html, flags=re.S)
html = re.sub(r'(id="root"[^>]*data-duration=")[^"]*"', rf'\g<1>{total}"', html)
INDEX.write_text(html)

# ---------- 3. bed + scaled voice clips ----------
evp = raw / "events.json"; json.dump(ev, open(evp, "w"))
planp = raw / "plan.json"; json.dump({"clips": plan}, open(planp, "w"))
latar = raw / "latar.wav"
subprocess.check_call([sys.executable, str(TOOLS / "audio.py"), str(evp), str(latar), str(planp)])
ff = ["ffmpeg", "-y", "-loglevel", "error"]
subprocess.check_call(ff + ["-i", str(latar), "-b:a", "192k", str(ROOT / "assets/audio/latar.mp3")])
for c in plan:
    subprocess.check_call(ff + ["-i", c["out"], "-ac", "1", "-b:a", "128k", str(out / (Path(c["src"]).stem + ".mp3"))])
print("jumlah", total, "s | babak", dur, "| split", split)
