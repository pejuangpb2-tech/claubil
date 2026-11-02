#!/usr/bin/env python3
"""Jana thumbnail.png (1280x720) untuk YouTube: Wafiy, roket, Gogo dan perkataan KATA ARAH.

Usage (dari misi-kata-arah/):  python3 tools/thumbnail.py
Menggunakan watak SVG yang sama dengan video (pustaka KA dalam tools/index.template.html).
"""
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tpl = open(os.path.join(ROOT, "tools", "index.template.html")).read()
cues = open(os.path.join(ROOT, "audio", "cues.json")).read()
style = re.search(r"<style>(.*?)</style>", tpl, re.S).group(1).replace('url("assets/', 'url("../assets/')
lib = re.findall(r"<script>(.*?)</script>", tpl, re.S)[1]
symbols = re.search(r'(<svg width="0" height="0".*?</svg>)\s*\n\s*<div id="root"', tpl, re.S).group(1)

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{style}
html,body{{width:1920px;height:1080px}}
#t-kick{{position:absolute;left:96px;top:120px;font:900 64px var(--font);letter-spacing:12px;color:var(--cyan)}}
#t-big{{position:absolute;left:84px;top:200px;font:900 250px/0.95 var(--font);color:#fff;text-shadow:0 14px 0 #0F0B2E}}
#t-sub{{position:absolute;left:100px;top:760px;font:900 62px var(--font);color:var(--ink);background:var(--yellow);border:7px solid var(--ink);border-radius:999px;padding:10px 40px}}
#t-w{{position:absolute;left:1180px;top:330px;width:520px;height:702px}}
#t-r{{position:absolute;left:1180px;top:60px;width:620px;height:289px}}
#t-g{{position:absolute;left:1560px;top:680px;width:300px;height:317px}}
</style><script>window.CUES={cues};</script><script>{lib}</script></head><body>
{symbols}
<div id="root"><div class="sky"></div><div class="stars s1"></div><div class="stars s2"></div><div class="stars s3"></div>
<div id="t-kick">MISI ANGKASA</div>
<div id="t-big">KATA<br><span class="y">ARAH</span></div>
<div id="t-sub">Bahasa Melayu · Tahun 3</div>
<div id="t-r"></div><div id="t-w"></div><div id="t-g"></div></div>
<script>
document.getElementById('t-w').innerHTML=KA.svgWafiy('tw');
document.getElementById('t-r').innerHTML=KA.svgRocket('tr',{{face:true}});
document.getElementById('t-g').innerHTML=KA.svgGogo('tg');
document.getElementById('t-r').style.transform='rotate(-14deg)';
</script></body></html>"""
page = os.path.join(ROOT, "design", "thumbnail.html")
open(page, "w").write(html)
js = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  const p = await b.newPage({{ viewport: {{ width: 1920, height: 1080 }}, deviceScaleFactor: 2 / 3 }});
  await p.goto('file://{page}');
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  await p.screenshot({{ path: '{os.path.join(ROOT, "thumbnail.png")}' }});
  await b.close();
}})();"""
subprocess.run(["node", "-e", js], check=True)
print("thumbnail.png ditulis")
