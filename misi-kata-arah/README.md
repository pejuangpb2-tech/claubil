# Misi Angkasa: Ekspedisi Kata Arah — Video Penerangan

Video penerangan animasi (Bahasa Melayu Tahun 3, SP 5.1.4 (iii) kata arah) untuk halaman
"Stesen Penerangan" dalam OPD Google Sites. Dibina dengan HyperFrames (HTML + GSAP → MP4).

## Hasil

| Fail | Keterangan |
|---|---|
| `renders/misi-kata-arah.mp4` | Video akhir 1920×1080, 30 fps, H.264 + AAC (tidak disimpan dalam git kerana saiznya) |
| `misi-kata-arah.srt` | Sari kata untuk YouTube |
| `thumbnail.png` | Imej kecil YouTube 1280×720 |
| `bab-youtube.txt` | Senarai bab mengikut stesen (tampal ke dalam penerangan YouTube) |
| `skrip.md` | Skrip akhir bermasa (untuk lampiran tugasan) |

## Bina semula

```bash
pip install edge-tts numpy
python3 tools/audio_build.py      # suara (ms-MY), muzik, SFX, campuran -16 LUFS, audio/cues.json
python3 tools/build_video.py      # index.html: masa setiap babak ikut audio sebenar
npx hyperframes render -o renders/misi-kata-arah.mp4
python3 tools/deliverables.py     # .srt dan bab YouTube
python3 tools/skrip_md.py         # skrip.md
python3 tools/thumbnail.py        # thumbnail.png
```

## Ganti suara dengan rakaman sendiri

1. Rakam setiap baris dalam `skrip.md` dan simpan sebagai WAV mono 48 kHz dengan nama yang sama dalam `audio/vo/`
   (contoh `audio/vo/12_atas.wav`). Jangan biarkan senyap panjang di hujung fail.
2. Jalankan semula `python3 tools/audio_build.py` dan `python3 tools/build_video.py`, kemudian render.
   Masa babak, kesan bunyi dan kapsyen mengikut tempoh fail baharu secara automatik.
3. Nota: masa setiap perkataan (untuk kapsyen karaoke dan SFX yang terikat pada perkataan) disimpan dalam
   `audio/vo/timing.json` dan datang daripada suara TTS. Untuk rakaman sendiri, masa perkataan perlu
   dikemas kini (contohnya dengan alat transkripsi), atau kapsyen akan sedikit tidak selari.

## Struktur

- `tools/skrip.py` — sumber tunggal skrip: penutur, teks, jeda visual dan kesan bunyi.
- `tools/index.template.html` — palet, watak SVG (Wafiy, Gogo, roket), prop dan fungsi animasi bersama.
- `compositions/` — satu babak bagi setiap bahagian (`pembukaan`, `masalah`, `s1`–`s5`, `rumusan`, `penutup`),
  bar kemajuan 5 planet (`prog`) dan kapsyen karaoke (`kapsyen`).
- `design/` — bingkai rujukan video contoh, bingkai gaya yang diluluskan dan thumbnail.

Semua ilustrasi dilukis sebagai SVG asli. Muzik dan kesan bunyi dicipta dengan kod (tiada bahan berhak cipta).
