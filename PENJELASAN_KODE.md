# Penjelasan Kode Proyek SISTER2

Dokumen ini merangkum struktur kode, isi file penting, dan fungsi singkat tiap file.

## File Utama

1. `simulator.py`
   Isi: kelas utama `DistributedCommSimulator`, UI Tkinter, loop simulasi, animasi paket, log, dan metrik perbandingan.
   Fungsi: menjalankan seluruh aplikasi simulasi dari awal sampai akhir.

2. `README.md`
   Isi: ringkasan project, cara menjalankan, kontrol simulasi, dan preview GIF.
   Fungsi: dokumentasi utama untuk dosen dan pengunjung repo.

3. `.gitignore`
   Isi: daftar file/folder yang tidak perlu masuk Git (misalnya `.venv`, `__pycache__`, `*.pyc`).
   Fungsi: menjaga repo tetap bersih dari file sementara.

## Folder Model

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

## Folder Media Demo

1. `docs/assets/requestresponse.gif`
   Isi: animasi demo model Request-Response.
   Fungsi: bukti visual alur request dan response.

2. `docs/assets/publishsubscribe.gif`
   Isi: animasi demo model Publish-Subscribe.
   Fungsi: bukti visual fanout dari publisher ke banyak subscriber.

3. `docs/assets/messagepassing.gif`
   Isi: animasi demo model Message Passing.
   Fungsi: bukti visual alur pesan bertahap antar komponen.

## File Sisa Versi Web (Tidak Dipakai pada Demo Python)

1. `index.html`
   Isi: kerangka antarmuka versi web.
   Fungsi: jejak versi awal berbasis web (tidak dipakai pada simulasi Tkinter saat ini).

2. `style.css`
   Isi: styling untuk versi web.
   Fungsi: pasangan dari `index.html` (tidak dipakai pada simulasi Tkinter saat ini).

## Folder Sistem/Tooling

1. `.git/`
   Isi: metadata repository Git.
   Fungsi: menyimpan riwayat commit, branch, dan konfigurasi version control.

2. `.venv/`
   Isi: environment Python lokal.
   Fungsi: menyimpan dependency environment lokal proyek.

3. `__pycache__/`
   Isi: bytecode cache Python.
   Fungsi: cache otomatis saat file Python dieksekusi.
