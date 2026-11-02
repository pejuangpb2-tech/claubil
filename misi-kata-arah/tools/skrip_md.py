#!/usr/bin/env python3
"""Tulis skrip.md (skrip akhir bermasa, untuk lampiran tugasan) daripada audio/cues.json."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from skrip import STESEN  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cues = json.load(open(os.path.join(ROOT, "audio", "cues.json")))
NAMA = {"N": "Pencerita", "W": "Wafiy", "G": "Gogo"}
title = dict(STESEN)


def mmss(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


out = ["# Skrip Video: Misi Angkasa, Ekspedisi Kata Arah", "",
       "Bahasa Melayu Tahun 3 · SP 5.1.4 (iii) kata arah · Video penerangan (tiada kuiz)", "",
       f"Tempoh: {mmss(cues['total'])}. Suara: Pencerita (ms-MY-OsmanNeural), Wafiy dan Gogo (suara Osman dengan pic dinaikkan).", ""]
for sec in cues["sections"]:
    out += [f"## {title[sec['id']]} ({mmss(sec['start'])}–{mmss(sec['end'])})", "", "| Masa | Penutur | Dialog / Narasi |", "|---|---|---|"]
    for l in cues["lines"]:
        if l["section"] == sec["id"]:
            out.append(f"| {mmss(l['start'])} | {NAMA[l['spk']]} | {l['text']} |")
    if sec["id"] == "rumusan" and cues["chant"]:
        words = " ".join(c["w"] + ("!" if i in (5, 11) else ",") for i, c in enumerate(cues["chant"]))
        out.append(f"| {mmss(cues['chant'][0]['t'])} | Pencerita + Wafiy (chant mengikut rentak) | {words} |")
    out.append("")
open(os.path.join(ROOT, "skrip.md"), "w").write("\n".join(out))
print("skrip.md ditulis")
