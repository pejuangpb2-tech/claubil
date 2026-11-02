"""Skrip video Misi Angkasa: Ekspedisi Kata Arah (sumber tunggal kebenaran).

Setiap baris: (id, penutur, teks, jeda_sebelum_s, sfx)
  penutur : N = pencerita (Osman), W = Wafiy (angkasawan), G = Gogo
  jeda_sebelum_s : masa visual sebelum suara bermula (objek bergerak, kad stesen)
  sfx     : senarai (nama, ofset) — ofset nombor = saat dari permulaan baris (negatif = sebelum suara),
            atau "w<n>[+/-s]" = pada perkataan ke-n (bermula 0) dalam baris itu
Fail suara: audio/vo/<id>.wav. Ganti fail itu dengan rakaman sendiri (nama sama),
kemudian jalankan semula tools/audio_build.py: pemasaan akan dilaras automatik.
"""

STESEN = [
    ("pembukaan", "Pembukaan"),
    ("masalah", "Masalah Gogo"),
    ("s1", "Stesen 1: Apa itu Kata Arah?"),
    ("s2", "Stesen 2: Kenali Kata Arah"),
    ("s3", "Stesen 3: Kegunaan Kata Arah"),
    ("s4", "Stesen 4: Cara Menggunakan Kata Arah"),
    ("s5", "Stesen 5: Cara Membina Ayat"),
    ("rumusan", "Rumusan"),
    ("penutup", "Penutup"),
]

