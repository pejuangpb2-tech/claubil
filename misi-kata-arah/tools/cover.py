#!/usr/bin/env python3
"""Jana kulit biodata (1920x1080, dirender 2x): foto sebenar dalam sut angkasawan,
latar angkasa dengan palet dan watak OPD Misi Angkasa.

Usage (dari misi-kata-arah/):  python3 tools/cover.py
Input:  design/cover/kepala.png (kepala yang telah dipotong, 720x1000, latar lutsinar)
Output: design/cover/cover-biodata.png dan .jpg
"""
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "design", "cover")
tpl = open(os.path.join(ROOT, "tools", "index.template.html")).read()
style = re.search(r"<style>(.*?)</style>", tpl, re.S).group(1).replace('url("assets/', 'url("../../assets/')
lib = re.findall(r"<script>(.*?)</script>", tpl, re.S)[1]
symbols = re.search(r'(<svg width="0" height="0".*?</svg>)\s*\n\s*<div id="root"', tpl, re.S).group(1)

# Pusat topi keledar dan skala kepala (kepala.png 720x1000; pusat muka pada (360, 450))
HX, HY, SC = 1340, 470, 0.62
IW, IH = 720 * SC, 1000 * SC
IX, IY = HX - 360 * SC, HY + 25 - 450 * SC

