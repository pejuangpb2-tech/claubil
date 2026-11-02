"""Bina suara naratif + runut latar untuk video Kak Ros, dan selaraskan tempoh babak.

    python3 tools/bina.py                              # Piper, suara Indonesia asli (lalai)
    python3 tools/bina.py --engine kokoro --voice if_sara --speed 1.05

1. Jana setiap baris dalam tools/naratif.json.
   - piper (lalai): suara wanita Piper id_ID-news_tts. Sebutan dari espeak-ng 'id'
     (ikut ejaan, seperti sebutan baku), dibetulkan oleh tools/sebutan.json
     untuk e pepet / e taling.
   - kokoro: suara Kokoro (bukan suara Melayu asli, jadi berloghat).
2. Panjangkan babak yang lebih pendek daripada suaranya, tulis TIMING dan tag
   <audio> ke index.html.
3. Jalankan tools/audio.py: muzik + kesan bunyi + suasana (ditekan bawah suara)
   -> assets/audio/latar.mp3, dan klip suara -> assets/audio/narasi/*.mp3.

Model dimuat turun sekali ke ~/.cache/piper atau ~/.cache/kokoro.
"""
import argparse, json, os, re, subprocess, sys, tarfile, urllib.request
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
ap.add_argument("--engine", choices=["piper", "kokoro"], default="piper")
ap.add_argument("--voice", default="if_sara", help="suara Kokoro (untuk --engine kokoro)")
ap.add_argument("--speed", type=float, default=None, help="kelajuan (lalai: piper 1.2, kokoro 1.05)")
args = ap.parse_args()
speed = args.speed or (1.2 if args.engine == "piper" else 1.05)


def espeak():
    import espeakng_loader
    from phonemizer.backend.espeak.wrapper import EspeakWrapper
    EspeakWrapper.set_library(espeakng_loader.get_library_path())
    EspeakWrapper.set_data_path(espeakng_loader.get_data_path())
    from phonemizer.backend import EspeakBackend
    return EspeakBackend


# ---------- 1. voice ----------
if args.engine == "piper":
    import onnxruntime as ort
    pdir = Path(os.environ.get("PIPER_DIR", Path.home() / ".cache" / "piper")); pdir.mkdir(parents=True, exist_ok=True)
    NAME = "id_ID-news_tts-medium"
    if not (pdir / f"{NAME}.onnx").exists():
        url = f"https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-{NAME}.tar.bz2"
        print("muat turun", url); tb = pdir / "model.tar.bz2"; urllib.request.urlretrieve(url, tb)
        with tarfile.open(tb) as t:
            for m in t.getmembers():
                if m.name.endswith((".onnx", ".onnx.json")):
                    m.name = Path(m.name).name; t.extract(m, pdir, filter="data")
        tb.unlink()
    pcfg = json.load(open(pdir / f"{NAME}.onnx.json")); PM = pcfg["phoneme_id_map"]; PSR = pcfg["audio"]["sample_rate"]
    sess = ort.InferenceSession(str(pdir / f"{NAME}.onnx"))
    ID = espeak()("id", with_stress=True)
    LEX = {k: v for k, v in json.load(open(TOOLS / "sebutan.json")).items() if not k.startswith("_")}

    def phonemes(text):
        out = []
        for word, punct in re.findall(r"([A-Za-z-]+)([.,?!:;]*)", text):
            w = word.lower()
            p = LEX.get(w) or ID.phonemize([w])[0].strip()
            if w.endswith("k") and p.endswith("k"):
                p = p[:-1] + "ʔ"      # sebutan baku: k di hujung kata = hentian glotis
            out.append(p + punct)
        return " ".join(out)

    def synth(text):
        ph = phonemes(text); bad = {c for c in ph if c not in PM}
        assert not bad, (text, bad)
        ids = PM["^"] + PM["_"]
        for c in ph: ids += PM[c] + PM["_"]
        ids += PM["$"]
        a = sess.run(None, {"input": np.array([ids], dtype=np.int64), "input_lengths": np.array([len(ids)], dtype=np.int64),
                            "scales": np.array([0.667, 1.0 / speed, 0.8], dtype=np.float32)})[0].squeeze()
        return a, PSR, ph
else:
    kdir = Path(os.environ.get("KOKORO_DIR", Path.home() / ".cache" / "kokoro")); kdir.mkdir(parents=True, exist_ok=True)
    REL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
    for f in ("kokoro-v1.0.onnx", "voices-v1.0.bin"):
        if not (kdir / f).exists():
            print("muat turun", f); urllib.request.urlretrieve(REL + f, kdir / f)
    from kokoro_onnx import Kokoro
    kk = Kokoro(str(kdir / "kokoro-v1.0.onnx"), str(kdir / "voices-v1.0.bin"))

    def synth(text):
        a, sr = kk.create(text, voice=args.voice, lang="ms", speed=speed)
        return a, sr, ""


def trim(a, sr, thr=0.01):
    idx = np.where(np.abs(a) > thr * np.abs(a).max())[0]
    pad = int(0.04 * sr)
    return a[max(0, idx[0] - pad): idx[-1] + pad] if len(idx) else a


lines = json.load(open(TOOLS / "naratif.json"))["lines"]
raw = ROOT / ".media" / "narasi"; raw.mkdir(parents=True, exist_ok=True)
out = ROOT / "assets" / "audio" / "narasi"; out.mkdir(parents=True, exist_ok=True)
for f in out.glob("*.mp3"): f.unlink()

for n, ln in enumerate(lines, 1):
    a, sr, ph = synth(ln["text"])
    a = trim(np.asarray(a, dtype=np.float64), sr)
    a = resample_poly(a, SR, sr)
    a = a / (np.max(np.abs(a)) + 1e-9) * 0.7
    f = 0.012; k = int(f * SR); a[:k] *= np.linspace(0, 1, k); a[-k:] *= np.linspace(1, 0, k)
    ln["id"] = f"n{n:02d}"; ln["len"] = len(a) / SR
    ln["raw"] = str(raw / f"{ln['id']}.wav"); ln["out"] = str(raw / f"{ln['id']}.mix.wav")
    sf.write(ln["raw"], a, SR, subtype="PCM_16")
    print(f"{ln['id']} babak {ln['scene']:2d}  {ln['len']:.2f}s  {ln['text']}")
    if ph: print("     ", ph)

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
