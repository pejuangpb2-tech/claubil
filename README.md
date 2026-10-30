# claubil

A [HyperFrames](https://hyperframes.heygen.com) video project: HTML + GSAP rendered to MP4.

## Setup

```bash
npm install -g hyperframes
hyperframes browser ensure   # downloads Chrome Headless Shell for rendering
npm install
```

## Usage

```bash
npm run check    # lint + runtime validation
npm run dev      # preview in the browser
npm run render   # render to renders/*.mp4
```

## Notes

- GSAP is loaded from `vendor/gsap.min.js` instead of a CDN, so rendering works in
  environments where CDNs are blocked. If you upgrade GSAP, re-copy
  `node_modules/gsap/dist/gsap.min.js` into `vendor/`.
- `.claude/skills/` holds the HyperFrames skills for Claude Code
  (update with `npx hyperframes skills update`).

## Hari Raya video (10 s)

`index.html` renders a 3D Hari Raya morning made with Three.js
(`compositions/raya.html`, vendored as `vendor/three.min.js`):

- 0–4 s: close on the family. The son and daughter walk in and do salam
  (bermaaf-maafan) with their father and mother.
- 4–6 s: the camera cranes back to reveal the kampung house, a woman stirring
  rendang over a wood fire, and two children waving sparklers.
- 5–10 s: the greeting "Selamat Hari Raya Aidilfitri · Maaf Zahir & Batin"
  (`compositions/ucapan.html`).

### Photoreal version (Google Veo)

`veo/` holds a live-action alternative: two shots generated with Google Veo and the
same greeting. It needs `GEMINI_API_KEY` in the environment (billed by Google):

```bash
python3 tools/veo.py veo/prompts/shot1.txt assets/shot1.mp4
python3 tools/veo.py veo/prompts/shot2.txt assets/shot2.mp4
cp veo/index.html index.html
```

Then `npm run check` and `npm run render`.
