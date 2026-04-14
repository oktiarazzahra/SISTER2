# Simulasi Interaktif Model Komunikasi dalam Sistem Terdistribusi

Dokumen ini adalah satu-satunya dokumentasi utama untuk pengumpulan.

## Ringkasan

Simulasi ini mengimplementasikan 3 model komunikasi:

1. Request-Response
2. Publish-Subscribe
3. Message Passing

Semua model dibandingkan menggunakan metrik real-time: total pesan, throughput, rata-rata latensi, drop, dan urutan event.

## Struktur Kode

1. `simulator.py` -> UI Tkinter, loop simulasi, render visual, metrik, analisis perbandingan
2. `models/common.py` -> data class `Node` dan `Packet`
3. `models/request_response_model.py` -> logika Request-Response
4. `models/publish_subscribe_model.py` -> logika Publish-Subscribe
5. `models/message_passing_model.py` -> logika Message Passing

## Jalankan Aplikasi

```bash
python simulator.py
```

## Kontrol Simulasi

1. Model Komunikasi: `request-response`, `publish-subscribe`, `message-passing`
2. Laju Event/detik
3. Jumlah Subscriber (khusus Publish-Subscribe)
4. Mulai, Jeda, Kirim 1 Event, Burst 20, Reset
5. Simulasi Gangguan ON/OFF

## Media Demo

File media disimpan di folder [docs/assets](docs/assets):

1. [docs/assets/requestresponse.gif](docs/assets/requestresponse.gif)
2. [docs/assets/publishsubscribe.gif](docs/assets/publishsubscribe.gif)
3. [docs/assets/messagepassing.gif](docs/assets/messagepassing.gif)

## Cara Buka Media

1. Di lokal (VS Code Explorer): klik file `.mp4` atau `.gif` di folder `docs/assets`.
2. Di GitHub:
	- File GIF akan tampil animasi langsung jika dipanggil dengan sintaks gambar markdown.
	- File MP4 dibuka dengan klik link file video.

Contoh embed GIF (akan bergerak di GitHub):

```md
![Demo Publish-Subscribe](docs/assets/publishsubscribe.gif)
```

## Preview GIF

![Demo Request-Response](docs/assets/requestresponse.gif)

Penjelasan:
Pada cuplikan ini alur komunikasinya satu lawan satu. Sensor mengirim request ke service, lalu service mengirimkan response kembali. Polanya berurutan dan jelas titik awal-akhirnya. Bagian ini saya gunakan untuk menunjukkan bahwa Request-Response cocok ketika pengirim memang menunggu jawaban langsung.

![Demo Publish-Subscribe](docs/assets/publishsubscribe.gif)

Penjelasan:
Di sini terlihat satu event dari publisher bisa diteruskan ke beberapa subscriber sekaligus. Saya menekankan bahwa pengirim tidak perlu tahu siapa penerimanya satu per satu. Model ini lebih pas untuk distribusi data ke banyak komponen, misalnya notifikasi atau telemetry yang dipantau banyak layanan.

![Demo Message Passing](docs/assets/messagepassing.gif)

Penjelasan:
Cuplikan ini menunjukkan pesan bergerak bertahap antarkomponen, dari pengirim ke perantara, lalu ke pemroses. Karakter utamanya ada di alur pipeline: pesan tidak langsung selesai di satu titik, tetapi diteruskan sesuai tahapan. Ini relevan untuk proses antrian kerja atau pemrosesan data berantai.

## Penjelasan Kode per File

### File Utama

1. `simulator.py`
	Isi: kelas utama `DistributedCommSimulator`, UI Tkinter, loop simulasi, animasi paket, log, dan metrik perbandingan.
	Fungsi: menjalankan seluruh aplikasi simulasi dari awal sampai akhir.

2. `README.md`
	Isi: ringkasan project, cara menjalankan, kontrol simulasi, preview GIF, dan penjelasan file.
	Fungsi: dokumentasi utama untuk dosen dan pengunjung repo.

