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
