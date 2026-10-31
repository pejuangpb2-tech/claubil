# Misi Angkasa: Ekspedisi Kata Arah — Video Penerangan (Fasa 1 + Bingkai Gaya)

Status: **menunggu kelulusan guru**. Video penuh belum dibina.

## 0. Penyelarasan dengan perbincangan kita

| Perkara | Prompt asal | Yang diselaraskan |
|---|---|---|
| Tempoh | 6:00–6:30 | **Sasaran ~3:00–3:20** (seperti yang kita bincang). Kandungan dipadatkan: lihat §4 "Apa yang dipendekkan". |
| Suara latar | edge-tts ms-MY | **Sampel dahulu** (folder `sampel-suara/`). Guru pilih sebelum audio penuh dijana. |
| Kredit | – | **Tiada kredit.** |
| Muzik latar | ciptaan sendiri | **Ada muzik latar** ciptaan sendiri (kod), perlahan, dengan *ducking* semasa suara. |
| Kuiz / latihan | dilarang | **Tiada** kuiz, soalan, pemasa atau "jeda video". Bahagian "Kuiz!" video contoh tidak digunakan. |
| Bahasa | BM standard | BM Malaysia standard DBP; suara **ms-MY sahaja** (bukan id-ID); kosa kata Indonesia dielakkan. |

## 1. Ringkasan gaya video contoh (`kata_arah_ipan_1.mp4`)

Bingkai rujukan: `design/rujukan/` (0:04, 0:10, 0:38, 0:57).

- **Diukur** (sampel piksel): latar `#1E194C`, bahagian gelap `#16113E`, permukaan bulan `#493F8F`, kawah `#3C3579`, kuning `#FDD13F`, merah karang roket `#FE585F`, cyan tingkap `#3EBFD2`, oren api `#FE8B42`, krim `#F4EFEA`.
- **Fon**: sans-serif bulat tebal; padanan terdekat **Nunito 900/800** (fail fon disimpan dalam `assets/fonts/`).
- **Watak**: Aira (angkasawan, muka nampak di sebalik visor, sut putih, sarung tangan dan but oren), Gogo (makhluk hijau bermata satu, dua antena kuning), roket mendatar (badan krim, hidung/sirip merah karang, tingkap cyan, api oren).
- **Tatabahasa visual**: satu ayat di bahagian atas/bawah, objek di tengah, label kata arah kuning dengan anak panah, cip bulat **di** (merah jambu) / **ke** (oren) / **dari** (teal).

## 2. Bingkai gaya (Fasa 2) — `design/bingkai-gaya/`

1. `01-tajuk.png` – MISI ANGKASA / Ekspedisi KATA ARAH / Bahasa Melayu · Tahun 3; Aira, roket, Gogo di permukaan bulan.
2. `02-gerabak.png` – kereta api angkasa [di] → [atas] → [meja] dengan label + contoh gaya kapsyen karaoke.
3. `03-pasangan-atas.png` – "Pasangan 1: atas ↔ bawah", bintang di atas roket, label ATAS "pop" + anak panah, ayat dengan kata arah kuning bergaris bawah.
4. `04-kiri.png` – Aira **dari belakang**, tangan kiri bercincin kuning, planet merah di kiri, tip "kiri Aira = kiri kamu".
5. `05-di-ke-dari.png` – cip di/ke/dari (ke aktif), Gogo melompat ke atas batu dengan laluan anak panah oren.
6. `06-formula-ayat.png` – modul roket: Siapa/Apa? + Buat apa? + di/ke/dari + kata arah + benda/tempat + noktah.

Elemen tetap di setiap stesen: **bar kemajuan 5 planet** (atas tengah), tag stesen/pasangan (kiri atas), latar bintang 3 lapisan (bergerak parallax dalam video).

**Cadangan kapsyen**: kapsyen karaoke di bawah untuk semua narasi; **kecuali** apabila ayat yang sama sudah dipaparkan besar di tengah skrin (contoh 12 ayat Stesen 2). Pada ketika itu, ayat besar itulah yang diserlahkan perkataan demi perkataan, supaya teks tidak berulang dua kali di skrin. Fail `.srt` YouTube tetap mengandungi semua narasi.

## 3. Skrip (sasaran ~3:10) — anggaran masa, akan dilaras ikut tempoh audio sebenar

Watak suara: **N** = pencerita, **A** = Aira, **G** = Gogo.