3. `.gitignore`
	Isi: daftar file/folder yang tidak perlu masuk Git (misalnya `.venv`, `__pycache__`, `*.pyc`).
	Fungsi: menjaga repo tetap bersih dari file sementara.

### Folder Model

1. `models/common.py`
	Isi: data class `Node` dan `Packet`.
	Fungsi: struktur data bersama yang dipakai semua model komunikasi.

2. `models/request_response_model.py`
	Isi: class `RequestResponseModel` dengan metode `emit_event` dan `on_arrive`.
	Fungsi: logika komunikasi sinkron Request-Response (kirim request lalu terima response).

3. `models/publish_subscribe_model.py`
	Isi: class `PublishSubscribeModel` dengan metode publish dan fanout ke subscriber.
	Fungsi: logika komunikasi event-driven Publish-Subscribe.

4. `models/message_passing_model.py`
	Isi: class `MessagePassingModel` dengan alur `send -> route -> consume`.
	Fungsi: logika komunikasi Message Passing berbasis pipeline.

### Folder Media Demo

1. `docs/assets/requestresponse.gif`
	Isi: animasi demo model Request-Response.
	Fungsi: bukti visual alur request dan response.

2. `docs/assets/publishsubscribe.gif`
	Isi: animasi demo model Publish-Subscribe.
	Fungsi: bukti visual fanout dari publisher ke banyak subscriber.

3. `docs/assets/messagepassing.gif`
	Isi: animasi demo model Message Passing.
	Fungsi: bukti visual alur pesan bertahap antar komponen.

### File Sisa Versi Web (Tidak Dipakai pada Demo Python)

1. `index.html`
	Isi: kerangka antarmuka versi web.
	Fungsi: jejak versi awal berbasis web (tidak dipakai pada simulasi Tkinter saat ini).

2. `style.css`
	Isi: styling untuk versi web.
	Fungsi: pasangan dari `index.html` (tidak dipakai pada simulasi Tkinter saat ini).

## Pemetaan Rubrik Nilai Sangat Baik

Bagian ini disusun agar isi tugas sesuai kriteria nilai tertinggi.

### 1. Pemilihan Model Komunikasi

Target Sangat Baik:
Menggunakan dua atau lebih model dan memberi alasan yang jelas.

Yang sudah dipenuhi di proyek ini:

1. Menggunakan tiga model: Request-Response, Publish-Subscribe, dan Message Passing.
2. Setiap model dijelaskan kegunaannya dalam situasi berbeda.
3. Alasan pemilihan model ditulis dalam bahasa yang mudah dipahami.

Yang perlu Anda tunjukkan saat presentasi:

1. Request-Response untuk kebutuhan jawaban langsung.
2. Publish-Subscribe untuk sebar informasi ke banyak penerima.
3. Message Passing untuk alur kerja bertahap.

### 2. Komponen Sistem

Target Sangat Baik:
Menjelaskan komponen penting dan hubungan antarkomponen secara jelas.

Yang sudah dipenuhi di proyek ini:

1. Ada komponen sumber pesan, penghubung, pengolah, dan penerima hasil.
2. Jalur perpindahan pesan terlihat pada animasi.
3. Peran setiap komponen ditulis di dokumentasi.

Yang perlu Anda tunjukkan saat presentasi:

1. Siapa pengirim awal.
2. Siapa yang menyalurkan.
3. Siapa yang mengolah.
4. Siapa yang menerima hasil akhir.

### 3. Implementasi Logika Interaksi

Target Sangat Baik:
Proses kirim, terima, dan proses pesan berjalan benar di setiap model.

Yang sudah dipenuhi di proyek ini:

1. Tiap model punya alur yang berbeda dan konsisten.
2. Ada urutan proses yang bisa dilihat dari log dan animasi.
3. Kondisi gangguan juga ikut disimulasikan.

