#!/usr/bin/env python3
"""Make the male Malay voiceover with Microsoft's ms-MY-OsmanNeural voice.

Usage (from kata-ganti/):
    pip install edge-tts
    python3 tools/voiceover.py

Writes one MP3 per scene to assets/voice/ and prints each clip's length, so the
scene durations in index.html can follow the voice. Needs network access to
speech.platform.bing.com.
"""
import asyncio
import json
import os
import subprocess

import edge_tts

VOICE = "ms-MY-OsmanNeural"
RATE = "-5%"  # a touch slower for primary-school listeners

LINES = {
    "s1": "Hai, murid-murid! Selamat datang ke Misi Kata Ganti Nama Diri. Jom kumpul bintang sambil belajar!",
    "s2": "Kata ganti nama diri ialah perkataan yang menggantikan nama orang. Contohnya, Aina suka membaca. Dia membaca buku cerita.",
    "s3": "Kata ganti nama diri terbahagi kepada tiga pasukan. Mari kita kenali satu per satu!",
    "s4": "Pasukan pertama ialah orang pertama, iaitu orang yang bercakap. Contohnya saya, aku, kami dan kita. Gunakan saya apabila bercakap dengan guru.",
    "s5": "Gunakan kami apabila pendengar tidak termasuk. Gunakan kita apabila pendengar turut termasuk.",
    "s6": "Pasukan kedua ialah orang kedua, iaitu orang yang diajak bercakap. Contohnya kamu, awak, anda dan kalian. Kalian untuk ramai orang.",
    "s7": "Pasukan ketiga ialah orang ketiga, iaitu orang yang diperkatakan. Contohnya dia, mereka, beliau dan ia. Beliau untuk orang yang dihormati.",
    "s8": "Hebat! Mari kita ingat semula. Orang pertama, orang yang bercakap. Orang kedua, orang yang diajak bercakap. Orang ketiga, orang yang diperkatakan. Misi selesai!",
}


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


async def main():
    os.makedirs("assets/voice", exist_ok=True)
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    lengths = {}
    for sid, text in LINES.items():
        path = f"assets/voice/{sid}.mp3"
        await edge_tts.Communicate(text, VOICE, rate=RATE, proxy=proxy).save(path)
        lengths[sid] = round(duration(path), 2)
        print(f"{sid}: {lengths[sid]:.2f}s  {path}")
    with open("assets/voice/lengths.json", "w") as f:
        json.dump(lengths, f, indent=2)
    print(f"total {sum(lengths.values()):.2f}s")


asyncio.run(main())
