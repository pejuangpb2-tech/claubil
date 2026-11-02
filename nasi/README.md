# Kalau Rakyat Malaysia Tak Makan Nasi? (TikTok 9:16, ~89 s)

Kisah Kak Ros, penjual nasi lemak, dilukis di kanvas (`index.html`) dengan suara
naratif Bahasa Melayu, muzik, kesan bunyi dan bunyi suasana.

## Fail

- `index.html`: komposisi HyperFrames 1080×1920. Kanvas dilukis dari masa garis
  masa (`hf-seek`), jadi render sentiasa sama.
- `tools/naratif.json`: skrip suara, satu baris per babak (`scene`, `at`, `text`).
  Nombor dieja penuh supaya enjin suara menyebutnya betul.
- `tools/bina.py`: jana suara (Kokoro, sebutan `ms` dari espeak-ng), panjangkan
  babak supaya muat dengan suaranya, tulis tag `<audio>` dan tempoh ke `index.html`,
  kemudian jalankan `tools/audio.py`.
- `tools/audio.py`: muzik lo-fi, kesan bunyi dan suasana yang disintesis, ditekan
  (duck) bawah suara → `assets/audio/latar.mp3`; klip suara → `assets/audio/narasi/*.mp3`.
- `tools/video-asal.html`: fail kanvas asal sebelum disesuaikan.

## Tukar skrip atau suara

```bash
pip install kokoro-onnx soundfile scipy
python3 tools/bina.py                      # suara lalai: ef_dora, laju 1.05
python3 tools/bina.py --voice af_heart --speed 1.1
npm run check
npm run render
```

Suara wanita lain untuk dicuba: `if_sara`, `pf_dora`, `af_heart`, `bf_emma`,
`hf_alpha`. Kokoro tiada suara asli Bahasa Melayu, jadi sebutannya berloghat. Untuk
suara Melayu asli, rakam sendiri atau guna HeyGen/ElevenLabs, letak klip di
`assets/audio/narasi/n01.mp3` … `n16.mp3`, dan kemas kini `data-duration` dalam `index.html`.
