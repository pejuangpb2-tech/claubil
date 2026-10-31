#!/usr/bin/env python3
"""Make the male Malay voiceover with Microsoft's ms-MY-OsmanNeural voice.

Usage (from kata-ganti/):
    pip install edge-tts
    python3 tools/voiceover.py

Writes one MP3 per scene to assets/voice/ plus assets/voice/timing.json, which
holds each clip's length and the start time of every spoken word, so scenes and
reveals can follow the voice. Needs network access to speech.platform.bing.com.
"""
import asyncio
import json
import os
import subprocess

import edge_tts

VOICE = "ms-MY-OsmanNeural"
RATE = "+5%"

LINES = {
    "s1": "Hai, murid-murid! Jom sertai Misi Kata Ganti Nama Diri!",
    "s2": "Kata ganti nama diri ialah perkataan yang menggantikan nama orang. Contohnya, Aina suka membaca. Dia membaca buku cerita.",
    "s3": "Kata ganti nama diri ada tiga pasukan. Jom kenali!",
    "s4": "Pasukan pertama, orang yang bercakap. Contohnya, saya, aku, kami dan kita.",
    "s5": "Kami, pendengar tidak termasuk. Kita, pendengar turut termasuk.",
    "s6": "Pasukan kedua, orang yang diajak bercakap. Contohnya, kamu, awak, anda dan kalian.",
    "s7": "Pasukan ketiga, orang yang diperkatakan. Contohnya, dia, mereka, beliau dan ia.",
    "s8": "Hebat! Ingat tiga pasukan ini: orang pertama, orang kedua dan orang ketiga. Misi selesai!",
}


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


async def speak(text, path, proxy):
    words = []
    com = edge_tts.Communicate(text, VOICE, rate=RATE, proxy=proxy, boundary="WordBoundary")
    with open(path, "wb") as f:
        async for chunk in com.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                words.append({"w": chunk["text"], "t": round(chunk["offset"] / 1e7, 3)})
    return words


async def main():
    os.makedirs("assets/voice", exist_ok=True)
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    timing = {}
    for sid, text in LINES.items():
        path = f"assets/voice/{sid}.mp3"
        words = await speak(text, path, proxy)
        timing[sid] = {"length": round(duration(path), 2), "words": words}
        print(f"{sid}: {timing[sid]['length']:.2f}s  {len(words)} words")
    with open("assets/voice/timing.json", "w") as f:
        json.dump(timing, f, indent=1, ensure_ascii=False)
    print(f"total {sum(t['length'] for t in timing.values()):.2f}s")


asyncio.run(main())
