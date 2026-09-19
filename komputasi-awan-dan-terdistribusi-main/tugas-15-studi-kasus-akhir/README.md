# Tugas 15 (Pekan 15) — Studi Kasus Akhir: Prototipe "Smart City"

**Materi terkait:** Integrasi Sistem Terdistribusi + Komputasi Awan (proyek akhir).

## Studi Kasus

Bangun prototipe sederhana sistem **Smart City**: banyak **sensor** (simulasi lampu jalan pintar, sensor kualitas udara, sensor parkir, dll.) mengirim data secara berkala, dan data tersebut harus **disimpan di penyimpanan mirip-cloud** agar bisa diakses dashboard kota nanti.

Ini proyek **integrasi**: kalian **wajib menggabungkan minimal satu konsep dari Bagian 1 (Tugas 1–7)** ke dalam infrastruktur ala-cloud (konsep dari Tugas 9–14), dalam satu repositori yang rapi.

## Arsitektur Default yang Disediakan

Skeleton di repo ini memakai kombinasi berikut (kalian **boleh menggantinya** dengan konsep lain dari Tugas 1-7, jelaskan alasannya di README jika berbeda dari default):

- **Message Queue (konsep Tugas 4)** — sensor mem-publish data ke RabbitMQ lokal (via Docker), bukan menulis langsung ke storage (supaya sensor tetap bisa "mengirim" walau storage sedang sibuk/restart — *asynchronous decoupling*).
- **MinIO (S3-compatible object storage, lokal via Docker)** sebagai simulasi **cloud storage** — MinIO adalah software open-source gratis yang menyediakan API yang sama seperti Amazon S3, tapi jalan 100% di laptop kalian, tanpa akun cloud apa pun.

```
[Sensor 1] --\
[Sensor 2] ---> [RabbitMQ (broker lokal)] --> [Processor] --> [MinIO (storage lokal, S3-compatible)]
[Sensor N] --/
```

### Konsep Alternatif yang Bisa Kalian Pilih (Ganti Message Queue)

Jika kelompok ingin mengintegrasikan konsep lain sebagai pengganti Message Queue, misalnya:
- **Bully Algorithm (Tugas 5)**: beberapa "gateway" sensor bersaing menjadi koordinator yang mengumpulkan data sebelum dikirim ke storage.
- **DHT/Chord (Tugas 6)**: memetakan `sensor_id` ke node gateway mana yang bertanggung jawab menampungnya.
- **Consistency (Tugas 7)**: dua region storage (mis. "Jakarta" dan "Bandung" MinIO) dengan strategi konsistensi tertentu.

Silakan pilih salah satu dan jelaskan kenapa di `README.md` — yang penting **ada satu konsep sistem terdistribusi yang benar-benar terlihat bekerja**, bukan cuma disebut di teks.

## Yang Disediakan di Skeleton

- `docker-compose.yml` — menjalankan RabbitMQ + MinIO lokal.
- `sensors/sensor_publisher.py` — skeleton simulasi beberapa sensor (thread berbeda) mengirim data periodik ke RabbitMQ.
- `processor/consumer_to_storage.py` — skeleton yang subscribe ke RabbitMQ dan menyimpan tiap data sensor sebagai object JSON ke bucket MinIO.

### Cara Menjalankan

```bash
docker compose up -d          # jalankan RabbitMQ + MinIO
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

python3 processor/consumer_to_storage.py    # terminal 1
python3 sensors/sensor_publisher.py         # terminal 2
```

Dashboard MinIO (lihat object yang tersimpan): `http://localhost:9001` (login default `minioadmin`/`minioadmin`).
Dashboard RabbitMQ: `http://localhost:15672` (login default `guest`/`guest`).

## Tugas Kelompok

1. Lengkapi semua `# TODO` di skeleton (atau ganti dengan implementasi konsep alternatif pilihan kalian).
2. Jalankan sistem end-to-end, buktikan data sensor benar-benar tersimpan di MinIO (screenshot dashboard MinIO menunjukkan object baru muncul, atau list via `mc`/API).
3. Simulasikan **satu skenario gangguan** (mis. matikan `consumer_to_storage.py` sementara sensor tetap mengirim, lalu nyalakan lagi — buktikan data tidak hilang karena tertampung di antrean RabbitMQ) — ini adalah pembuktian nyata konsep *asynchronous decoupling* yang dipelajari sejak Tugas 4.
4. Tulis laporan akhir di `README.md`: arsitektur final (diagram Mermaid), konsep sistem terdistribusi yang diintegrasikan dan kenapa, serta refleksi menyeluruh — apa yang paling sulit sepanjang semester, dan bagaimana 15 tugas ini saling terhubung membentuk pemahaman utuh.

## Struktur Submission

```
tugas-15-studi-kasus-akhir/
├── README.md              # Laporan akhir + diagram arsitektur final
├── JURNAL.md
├── docker-compose.yml
├── requirements.txt
├── sensors/
│   └── sensor_publisher.py
├── processor/
│   └── consumer_to_storage.py
└── bukti/                  # Screenshot dashboard MinIO/RabbitMQ, log skenario gangguan
```

## Rubrik Penilaian (Tugas 15)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Sistem end-to-end berjalan | 30% | Data sensor benar-benar sampai dan tersimpan di storage |
| Integrasi konsep sistem terdistribusi (Tugas 1-7) | 25% | Konsep benar-benar terlihat bekerja (dibuktikan lewat skenario gangguan), bukan sekadar disebut |
| Kualitas arsitektur & laporan akhir | 25% | Diagram jelas, keputusan desain dijustifikasi |
| Refleksi & proses sepanjang semester | 10% | Menunjukkan pemahaman kumulatif, bukan cuma tugas ini saja |
| Proses & kontribusi kelompok | 10% | `JURNAL.md`, commit history konsisten sepanjang pengerjaan |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya ke AI opsi konsep sistem terdistribusi mana yang cocok diintegrasikan untuk brainstorming; **tidak boleh** meminta AI menuliskan isi `# TODO` di `sensor_publisher.py`/`consumer_to_storage.py` atau laporan akhir. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- Karena ini proyek akhir, video demo di `bukti/` wajib lebih lengkap dari tugas lain: tunjukkan sistem berjalan end-to-end, lalu jalankan skenario gangguan (mis. matikan salah satu komponen) secara langsung dalam rekaman yang sama — bukan potongan klip terpisah yang bisa disunting untuk menyembunyikan kegagalan.