| Bahagian | Masa | Visual | Dialog / Narasi | Teks skrin | SFX |
|---|---|---|---|---|---|
| Pembukaan | 0:00–0:14 | Roket di permukaan bulan → kira detik → roket naik → warp → tajuk → peta 5 planet | A: "Tiga, dua, satu… berlepas!" · N: "Hari ini, kita belajar apa itu kata arah, kegunaannya, cara menggunakannya dan cara membina ayat. Jom!" | MISI ANGKASA / Ekspedisi KATA ARAH / Bahasa Melayu · Tahun 3; nama 5 stesen | roket, whoosh warp |
| Masalah Gogo | 0:14–0:25 | Aira di dalam roket; radio berkelip | G: "Aira! Tolong! Saya ada di… di… alamak, saya tidak tahu cara hendak memberitahu!" · A: "Jangan risau, Gogo! Mari kita belajar kata arah dahulu." | – | bip radio |
| Stesen 1: Apa itu Kata Arah? | 0:25–0:48 | Kad stesen → bintang dengan anak panah 4 hala → kereta api [di][atas][meja] → baris kecil | N: "Kata arah ialah perkataan yang menunjukkan arah atau kedudukan sesuatu benda." · "Kata arah datang selepas di, ke atau dari, dan sebelum nama benda atau tempat. Contohnya, di atas meja." · "Kata arah ialah sejenis kata tugas." | Definisi ("arah", "kedudukan" kuning); label gerabak | pop, klik gerabak |
| Stesen 2: Kenali Kata Arah | 0:48–1:58 | 12 kata arah, ~5 s setiap satu: objek bergerak → label "pop" + anak panah → ayat dibaca. Roket sebagai rujukan. | N sebut kata arah, kemudian ayat (12 ayat **tidak diubah**, lihat bawah) · sebelum kiri: "Kita lihat dari belakang Aira." · N: "Tahukah kamu? Utara, selatan, timur dan barat juga kata arah!" | "Pasangan 1–5" + "Bonus"; tip kiri/kanan; kompas; grid 12 lencana | pop setiap label |
| Stesen 3: Kegunaan | 1:58–2:16 | 3 kad kegunaan dengan animasi angkasa | N: "Kata arah memberitahu kedudukan. Satelit berada di sebelah kanan bulan." · "Kata arah menunjukkan hala tuju. Roket terbang ke atas." · "Kata arah memberitahu tempat asal. Gogo keluar dari dalam roket." | di mana? / ke mana? / dari mana? | whoosh roket |
| Stesen 4: Cara Menggunakan | 2:16–2:48 | Gogo + batu (di/ke/dari); laser roket memotong "diatas" → "di atas"; tip dua lajur; ayat tergantung; antara…dengan | N: "Gogo berdiri di atas batu. Gogo melompat ke atas batu. Gogo turun dari atas batu." · "Ingat, di, ke dan dari ditulis terpisah." · "Tetapi di yang melekat pada perbuatan ditulis rapat, seperti diletakkan." · "Jangan guna 'daripada' untuk tempat atau arah." · "Bola itu berada di bawah… di bawah apa? Di bawah meja!" · "Bulan berada di antara roket dengan planet. Guna 'dengan', bukan 'dan'." | cip di/ke/dari; ✓ di atas ✗ diatas, ✓ ke dalam ✗ kedalam, ✓ dari luar ✗ dariluar; "di + tempat → JARAK / di + perbuatan → RAPAT" | laser, ✓ ding |
| Stesen 5: Bina Ayat | 2:48–3:12 | Formula modul roket → contoh dibina modul demi modul (think-aloud) → tip ayat → Gogo bina ayatnya → Aira jumpa Gogo | N: "Siapa? Aira. Buat apa? Duduk. Di mana? Di dalam roket." → "Aira duduk di dalam roket." · "Mulakan dengan huruf besar, pilih kata arah yang tepat, dan akhiri dengan noktah." · G: "Aira! Saya bersembunyi di belakang batu besar!" · A: "Saya jumpa kamu, Gogo!" | modul berwarna; 3 ikon tip | klik modul, sorakan |
| Penutup | 3:12–3:20 | Konfeti, roket terbang keluar | N: "Syabas! Sekarang kamu sudah tahu tentang kata arah. Teruskan misi kamu di Zon Cabaran. Jumpa lagi!" | "Syabas, angkasawan cilik!" | sorakan |

