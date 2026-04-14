# Simulasi Interaktif Model Komunikasi dalam Sistem Terdistribusi

Dokumen ini adalah satu-satunya dokumentasi utama untuk pengumpulan.

## Ringkasan

Simulasi ini mengimplementasikan 4 model komunikasi:

1. Request-Response
2. Publish-Subscribe
3. Message Passing
4. Remote Procedure Call (RPC)

Semua model dibandingkan menggunakan metrik real-time: total pesan, throughput, rata-rata latensi, drop, dan urutan event.

## Struktur Kode

1. `simulator.py` -> UI Tkinter, loop simulasi, render visual, metrik, analisis perbandingan
2. `models/common.py` -> data class `Node` dan `Packet`
3. `models/request_response_model.py` -> logika Request-Response
4. `models/publish_subscribe_model.py` -> logika Publish-Subscribe
5. `models/message_passing_model.py` -> logika Message Passing
6. `models/rpc_model.py` -> logika RPC

## Jalankan Aplikasi

```bash
python simulator.py
```

## Kontrol Simulasi

1. Model Komunikasi: `request-response`, `publish-subscribe`, `message-passing`, `rpc`
2. Laju Event/detik
3. Jumlah Subscriber (khusus Publish-Subscribe)
4. Mulai, Jeda, Kirim 1 Event, Burst 20, Reset
5. Simulasi Gangguan ON/OFF

## Media Demo

File media disimpan di folder [docs/assets](docs/assets):

1. [docs/assets/requestresponse.mp4](docs/assets/requestresponse.mp4)
2. [docs/assets/publishsubscribe.mp4](docs/assets/publishsubscribe.mp4)
3. [docs/assets/messagepassing.mp4](docs/assets/messagepassing.mp4)
4. [docs/assets/rpc.mp4](docs/assets/rpc.mp4)
5. [docs/assets/demo-request-response.gif](docs/assets/demo-request-response.gif)
6. [docs/assets/demo-publish-subscribe.gif](docs/assets/demo-publish-subscribe.gif)
7. [docs/assets/demo-message-passing.gif](docs/assets/demo-message-passing.gif)
8. [docs/assets/demo-rpc.gif](docs/assets/demo-rpc.gif)

## Cara Buka Media

1. Di lokal (VS Code Explorer): klik file `.mp4` atau `.gif` di folder `docs/assets`.
2. Di GitHub:
	- File GIF akan tampil animasi langsung jika dipanggil dengan sintaks gambar markdown.
	- File MP4 dibuka dengan klik link file video.

Contoh embed GIF (akan bergerak di GitHub):

```md
![Demo Publish-Subscribe](docs/assets/demo-publish-subscribe.gif)
```

Contoh link MP4:

```md
[Lihat video Request-Response](docs/assets/requestresponse.mp4)
```
