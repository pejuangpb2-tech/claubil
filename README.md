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

Two realistic shots generated with Google Veo, plus an animated greeting
(`compositions/ucapan.html`: "Selamat Hari Raya Aidilfitri · Maaf Zahir & Batin").

| Time | Shot | Prompt |
| --- | --- | --- |
| 0–5 s | Family salam (bermaaf-maafan) on Raya morning | `prompts/shot1.txt` |
| 5–10 s | Wide: family, rendang cooking, kids with sparklers + greeting | `prompts/shot2.txt` |

Generate the clips (needs `GEMINI_API_KEY` in the environment; billed by Google):

```bash
python3 tools/veo.py prompts/shot1.txt assets/shot1.mp4
python3 tools/veo.py prompts/shot2.txt assets/shot2.mp4
```

Then `npm run check` and `npm run render`.
