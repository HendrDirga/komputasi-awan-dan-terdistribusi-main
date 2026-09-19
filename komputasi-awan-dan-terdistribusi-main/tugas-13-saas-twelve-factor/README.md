# Tugas 13 (Pekan 13) — SaaS & Twelve-Factor App

**Materi terkait:** Software as a Service (SaaS), Twelve-Factor App Methodology.

## Studi Kasus

Aplikasi SaaS sering **rusak saat dipindahkan** dari laptop developer ke lingkungan produksi ("kerja di laptop saya, kok di server error?"). Penyebab paling umum: konfigurasi hardcoded, dependency tidak terkunci versinya, dan asumsi lingkungan lokal yang tidak berlaku di server.

## Tugas Kelompok

Di folder `app/` disediakan **aplikasi contoh yang sengaja melanggar beberapa prinsip Twelve-Factor App** (`bad_app.py`). Tugas kalian:

1. **Audit** — temukan dan catat pelanggaran terhadap 3 faktor berikut (fokus tugas ini, sesuai arahan materi):
   - **Factor I — Codebase**: satu codebase yang dilacak di version control, banyak deploy.
   - **Factor II — Dependencies**: deklarasikan & isolasi dependency secara eksplisit, jangan asumsikan package "sudah pasti ada" di sistem.
   - **Factor III — Config**: simpan konfigurasi (kredensial, endpoint, feature flag) di **environment variable**, bukan hardcoded di kode.
2. **Perbaiki** `bad_app.py` menjadi versi yang sesuai Twelve-Factor App — simpan versi perbaikan sebagai `app/fixed_app.py` (biarkan `bad_app.py` apa adanya sebagai bukti "before").
3. Tulis **laporan audit** (gunakan [`AUDIT-TEMPLATE.md`](AUDIT-TEMPLATE.md)) yang memetakan tiap pelanggaran ke perbaikannya.

## Petunjuk yang Harus Dicari di `bad_app.py`

Tanpa memberi tahu semua jawabannya (kalian yang harus menemukan), berikut kategori masalah yang perlu diwaspadai:
- Kredensial atau URL database yang ditulis langsung di kode.
- Dependency yang diimpor tapi tidak dicantumkan versinya di manapun (atau tidak ada `requirements.txt` sama sekali).
- Asumsi path file lokal (mis. `/Users/nama-developer/...`) yang tidak akan ada di server lain.

## Struktur Submission

```
tugas-13-saas-twelve-factor/
├── README.md          # Ringkasan hasil audit
├── AUDIT-TEMPLATE.md   # Isi dan simpan sebagai laporan audit
├── JURNAL.md
├── app/
│   ├── bad_app.py      # JANGAN diubah - bukti "before"
│   ├── fixed_app.py     # Versi perbaikan kalian
│   └── requirements.txt # Dependency dengan versi terkunci (bagian dari perbaikan)
└── bukti/
```

## Rubrik Penilaian (Tugas 13)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Kelengkapan temuan audit | 30% | Semua pelanggaran utama di 3 faktor (Codebase, Dependencies, Config) ditemukan |
| Kualitas perbaikan (`fixed_app.py`) | 35% | Config lewat env var, dependency terkunci versi, tidak ada path hardcoded |
| Kejelasan laporan audit | 20% | Pemetaan pelanggaran → perbaikan jelas dan spesifik |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya ke AI daftar 12 faktor secara umum untuk orientasi; **tidak boleh** meminta AI menemukan pelanggaran di `bad_app.py` atau menuliskan isi `fixed_app.py` untuk kalian. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- `AUDIT-TEMPLATE.md` wajib menjelaskan **kenapa** menyimpan config di environment variable lebih baik daripada hardcoded — termasuk skenario konkret yang bisa gagal jika prinsip ini dilanggar (mis. kredensial ter-commit ke repo publik — akan dibahas lebih dalam di Tugas 14).
