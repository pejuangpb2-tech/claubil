#!/usr/bin/env python3
"""Jana misi-kata-arah.srt dan bab-youtube.txt daripada audio/cues.json.

Usage (dari misi-kata-arah/):  python3 tools/deliverables.py
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from skrip import STESEN  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cues = json.load(open(os.path.join(ROOT, "audio", "cues.json")))


def ts(t):
    t = max(0.0, t)
    h, m = int(t // 3600), int(t % 3600 // 60)
    s = t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"


# ---- SRT: setiap baris narasi dipecah ikut ayat, maksimum ~12 patah perkataan, 2 baris
blocks = []
for l in cues["lines"]:
    tk = l["text"].split()
    ws = l["words"]
    cur = []
    for i, t in enumerate(tk):
        cur.append(i)
        end_sent = bool(re.search(r"[.!?…]$", t))
        if i == len(tk) - 1 or (end_sent and len(cur) >= 3) or len(cur) >= 10:
            a, b = cur[0], cur[-1]
            st = ws[a]["t"] - 0.05
            en = ws[b]["t"] + ws[b]["d"] + 0.3
            text = " ".join(tk[a:b + 1])
            if len(text) > 42:  # pecah kepada dua baris
                words = text.split()
                best = min(range(1, len(words)), key=lambda k: abs(len(" ".join(words[:k])) - len(" ".join(words[k:]))))
                text = " ".join(words[:best]) + "\n" + " ".join(words[best:])
            blocks.append([st, en, text])
            cur = []
for c in [cues["chant"]]:
    if c:
        blocks.append([c[0]["t"] - 0.05, c[5]["t"] + 0.6, ", ".join(x["w"] for x in c[:6]) + "!"])
        blocks.append([c[6]["t"] - 0.05, c[-1]["t"] + 0.6, ", ".join(x["w"] for x in c[6:]) + "!"])
blocks.sort(key=lambda b: b[0])
for i in range(len(blocks) - 1):
    blocks[i][1] = min(blocks[i][1], blocks[i + 1][0] - 0.02)
srt = "\n".join(f"{i + 1}\n{ts(a)} --> {ts(b)}\n{t}\n" for i, (a, b, t) in enumerate(blocks))
open(os.path.join(ROOT, "misi-kata-arah.srt"), "w").write(srt)

# ---- Bab YouTube
names = dict(STESEN)
names["pembukaan"] = "Berlepas!"
out = []
for s in cues["sections"]:
    t = int(s["start"])
    out.append(f"{t // 60}:{t % 60:02d} {names[s['id']]}")
out[0] = "0:00 " + out[0].split(" ", 1)[1]
open(os.path.join(ROOT, "bab-youtube.txt"), "w").write("\n".join(out) + "\n")
print(f"misi-kata-arah.srt: {len(blocks)} blok; bab-youtube.txt: {len(out)} bab")
