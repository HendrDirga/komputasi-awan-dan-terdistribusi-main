# Tugas 12 (Pekan 12) — Implementasi PaaS

**Materi terkait:** Platform as a Service (PaaS).

## Studi Kasus

Pengembang FoodGo ingin fokus menulis **kode aplikasi Python** tanpa mau mengurus sistem operasi server, *patching* keamanan, atau konfigurasi web server — inilah nilai jual utama PaaS dibanding IaaS (Tugas 11).

## Catatan Biaya (Baca Sebelum Mulai)

Berbeda dari tugas lain di repo ini, tugas ini **memang perlu mendaftar akun** di penyedia PaaS — tapi tetap **gratis, tanpa tagihan**, selama kalian pakai tingkatan *free tier* dan tidak memasukkan data kartu pembayaran ke fitur berbayar. Rekomendasi platform yang **tidak meminta kartu kredit sama sekali** untuk tier gratis:

- **[Render](https://render.com/)** — free tier "Web Service", cukup daftar pakai akun GitHub, tidak perlu kartu kredit.
- **[PythonAnywhere](https://www.pythonanywhere.com/)** — free tier "Beginner", tidak perlu kartu kredit.

Jika kelompok kalian ingin coba platform lain (Railway, Fly.io, dll.) yang mungkin meminta verifikasi kartu, itu **pilihan opsional dan risiko kalian sendiri** — pastikan paham batas *free tier*-nya dan set budget alert, jangan sampai tertagih. Dosen **tidak mewajibkan** platform yang meminta kartu kredit.

## Tugas Kelompok

1. Gunakan skeleton aplikasi web sederhana di `app/app.py` (Flask) — lengkapi TODO agar aplikasi menampilkan info dasar (mis. nama kelompok, waktu server, dan endpoint `/health`).
2. **Uji lokal dulu** sebelum deploy:
   ```bash
   cd app
   python3 -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   python3 app.py
   # buka http://localhost:5000
   ```
3. Deploy ke platform PaaS pilihan kalian (ikuti tutorial resmi platform tsb — umumnya: hubungkan repo GitHub kalian, platform otomatis build & jalankan tanpa kalian mengatur OS/web server).
4. Catat **link aplikasi yang aktif** (URL publik) di `README.md`.
5. Tulis analisis: apa saja yang **tidak perlu kalian urus sendiri** dibanding jika ini dideploy manual sebagai IaaS di Tugas 11 (mis. OS patching, instalasi web server, konfigurasi port, TLS/HTTPS otomatis).

## Analisis yang Wajib Ditulis di `README.md`

1. Link aplikasi yang aktif + screenshot aplikasi diakses dari browser.
2. Tabel perbandingan **tanggung jawab kalian vs tanggung jawab platform** (kaitkan ke *Shared Responsibility* yang akan dibahas lebih dalam di Tugas 14).
3. Apa yang terjadi jika aplikasi kalian butuh **library sistem operasi khusus** yang tidak didukung platform PaaS (mis. driver khusus) — jelaskan kapan justru IaaS/kontainer custom (Tugas 11) lebih tepat dibanding PaaS.

## Struktur Submission

```
tugas-12-implementasi-paas/
├── README.md      # Link aplikasi aktif + analisis
├── JURNAL.md       # Kendala saat deploy (error build, dsb)
├── app/
│   ├── app.py
│   └── requirements.txt
└── bukti/          # Screenshot aplikasi live + dashboard platform PaaS
```

## Rubrik Penilaian (Tugas 12)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Aplikasi berhasil di-deploy & aktif | 40% | Link diakses dosen/asisten dan benar-benar berfungsi saat penilaian |
| Analisis tanggung jawab PaaS vs IaaS | 30% | Perbandingan konkret, bukan definisi umum |
| Bukti proses deploy | 15% | Screenshot dashboard platform, log build |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya ke AI langkah umum deploy ke platform PaaS untuk orientasi awal; **tidak boleh** meminta AI menuliskan isi `# TODO` di `app/app.py` atau menuliskan analisis akhir tanggung jawab PaaS vs IaaS. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- Karena hasil akhirnya adalah link publik yang bisa dicek langsung, dosen/asisten akan mengakses aplikasi kalian **secara langsung saat penilaian** — pastikan tetap aktif (tidak di-sleep karena tidak dipakai lama, atau kalian tahu cara membangunkannya) sampai jadwal penilaian selesai.
- `JURNAL.md` wajib mencatat langkah konfigurasi apa saja yang dilakukan di dashboard platform (bukan cuma "klik deploy") beserta screenshot tiap langkah penting di `bukti/`.
