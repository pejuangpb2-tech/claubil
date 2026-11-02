#!/usr/bin/env python3
"""Jana index.html daripada tools/index.template.html + audio/cues.json.

Usage (dari misi-kata-arah/):
    python3 tools/audio_build.py   # audio + cues.json
    python3 tools/build_video.py   # index.html (masa setiap babak ikut audio sebenar)
    npx hyperframes render
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cues = json.load(open(os.path.join(ROOT, "audio", "cues.json")))
tpl = open(os.path.join(ROOT, "tools", "index.template.html")).read()

total = round(cues["total"], 3)
sec = {s["id"]: s for s in cues["sections"]}
hosts = []


def host(cid, start, dur, kind="graphics", z=1, track=1):
    hosts.append(
        f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
        f'data-start="{start:.3f}" data-duration="{dur:.3f}" data-track-index="{track}" data-track-kind="{kind}" '
        f'data-width="1920" data-height="1080" style="z-index:{z}"></div>'
    )


order = [s["id"] for s in cues["sections"]]
for i, sid in enumerate(order):
    s = sec[sid]
    end = total if i == len(order) - 1 else sec[order[i + 1]]["start"]
    host(sid, s["start"], end - s["start"])
# bar kemajuan: dari Stesen 1 hingga sebelum Penutup
host("prog", sec["s1"]["start"], sec["penutup"]["start"] - sec["s1"]["start"], z=5, track=2)
host("kapsyen", 0, total, kind="captions", z=10, track=3)

out = (tpl.replace("%CUES%", json.dumps(cues, ensure_ascii=False, separators=(",", ":")))
          .replace("%TOTAL%", f"{total:.3f}")
          .replace("%HOSTS%", "\n".join(hosts)))
open(os.path.join(ROOT, "index.html"), "w").write(out)
print(f"index.html: {len(hosts)} host, tempoh {total:.2f} s")