LINES = [
    # ---------------- PEMBUKAAN ----------------
    ("pembukaan", [
        ("01_berlepas", "W", "Tiga, dua, satu… berlepas!", 1.2, [("rumble", 0.2), ("whoosh1", 2.0)]),
        ("02_tajuk", "N", "Selamat datang ke Misi Angkasa: Ekspedisi Kata Arah!", 1.8, [("pop1", 0.0)]),
        ("03_hari_ini", "N", "Hari ini, kita akan belajar apa itu kata arah, kegunaannya, cara menggunakannya, dan cara membina ayat. Jom!", 0.8, []),
    ]),
    # ---------------- MASALAH GOGO ----------------
    ("masalah", [
        ("04_gogo_tolong", "G", "Wafiy! Tolong! Saya ada di… di… alamak, saya tidak tahu cara hendak memberitahu!", 1.8, [("radio", -1.4)]),
        ("05_wafiy_jangan_risau", "W", "Jangan risau, Gogo! Kita belajar kata arah dahulu. Selepas itu, kamu boleh beritahu saya di mana kamu berada!", 0.5, []),
    ]),
    # ---------------- STESEN 1 ----------------
    ("s1", [
        ("06_s1_tajuk", "N", "Stesen satu. Apa itu kata arah?", 1.6, [("whoosh2", -1.5)]),
        ("07_definisi", "N", "Kata arah ialah perkataan yang menunjukkan arah atau kedudukan sesuatu benda.", 0.8, [("pop2", 0.3)]),
        ("08_kedudukan", "N", "Di mana kata arah dalam ayat? Kata arah datang selepas di, ke atau dari, dan sebelum nama benda atau tempat.", 1.0, []),
        ("09_di_atas_meja", "N", "Contohnya, di atas meja. Di ialah kata sendi nama, atas ialah kata arah, dan meja ialah nama benda.", 0.6, [("klik", "w1"), ("klik", "w2+0.15"), ("klik", "w3+0.2")]),
        ("10_kata_tugas", "N", "Kata arah ialah sejenis kata tugas.", 0.6, [("pop1", 0.0)]),
    ]),
    # ---------------- STESEN 2 ----------------
    ("s2", [
        ("11_s2_tajuk", "N", "Stesen dua. Kenali kata arah. Kita mulakan dengan pasangan berlawanan.", 1.6, [("whoosh3", -1.5)]),
        ("12_atas", "N", "Atas. Bintang berkelip di atas roket.", 1.3, [("pop1", 0.0)]),
        ("13_bawah", "N", "Bawah. Bumi kelihatan di bawah roket.", 1.3, [("pop2", 0.0)]),
        ("14_dalam", "N", "Dalam. Wafiy duduk di dalam roket.", 1.3, [("pop1", 0.0)]),
        ("15_luar", "N", "Luar. Gogo melambai di luar roket.", 1.3, [("pop2", 0.0)]),
        ("16_hadapan", "N", "Hadapan. Bulan bersinar di hadapan roket.", 1.3, [("pop1", 0.0)]),
        ("17_belakang", "N", "Belakang. Komet meluncur di belakang roket.", 1.3, [("whoosh1", -0.9), ("pop2", 0.0)]),
        ("18_tip_kiri_kanan", "N", "Untuk kiri dan kanan, kita lihat dari belakang Wafiy. Jadi, kiri dan kanan Wafiy sama dengan kiri dan kanan kamu.", 1.2, []),
        ("19_kiri", "N", "Kiri. Planet merah berada di sebelah kiri Wafiy.", 1.0, [("pop1", 0.0)]),
        ("20_kanan", "N", "Kanan. Planet biru berada di sebelah kanan Wafiy.", 1.3, [("pop2", 0.0)]),
        ("21_tepi", "N", "Tepi. Bendera dipacak di tepi kawah.", 1.3, [("klik", -0.3), ("pop1", 0.0)]),
        ("22_tengah", "N", "Tengah. Matahari berada di tengah sistem suria.", 1.3, [("pop2", 0.0)]),
        ("23_bonus", "N", "Bonus! Dua lagi kata arah.", 1.0, [("pop1", 0.0)]),
        ("24_antara", "N", "Antara. Bulan berada di antara dua bintang.", 1.3, [("pop2", 0.0)]),
        ("25_sisi", "N", "Sisi. Tangga diletakkan di sisi roket.", 1.3, [("klik", -0.3), ("pop1", 0.0)]),
        ("26_tahukah_kamu", "N", "Tahukah kamu? Utara, selatan, timur dan barat juga kata arah!", 1.0, [("pop2", 0.0)]),
        ("27_dua_belas", "N", "Hebat! Inilah dua belas kata arah yang kita kenali hari ini.", 0.8, []),
    ]),
    # ---------------- STESEN 3 ----------------
    ("s3", [
        ("28_s3_tajuk", "N", "Stesen tiga. Kegunaan kata arah.", 1.6, [("whoosh2", -1.5)]),
        ("29_guna_kedudukan", "N", "Pertama, kata arah memberitahu kedudukan benda. Di mana? Satelit berada di sebelah kanan bulan.", 0.9, [("pop1", 0.0)]),
        ("30_guna_hala_tuju", "N", "Kedua, kata arah menunjukkan hala tuju. Ke mana? Roket terbang ke atas.", 0.9, [("pop2", 0.0), ("whoosh3", "w9-0.2")]),
        ("31_guna_asal", "N", "Ketiga, kata arah memberitahu tempat asal. Dari mana? Gogo keluar dari dalam roket.", 0.9, [("pop1", 0.0)]),
        ("32_harian", "N", "Kata arah juga kita gunakan setiap hari.", 1.0, [("whoosh1", -0.9)]),
        ("33_kasut", "N", "Kasut disusun di atas rak kasut.", 0.8, [("pop2", 0.0)]),
        ("34_pisau", "N", "Pisau disimpan di dalam laci.", 0.8, [("pop1", 0.0)]),
        ("35_sekolah", "N", "Sekolah saya terletak di sebelah kiri masjid.", 0.8, [("pop2", 0.0)]),
        ("36_membantu", "N", "Kata arah membantu kita mencari barang, memberi arah jalan dan menyimpan barang dengan selamat.", 0.8, []),
    ]),
    # ---------------- STESEN 4 ----------------
    ("s4", [
        ("37_s4_tajuk", "N", "Stesen empat. Cara menggunakan kata arah.", 1.6, [("whoosh3", -1.5)]),
        ("38_peraturan1", "N", "Peraturan pertama. Kata arah yang sama membawa makna berbeza apabila digunakan dengan di, ke dan dari.", 0.8, [("pop1", 0.0)]),
        ("39_di", "N", "Di menunjukkan kedudukan. Gogo berdiri di atas batu.", 0.8, [("pop2", 0.0)]),
        ("40_ke", "N", "Ke menunjukkan hala tuju. Gogo melompat ke atas batu.", 0.8, [("pop1", 0.0), ("whoosh1", "w5-0.1")]),
        ("41_dari", "N", "Dari menunjukkan tempat asal. Gogo turun dari atas batu.", 0.8, [("pop2", 0.0), ("whoosh2", "w5-0.1")]),
        ("42_daripada", "N", "Ingat, gunakan dari untuk tempat. Jangan gunakan daripada bersama kata arah.", 0.8, []),
        ("43_peraturan2", "N", "Peraturan kedua. Di, ke dan dari ditulis terpisah daripada kata arah.", 1.0, [("laser", "w7-0.1")]),
        ("44_ejaan_betul", "N", "Lihat ejaan yang betul: di atas, ke dalam, dan dari luar. Ada jarak di antara perkataan itu.", 0.6, [("pop1", "w4"), ("pop2", "w6"), ("pop1", "w9")]),
        ("45_tip_rapat", "N", "Tetapi, di yang melekat pada perbuatan ditulis rapat, seperti diletakkan dan dimakan.", 0.8, [("klik", "w5")]),
        ("46_peraturan3", "N", "Peraturan ketiga. Letakkan nama benda atau tempat selepas kata arah.", 1.0, [("pop2", 0.0)]),
        ("47_gogo_bola", "G", "Bola itu berada di bawah… di bawah apa?", 0.6, []),
        ("48_bola_meja", "N", "Bola itu berada di bawah meja. Barulah ayat itu jelas dan lengkap.", 0.5, [("pop1", 0.0)]),
        ("49_peraturan4", "N", "Peraturan keempat. Apabila menyebut dua benda, gunakan antara bersama perkataan dengan.", 1.0, [("pop2", 0.0)]),
        ("50_antara_dengan", "N", "Bulan berada di antara roket dengan planet. Guna dengan, bukan dan.", 0.6, []),
    ]),
    # ---------------- STESEN 5 ----------------
    ("s5", [
        ("51_s5_tajuk", "N", "Stesen lima. Cara membina ayat.", 1.6, [("whoosh1", -1.5)]),
        ("52_formula", "N", "Inilah formula ayat kita. Siapa atau apa, buat apa, di, ke atau dari, kata arah, dan nama benda atau tempat.", 0.8, [("klik", "w4"), ("klik", "w7"), ("klik", "w9"), ("klik", "w13"), ("klik", "w16")]),
        ("53_contoh1", "N", "Wafiy duduk di dalam roket.", 1.6, [("klik", -1.4), ("klik", -1.1), ("klik", -0.8), ("klik", -0.5), ("klik", -0.2)]),
        ("54_contoh2", "N", "Gogo melompat ke atas batu.", 1.6, [("klik", -1.4), ("klik", -1.1), ("klik", -0.8), ("klik", -0.5), ("klik", -0.2)]),
        ("55_contoh3", "N", "Komet datang dari belakang planet.", 1.6, [("klik", -1.4), ("klik", -1.1), ("klik", -0.8), ("klik", -0.5), ("klik", -0.2)]),
        ("56_lihat_cara", "N", "Sekarang, lihat cara saya membina ayat berdasarkan gambar.", 1.0, []),
        ("57_think_aloud", "N", "Apa dalam gambar? Satelit. Apa yang ia buat? Berputar. Di mana? Di sisi bulan.", 0.8, [("klik", "w3"), ("klik", "w8"), ("klik", "w11")]),
        ("58_ayat_lengkap", "N", "Ayat lengkapnya: Satelit berputar di sisi bulan.", 0.4, [("pop1", 0.0)]),
        ("59_tip_ayat", "N", "Tip ayat hebat! Mulakan dengan huruf besar. Pilih kata arah yang tepat. Akhiri dengan noktah.", 1.0, [("pop2", "w3"), ("pop1", "w7"), ("pop2", "w12")]),
        ("60_gogo_tahu", "G", "Wafiy! Sekarang saya tahu! Saya bersembunyi di belakang batu besar!", 1.4, [("radio", -1.2), ("klik", "w4"), ("klik", "w5"), ("klik", "w6"), ("klik", "w7"), ("klik", "w8")]),
        ("61_wafiy_datang", "W", "Saya nampak kamu, Gogo! Saya datang!", 0.5, [("whoosh2", "w5-0.2")]),
        ("62_gogo_terima_kasih", "G", "Terima kasih, Wafiy!", 1.8, [("fanfare", -0.6)]),
    ]),
    # ---------------- RUMUSAN ----------------
    ("rumusan", [
        ("63_rumusan", "N", "Mari kita rumuskan.", 1.4, [("whoosh3", -1.3)]),
        ("64_poin1", "N", "Satu. Kata arah menunjukkan arah atau kedudukan.", 0.5, [("pop1", 0.0)]),
        ("65_poin2", "N", "Dua. Kata arah datang selepas di, ke atau dari, dan sebelum nama benda atau tempat.", 0.5, [("pop2", 0.0)]),
        ("66_poin3", "N", "Tiga. Di untuk kedudukan, ke untuk hala tuju, dan dari untuk tempat asal.", 0.5, [("pop1", 0.0)]),
        ("67_poin4", "N", "Empat. Di, ke dan dari ditulis terpisah.", 0.5, [("pop2", 0.0)]),
        ("68_chant_ajak", "N", "Jom sebut bersama!", 0.8, []),
    ]),
    # chant diletakkan pada rentak muzik oleh audio_build.py
    # ---------------- PENUTUP ----------------
    ("penutup", [
        ("80_syabas", "N", "Syabas! Sekarang kamu sudah tahu tentang kata arah. Teruskan misi kamu di Zon Cabaran. Jumpa lagi!", 1.4, [("fanfare", -1.2)]),
        ("81_jumpa_lagi", "W", "Jumpa lagi!", 0.3, [("whoosh1", 1.2)]),
    ]),
]

# Chant: setiap perkataan dirakam berasingan dan diletakkan pada rentak muzik (2 rentak sepatah).
CHANT = ["Atas", "bawah", "dalam", "luar", "hadapan", "belakang", None,
         "Kiri", "kanan", "tepi", "tengah", "antara", "sisi", None]
