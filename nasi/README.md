# Bagaimana Jika Rakyat Malaysia Tidak Makan Nasi? (TikTok 9:16, ~99 s)

Kisah Kak Ros, penjual nasi lemak, dilukis di kanvas (`index.html`) dengan suara
naratif dalam Bahasa Melayu baku (tanpa slang), muzik, kesan bunyi dan bunyi suasana.

## Fail

- `index.html`: komposisi HyperFrames 1080×1920. Kanvas dilukis dari masa garis
  masa (`hf-seek`), jadi render sentiasa sama.
- `tools/naratif.json`: skrip suara, satu baris per babak (`scene`, `at`, `text`).
  Nombor dieja penuh supaya enjin suara menyebutnya betul.
- `tools/sebutan.json`: kamus sebutan baku (IPA) untuk perkataan yang enjin
  suara salah sebut, terutamanya e pepet (ə) lawan e taling (e).
- `tools/bina.py`: jana suara (lalai: suara wanita Piper `id_ID-news_tts`, sebutan
  ikut ejaan dari espeak-ng `id` + `tools/sebutan.json`), panjangkan
  babak supaya muat dengan suaranya, tulis tag `<audio>` dan tempoh ke `index.html`,
  kemudian jalankan `tools/audio.py`.
- `tools/audio.py`: muzik lo-fi, kesan bunyi dan suasana yang disintesis, ditekan
  (duck) bawah suara → `assets/audio/latar.mp3`; klip suara → `assets/audio/narasi/*.mp3`.
- `tools/video-asal.html`: fail kanvas asal sebelum disesuaikan.

## Tukar skrip atau suara

```bash
pip install onnxruntime phonemizer-fork espeakng-loader soundfile scipy
python3 tools/bina.py                      # Piper, laju 1.2
python3 tools/bina.py --speed 1.3          # lebih laju
python3 tools/bina.py --engine kokoro --voice if_sara   # suara Kokoro (berloghat)
npm run check
npm run render
```

Suara Piper ini dilatih dengan Bahasa Indonesia, jadi bunyinya dekat dengan sebutan
baku tetapi bukan penutur Malaysia. Jika ada perkataan yang disebut salah, tambah
sebutannya dalam `tools/sebutan.json`. Untuk suara penutur Malaysia, rakam sendiri
atau guna HeyGen/ElevenLabs, letak klip di `assets/audio/narasi/n01.mp3` …
`n16.mp3`, dan kemas kini `data-duration` dalam `index.html`.