suit = f"""
<svg id="astro" viewBox="0 0 1920 1080" width="1920" height="1080">
 <defs>
  <radialGradient id="g-shell" cx="38%" cy="30%" r="75%">
   <stop offset="0" stop-color="#FFFFFF"/><stop offset=".55" stop-color="#E9E4F1"/><stop offset="1" stop-color="#A79FC2"/>
  </radialGradient>
  <linearGradient id="g-suit" x1="0" y1="0" x2="1" y2="0">
   <stop offset="0" stop-color="#B9B1D0"/><stop offset=".22" stop-color="#F4F1F8"/><stop offset=".55" stop-color="#FFFFFF"/>
   <stop offset=".8" stop-color="#E6E1EF"/><stop offset="1" stop-color="#A69EC0"/>
  </linearGradient>
  <linearGradient id="g-ring" x1="0" y1="0" x2="0" y2="1">
   <stop offset="0" stop-color="#E7E3EE"/><stop offset=".45" stop-color="#9C95B5"/><stop offset="1" stop-color="#5E5784"/>
  </linearGradient>
  <radialGradient id="g-inside" cx="50%" cy="45%" r="60%">
   <stop offset="0" stop-color="#2E2670"/><stop offset="1" stop-color="#120E38"/>
  </radialGradient>
  <radialGradient id="g-vig" cx="50%" cy="46%" r="58%">
   <stop offset=".62" stop-color="#0F0B2E" stop-opacity="0"/><stop offset="1" stop-color="#0F0B2E" stop-opacity=".7"/>
  </radialGradient>
  <linearGradient id="g-rim" x1="0" y1="0" x2="1" y2="0">
   <stop offset=".55" stop-color="#3EBFD2" stop-opacity="0"/><stop offset="1" stop-color="#3EBFD2" stop-opacity=".28"/>
  </linearGradient>
  <linearGradient id="g-glass" x1="0" y1="0" x2="1" y2="1">
   <stop offset="0" stop-color="#FFFFFF" stop-opacity=".16"/><stop offset=".35" stop-color="#FFFFFF" stop-opacity=".02"/>
   <stop offset=".8" stop-color="#9B8CFF" stop-opacity=".06"/><stop offset="1" stop-color="#3EBFD2" stop-opacity=".14"/>
  </linearGradient>
  <radialGradient id="g-halo" cx="50%" cy="50%" r="50%">
   <stop offset="0" stop-color="#3EBFD2" stop-opacity=".32"/><stop offset=".6" stop-color="#9B8CFF" stop-opacity=".12"/><stop offset="1" stop-color="#9B8CFF" stop-opacity="0"/>
  </radialGradient>
  <clipPath id="c-visor"><ellipse cx="{HX}" cy="{HY + 10}" rx="262" ry="292"/></clipPath>
  <filter id="f-soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>
  <filter id="f-shadow" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="18" stdDeviation="20" flood-color="#07051C" flood-opacity=".55"/></filter>
 </defs>

 <circle cx="{HX}" cy="{HY + 60}" r="560" fill="url(#g-halo)"/>

 <!-- badan sut -->
 <g filter="url(#f-shadow)">
  <path d="M{HX - 470} 1100 C{HX - 470} 960 {HX - 420} 880 {HX - 300} 845 C{HX - 200} 815 {HX - 120} 805 {HX} 805
           C{HX + 120} 805 {HX + 200} 815 {HX + 300} 845 C{HX + 420} 880 {HX + 470} 960 {HX + 470} 1100 Z" fill="url(#g-suit)"/>
  <!-- jalur lengan -->
  <path d="M{HX - 452} 990 C{HX - 440} 930 {HX - 410} 895 {HX - 360} 870 L{HX - 340} 905 C{HX - 385} 928 {HX - 410} 960 {HX - 418} 1004 Z" fill="#FE8B42"/>
  <path d="M{HX + 452} 990 C{HX + 440} 930 {HX + 410} 895 {HX + 360} 870 L{HX + 340} 905 C{HX + 385} 928 {HX + 410} 960 {HX + 418} 1004 Z" fill="#3EBFD2"/>
  <!-- jahitan -->
  <path d="M{HX - 300} 845 C{HX - 320} 930 {HX - 318} 1010 {HX - 300} 1100" stroke="#C4BDD8" stroke-width="5" fill="none"/>
  <path d="M{HX + 300} 845 C{HX + 320} 930 {HX + 318} 1010 {HX + 300} 1100" stroke="#C4BDD8" stroke-width="5" fill="none"/>
  <!-- panel kawalan dada -->
  <rect x="{HX - 120}" y="905" width="240" height="150" rx="22" fill="#3C3579" stroke="#1A1442" stroke-width="6"/>
  <rect x="{HX - 96}" y="925" width="120" height="58" rx="10" fill="#120E38"/>
  <path d="M{HX - 86} 960 l18 -16 l16 12 l20 -20 l18 14 l14 -8" stroke="#35D0BA" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="{HX + 62}" cy="940" r="15" fill="#FE585F"/><circle cx="{HX + 62}" cy="982" r="15" fill="#FDD13F"/>
  <rect x="{HX - 96}" y="1000" width="34" height="34" rx="8" fill="#3EBFD2"/><rect x="{HX - 52}" y="1000" width="34" height="34" rx="8" fill="#9B8CFF"/>
  <rect x="{HX - 8}" y="1000" width="34" height="34" rx="8" fill="#FE8B42"/><circle cx="{HX + 62}" cy="1020" r="15" fill="#35D0BA"/>
  <!-- tampalan misi (kiri penonton) -->
  <g transform="translate({HX - 300} 955)">
   <circle r="74" fill="#1E194C" stroke="#FDD13F" stroke-width="8"/>
   <circle r="58" fill="none" stroke="#3EBFD2" stroke-width="3" stroke-dasharray="6 8"/>
   <use href="#a-rocket" x="-40" y="-30" width="80" height="37" transform="rotate(-30)"/>
   <text y="38" text-anchor="middle" font-family="Nunito KA" font-weight="900" font-size="13" fill="#FDD13F" letter-spacing=".5">MISI</text><text y="54" text-anchor="middle" font-family="Nunito KA" font-weight="900" font-size="13" fill="#FDD13F" letter-spacing=".5">ANGKASA</text>
  </g>
  <!-- Jalur Gemilang (bahu kiri angkasawan) -->
  <g id="flag" transform="translate({HX + 228} 905) rotate(6)"></g>
 </g>

 <!-- gelang leher -->
 <ellipse cx="{HX}" cy="{HY + 345}" rx="250" ry="58" fill="url(#g-ring)" stroke="#4A4373" stroke-width="5"/>
 <ellipse cx="{HX}" cy="{HY + 330}" rx="228" ry="40" fill="none" stroke="#FFFFFF" stroke-opacity=".55" stroke-width="4"/>

 <!-- cangkerang topi keledar -->
 <circle cx="{HX}" cy="{HY}" r="345" fill="url(#g-shell)" stroke="#8F87AE" stroke-width="5"/>
 <rect x="{HX - 362}" y="{HY - 70}" width="40" height="140" rx="18" fill="#D9D3E6" stroke="#8F87AE" stroke-width="4"/>
 <rect x="{HX + 322}" y="{HY - 70}" width="40" height="140" rx="18" fill="#D9D3E6" stroke="#8F87AE" stroke-width="4"/>
 <circle cx="{HX + 342}" cy="{HY - 100}" r="11" fill="#FE585F"/>
 <rect x="{HX + 336}" y="{HY - 210}" width="12" height="100" rx="6" fill="#B8B0CF"/>

 <!-- bahagian dalam visor + kepala sebenar + kaca -->
 <ellipse cx="{HX}" cy="{HY + 10}" rx="270" ry="300" fill="#5E5784"/>
 <g clip-path="url(#c-visor)">
  <rect x="{HX - 280}" y="{HY - 300}" width="560" height="620" fill="url(#g-inside)"/>
  <image href="kepala.png" x="{IX:.1f}" y="{IY:.1f}" width="{IW:.1f}" height="{IH:.1f}" preserveAspectRatio="none"/>
  <rect x="{HX - 280}" y="{HY - 300}" width="560" height="620" fill="url(#g-rim)"/>
  <rect x="{HX - 280}" y="{HY - 300}" width="560" height="620" fill="url(#g-vig)"/>
  <rect x="{HX - 280}" y="{HY - 300}" width="560" height="620" fill="url(#g-glass)"/>
  <path d="M{HX - 200} {HY - 150} C{HX - 170} {HY - 240} {HX - 70} {HY - 285} {HX + 30} {HY - 282}" stroke="#FFFFFF" stroke-opacity=".55" stroke-width="20" fill="none" stroke-linecap="round" filter="url(#f-soft)"/>
  <path d="M{HX - 228} {HY - 60} C{HX - 236} {HY - 100} {HX - 226} {HY - 128} {HX - 214} {HY - 148}" stroke="#FFFFFF" stroke-opacity=".6" stroke-width="9" fill="none" stroke-linecap="round"/>
  <ellipse cx="{HX + 190}" cy="{HY + 190}" rx="34" ry="12" transform="rotate(-48 {HX + 190} {HY + 190})" fill="#FFFFFF" fill-opacity=".22" filter="url(#f-soft)"/>
 </g>
 <ellipse cx="{HX}" cy="{HY + 10}" rx="266" ry="296" fill="none" stroke="#2A2266" stroke-width="10"/>
 <ellipse cx="{HX}" cy="{HY + 10}" rx="280" ry="310" fill="none" stroke="#FFFFFF" stroke-opacity=".7" stroke-width="4"/>
</svg>"""

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{style}
html,body{{width:1920px;height:1080px;margin:0;overflow:hidden;background:#1E194C}}
#astro{{position:absolute;left:0;top:0}}
.neb{{position:absolute;border-radius:50%;filter:blur(60px)}}
#n1{{left:-200px;top:-260px;width:900px;height:700px;background:rgba(155,140,255,.20)}}
#n2{{left:1050px;top:560px;width:900px;height:700px;background:rgba(62,191,210,.12)}}
#n3{{left:420px;top:620px;width:700px;height:500px;background:rgba(254,88,95,.08)}}
#moon{{position:absolute;left:-260px;top:830px;width:1500px;height:520px}}
#kick{{position:absolute;left:110px;top:190px;font:900 50px var(--font);letter-spacing:12px;color:var(--cyan)}}
#big{{position:absolute;left:100px;top:262px;font:900 180px/.95 var(--font);color:#fff;text-shadow:0 14px 0 #0F0B2E}}
#big .y{{color:var(--yellow)}}
#pill{{position:absolute;left:112px;top:672px;font:900 46px var(--font);color:var(--ink);background:var(--yellow);border:6px solid var(--ink);border-radius:999px;padding:8px 34px;box-shadow:0 8px 0 rgba(10,7,32,.55)}}
#sub{{position:absolute;left:118px;top:780px;font:800 34px var(--font);color:var(--cream);opacity:.85;letter-spacing:1px}}
.dec{{position:absolute}}
#rk{{left:640px;top:14px;width:290px;height:135px;transform:rotate(-14deg)}}
#trail{{left:330px;top:70px;width:340px;height:80px}}
#ring{{left:1640px;top:26px;width:250px;height:173px}}
#red{{left:1770px;top:600px;width:84px;height:84px}}
#gogo{{left:700px;top:850px;width:180px;height:190px;transform:rotate(-8deg)}}
#st1{{left:1060px;top:120px;width:46px;height:46px}}#st2{{left:1810px;top:430px;width:38px;height:38px}}#st3{{left:900px;top:600px;width:30px;height:30px}}
#comet{{left:1150px;top:30px;width:180px;height:63px;transform:rotate(12deg)}}
</style><script>window.CUES={{"lines":[],"sections":[],"chant":[],"total":1}};</script><script>{lib}</script></head><body>
{symbols}
<div id="root"><div class="sky"></div><div class="stars s1"></div><div class="stars s2"></div><div class="stars s3"></div>
<div class="neb" id="n1"></div><div class="neb" id="n2"></div><div class="neb" id="n3"></div>
<svg id="moon" viewBox="0 0 1500 520"><ellipse cx="750" cy="400" rx="900" ry="250" fill="#493F8F" stroke="#3C3579" stroke-width="8"/>
<ellipse cx="420" cy="230" rx="110" ry="26" fill="#3C3579"/><ellipse cx="900" cy="270" rx="70" ry="18" fill="#3C3579"/><ellipse cx="1180" cy="330" rx="130" ry="30" fill="#3C3579"/></svg>
<svg class="dec" id="trail" viewBox="0 0 340 80"><path d="M10 72 C110 66 220 46 330 14" stroke="#FDD13F" stroke-width="6" stroke-dasharray="4 18" stroke-linecap="round" fill="none" opacity=".7"/></svg>
<div class="dec" id="rk"></div>
<svg class="dec" id="ring"><use href="#a-planet-ring" width="250" height="173"/></svg>
<svg class="dec" id="red"><use href="#a-planet-red" width="84" height="84"/></svg>
<svg class="dec" id="comet"><use href="#a-comet" width="180" height="63"/></svg>
<svg class="dec" id="st1"><use href="#a-star" width="46" height="46"/></svg><svg class="dec" id="st2"><use href="#a-star" width="38" height="38"/></svg><svg class="dec" id="st3"><use href="#a-star" width="30" height="30"/></svg>
{suit}
<div class="dec" id="gogo"></div>
<div id="kick">MISI ANGKASA</div>
<div id="big">BIODATA<br><span class="y">DIRI</span></div>
<div id="pill">Ketua Misi · Guru Pelatih</div>
<div id="sub">Ekspedisi Kata Arah · Bahasa Melayu Tahun 3</div>
</div>
<script>
document.getElementById('rk').innerHTML=KA.svgRocket('cr',{{face:true}});
document.getElementById('gogo').innerHTML=KA.svgGogo('cg');
/* Jalur Gemilang: 14 jalur, kanton biru, anak bulan dan bintang pecah 14 */
(function(){{
  const W=150,H=75,sh=H/14;let s=`<rect x="-6" y="-6" width="${{W+12}}" height="${{H+12}}" rx="8" fill="#FFFFFF" stroke="#C4BDD8" stroke-width="3"/>`;
  for(let i=0;i<14;i++) s+=`<rect x="0" y="${{i*sh}}" width="${{W}}" height="${{sh+0.3}}" fill="${{i%2?'#FFFFFF':'#CC0001'}}"/>`;
  const cw=W/2,chh=sh*8;s+=`<rect x="0" y="0" width="${{cw}}" height="${{chh}}" fill="#010066"/>`;
  const cy=chh/2,r=chh*0.4;
  s+=`<circle cx="${{cw*0.36}}" cy="${{cy}}" r="${{r}}" fill="#FFCC00"/><circle cx="${{cw*0.36+r*0.28}}" cy="${{cy}}" r="${{r*0.83}}" fill="#010066"/>`;
  const sx=cw*0.68,R=r*0.78,ri=R*0.45;let p=[];
  for(let k=0;k<28;k++){{const a=-Math.PI/2+k*Math.PI/14,rr=k%2?ri:R;p.push((sx+rr*Math.cos(a)).toFixed(2)+','+(cy+rr*Math.sin(a)).toFixed(2));}}
  s+=`<polygon points="${{p.join(' ')}}" fill="#FFCC00"/>`;
  document.getElementById('flag').innerHTML=s;
}})();
</script></body></html>"""
page = os.path.join(OUT, "cover.html")
open(page, "w").write(html)
png = os.path.join(OUT, "cover-biodata.png")
js = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  const p = await b.newPage({{ viewport: {{ width: 1920, height: 1080 }}, deviceScaleFactor: 2 }});
  await p.goto('file://{page}');
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400);
  await p.screenshot({{ path: '{png}' }});
  await b.close();
}})();"""
subprocess.run(["node", "-e", js], check=True)
subprocess.run(["python3", "-c", f"from PIL import Image;Image.open('{png}').convert('RGB').save('{png[:-4]}.jpg',quality=92)"], check=True)
print("cover-biodata.png / .jpg ditulis (3840x2160)")