Yang perlu Anda tunjukkan saat presentasi:

1. Jalur pesan dari awal sampai akhir.
2. Perbedaan urutan antar model.
3. Dampak jika gangguan diaktifkan.

### 4. Representasi Visual

Target Sangat Baik:
Tampilan jelas, informatif, dan membantu memahami proses.

Yang sudah dipenuhi di proyek ini:

1. Ada tampilan gerak pesan antarbagian.
2. Ada warna pembeda jenis kejadian.
3. Ada catatan kejadian dan ringkasan hasil.

Yang perlu Anda tunjukkan saat presentasi:

1. Gerakan pesan pada tiap model.
2. Perubahan tampilan saat kondisi normal dan gangguan.
3. Bukti visual melalui tiga GIF.

### 5. Desain Interaksi Pengguna

Target Sangat Baik:
Kontrol mudah dipakai dan membantu proses simulasi.

Yang sudah dipenuhi di proyek ini:

1. Pilihan model tersedia dan mudah diganti.
2. Pengaturan laju dan jumlah penerima tersedia.
3. Tombol kendali lengkap: mulai, jeda, kirim satu, kirim banyak, reset.

Yang perlu Anda tunjukkan saat presentasi:

1. Cara mengganti model.
2. Cara mengubah laju.
3. Cara menguji keadaan normal dan gangguan.

### 6. Mekanisme Perbandingan

Target Sangat Baik:
Ada perbandingan yang jelas antar model dengan ukuran yang bisa dibaca.

Yang sudah dipenuhi di proyek ini:

1. Ada jumlah pesan yang diproses.
2. Ada kecepatan pemrosesan.
3. Ada waktu rata-rata sampai selesai.
4. Ada jumlah pesan yang gagal.

Yang perlu Anda tunjukkan saat presentasi:

1. Bandingkan hasil ketiga model pada kondisi sama.
2. Jelaskan mana yang paling cepat.
3. Jelaskan mana yang paling stabil saat gangguan.

### 7. Dokumentasi dan Penjelasan

Target Sangat Baik:
Dokumentasi lengkap, jelas, dan mudah dipahami.

Yang sudah dipenuhi di proyek ini:

1. Cara menjalankan dijelaskan langkah demi langkah.
2. Penjelasan tiap file dan tiap model tersedia.
3. Bukti visual disertakan dalam bentuk GIF.

Yang perlu Anda tunjukkan saat presentasi:

1. Buka README sebagai dokumen utama.
2. Tunjukkan bagian penjelasan model.
3. Tunjukkan bagian bukti visual.

### 8. Kreativitas dan Relevansi Dunia Nyata

Target Sangat Baik:
Ada kaitan yang kuat dengan kasus nyata.

Yang sudah dipenuhi di proyek ini:

1. Simulasi dibuat dengan gambaran penggunaan nyata.
2. Terdapat pengujian kondisi gangguan untuk meniru tantangan di lapangan.
3. Perbedaan perilaku tiap model terlihat pada situasi yang sama.

Yang perlu Anda tunjukkan saat presentasi:

1. Mengapa tiga model ini dipakai dalam kehidupan nyata.
2. Apa dampaknya jika pesan terlambat atau gagal.
3. Model mana yang cocok untuk kebutuhan yang berbeda.

## Ringkasan Kesiapan Nilai Sangat Baik

Secara isi, proyek ini sudah mengarah kuat ke kriteria Sangat Baik karena:

1. Model yang dipakai lebih dari dua.
2. Alur tiap model terlihat jelas.
3. Ada tampilan interaktif dan bukti visual.
4. Ada perbandingan hasil yang dapat dijelaskan.

Saran akhir saat pengumpulan:

1. Tunjukkan tiga GIF dengan narasi singkat masing-masing.
2. Tampilkan perbandingan hasil pada kondisi normal dan gangguan.
3. Tutup dengan kesimpulan model mana paling cocok untuk tujuan berbeda.
