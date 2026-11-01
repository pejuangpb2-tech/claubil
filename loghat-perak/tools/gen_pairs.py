# Generates compositions/pasangan-N.html: one standard (❌) / Perak (✅) word pair per segment.
import json, sys
out_dir = sys.argv[1]
PAIRS = [
  # id, biasa, perak, t_biasa, t_perak, exit_start, wobble_at (abs s or None), reaction sticker
  (1, "SUKA",       "INGKER",      3.700,  6.500,  8.40,  None, "🤩"),
  (2, "MENYAMPAH",  "GETIK",       11.600, 14.100, 18.60, None, "🤢"),
  (3, "TAK KERUAN", "RABAN TEBEN", 22.867, 28.233, 30.65, 25.0, "😵‍💫"),
  (4, "SEMBANG",    "MELABUN",     34.200, 37.300, 39.98, None, "🤥"),
  (5, "BALIK",      "BERANSUR",    43.533, 45.700, 47.15, None, "🏃"),
  (6, "MATI",       "TUMPO",       51.167, 52.733, 55.25, None, "💀"),
]
TPL = open(sys.argv[2]).read()
hosts = []
for n, biasa, perak, tb, tp, ex, wob, sticker in PAIRS:
    d_perak = round(tp - tb, 3)
    d_exit = round(ex - tb, 3)
    dur = round(d_exit + 0.2, 3)
    wobble = "" if wob is None else (
        f'    tl.to("#pasangan-{n}-w1", {{ rotation: -4, duration: 0.1, ease: "power2.out" }}, {round(wob - tb, 3)})\n'
        f'      .to("#pasangan-{n}-w1", {{ rotation: 3, duration: 0.12, ease: "power2.inOut" }})\n'
        f'      .to("#pasangan-{n}-w1", {{ rotation: 0, duration: 0.18, ease: "power2.out" }});\n')
    vars_ = json.dumps([
        {"id": "biasa", "type": "string", "label": "Perkataan biasa", "default": biasa},
        {"id": "perak", "type": "string", "label": "Perkataan Perak", "default": perak},
        {"id": "sticker", "type": "string", "label": "Emoji reaksi", "default": sticker},
    ], ensure_ascii=False)
    html = (TPL.replace("__ID__", f"pasangan-{n}").replace("__VARS__", vars_.replace("'", "&#39;"))
               .replace("__BIASA__", biasa).replace("__PERAK__", perak).replace("__STICKER__", sticker)
               .replace("__DPERAK__", str(d_perak)).replace("__DEXIT__", str(d_exit)).replace("__WOBBLE__", wobble))
    open(f"{out_dir}/pasangan-{n}.html", "w").write(html)
    hosts.append((n, tb, dur))
for n, tb, dur in hosts:
    print(f'      <div id="pasangan-{n}" data-composition-id="pasangan-{n}" data-composition-src="compositions/pasangan-{n}.html" data-start="{tb}" data-duration="{dur}" data-track-index="2" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 3"></div>')