**12 ayat Stesen 2 (seperti dalam prompt, tidak diubah)**, susunan: atas↔bawah, dalam↔luar, hadapan↔belakang, kiri↔kanan, tepi↔tengah, Bonus: antara, sisi.

1. Bintang berkelip di atas roket. 2. Bumi kelihatan di bawah roket. 3. Aira duduk di dalam roket. 4. Gogo melambai di luar roket. 5. Bulan bersinar di hadapan roket. 6. Komet meluncur di belakang roket. 7. Planet merah berada di sebelah kiri Aira. 8. Planet biru berada di sebelah kanan Aira. 9. Bendera dipacak di tepi kawah. 10. Matahari berada di tengah sistem suria. 11. Bulan berada di antara dua bintang. 12. Tangga diletakkan di sisi roket.

## 4. Apa yang dipendekkan supaya muat ~3 minit (perlu kelulusan guru)

Prompt meminta saya bertanya sebelum mengubah ayat contoh Stesen 3–5. Cadangan saya:

| Bahagian | Dalam prompt | Cadangan 3 minit |
|---|---|---|
| Stesen 3 | 3 kegunaan + montaj harian (kasut, pisau, sekolah) | 3 kegunaan sahaja; **montaj harian dibuang** |
| Stesen 5 | 3 ayat contoh + think-aloud satelit | **1 contoh** (Aira duduk di dalam roket) yang dibina secara think-aloud; contoh Gogo, komet dan satelit dibuang |
| Rumusan | 4 poin + chant | **Dibuang**; diganti dengan penutup ringkas (rumusan ada di halaman Misi Berjaya) |
| Dialog | – | Dialog Gogo diubah daripada "saya tak tahu nak cakap" kepada "saya tidak tahu cara hendak memberitahu" (elak bahasa basahan) |

Jika guru mahu semua kandungan prompt dikekalkan, tempoh akan menjadi kira-kira 5–6 minit.

## 5. Senarai semak fakta Bahagian 1 → kedudukan dalam video

| Fakta | Di mana |
|---|---|
| Definisi kata arah | Stesen 1 (teks + narasi) |
| Kata arah selepas di/ke/dari, sebelum nama benda/tempat | Stesen 1 (kereta api [di][atas][meja]) |
| Kata arah ialah sejenis kata tugas | Stesen 1 (baris kecil) |
| di = kedudukan, ke = hala tuju, dari = tempat asal | Stesen 3 (kegunaan) + Stesen 4 Peraturan 1 |
| Jangan guna "daripada" bersama kata arah | Stesen 4 (satu baris) |
| di/ke/dari ditulis terpisah (3 pasangan ✓/✗) | Stesen 4 Peraturan 2 |
| Tip pembeza: di + tempat → jarak; di + perbuatan → rapat | Stesen 4 Peraturan 2 |
| kiri/kanan bersama "sebelah" | Stesen 2 (ayat 7–8) |
| antara … dengan (bukan "dan") | Stesen 4 Peraturan 4 |
| Letakkan nama benda/tempat selepas kata arah | Stesen 4 Peraturan 3 |
| BM standard DBP | Semua skrip; semakan akhir Fasa 5 |

## 6. Sampel suara — `sampel-suara/`

| Fail | Suara | Tetapan |
|---|---|---|
| `1_pencerita_yasmin.mp3` | ms-MY-YasminNeural (perempuan) | kadar -10% |
| `2_pencerita_osman.mp3` | ms-MY-OsmanNeural (lelaki) | kadar -10% |
| `3_aira_yasmin.mp3` | Yasmin, pic dinaikkan sedikit supaya berbeza daripada pencerita | kadar -5% |
| `4_gogo_osman_comel.mp3` | Osman, pic dinaikkan dengan FFmpeg (comel) | kadar -5% |

Nota: kadar -10% agak perlahan (~1.6 patah perkataan sesaat). Jika guru setuju, -5% membantu video muat 3 minit.

## 7. Keputusan yang diperlukan daripada guru

1. Reka bentuk 6 bingkai: lulus / perlu ubah?
2. Pencerita: Yasmin (perempuan) atau Osman (lelaki)? Suara Aira dan Gogo: sesuai?
3. Kadar bacaan: -10% atau -5%?
4. Senarai pemendekan §4: setuju?
5. Cadangan kapsyen (§2): setuju?
