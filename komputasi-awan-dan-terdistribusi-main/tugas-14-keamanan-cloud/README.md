# Tugas 14 (Pekan 14) — Keamanan Cloud

**Materi terkait:** Shared Responsibility Model, Identity & Access Management (IAM).

## Studi Kasus

Terjadi kebocoran data karena *access key* cloud (kredensial API) **ter-commit ke repositori GitHub publik**. Ini salah satu insiden keamanan cloud paling umum — bot pemindai otomatis di internet menemukan kredensial semacam ini **dalam hitungan menit** setelah ter-push ke repo publik.

## Tugas Kelompok

### Bagian 1 — Scan Repositori Sendiri (Wajib, Gratis, Cukup Laptop)

Gunakan **[Gitleaks](https://github.com/gitleaks/gitleaks)** (tool open-source gratis, jalan sepenuhnya lokal, tidak mengirim data kalian ke server manapun) untuk memindai **seluruh riwayat commit** repo fork kalian, mencari kredensial yang mungkin pernah ter-commit (termasuk dari tugas-tugas sebelumnya).

Instalasi (pilih sesuai OS, semua gratis):
```bash
# Mac (Homebrew)
brew install gitleaks

# Linux/Windows: download binary dari https://github.com/gitleaks/gitleaks/releases
```

Jalankan dari root repo kalian:
```bash
gitleaks detect --source . --verbose --report-path tugas-14-keamanan-cloud/bukti/gitleaks-report.json
```

- Jika ditemukan kredensial (termasuk yang sengaja dibuat contoh di Tugas 13 `bad_app.py` — itu memang ditaruh di sana **sebagai bahan latihan**, bukan kredensial asli), dokumentasikan temuannya.
- Simpan laporan (`gitleaks-report.json`) di folder `bukti/`.

### Bagian 2 — Praktik GitHub Secrets

1. Buat **GitHub Secret** di repo fork kalian (Settings → Secrets and variables → Actions), misalnya secret bernama `DUMMY_API_KEY` berisi nilai contoh (bukan kredensial asli).
2. Lengkapi `# TODO` di [`../.github/workflows/tugas-14-ci-example.yml`](../.github/workflows/tugas-14-ci-example.yml) — workflow GitHub Actions sederhana yang **memakai** secret tersebut sebagai environment variable saat berjalan, TANPA pernah menampilkan nilainya di log. **Catatan penting:** GitHub Actions hanya mengenali workflow yang berada di `.github/workflows/` pada **root repositori**, bukan di dalam folder tugas — karena itu file workflow-nya ditaruh di root, cukup dibatasi (`paths:`) agar hanya terpicu saat folder `tugas-14-keamanan-cloud/` berubah.
3. Jalankan workflow (push ke repo, atau trigger manual di tab Actions), tunjukkan di log bahwa secret tidak pernah tercetak dalam bentuk plain text (GitHub otomatis mask nilai secret di log — buktikan ini).
4. Screenshot halaman Settings → Secrets (tanpa membuka nilai secret-nya, cukup nama secretnya) dan log run workflow, simpan di `bukti/`.

### Bagian 3 — Analisis Shared Responsibility Model

Tulis di `README.md`:
1. Dalam kebocoran *access key* di skenario ini, bagian mana yang jadi **tanggung jawab penyedia cloud** dan bagian mana yang jadi **tanggung jawab pengguna** (developer)? Gunakan kerangka *Shared Responsibility Model*.
2. Kaitkan dengan `.gitignore` — jelaskan kenapa file `.env` (berisi config asli, ingat Tugas 13) **tidak boleh** ikut ter-commit, dan bagaimana `.gitignore` mencegah ini (lihat contoh di `.gitignore` folder ini).
3. Jelaskan konsep **least privilege** dalam IAM — kenapa access key sebaiknya dibatasi izinnya (mis. hanya bisa baca, tidak bisa hapus) dibanding memberi akses penuh (admin/root) ke semua service.

## Struktur Submission

```
tugas-14-keamanan-cloud/
├── README.md                          # Analisis Shared Responsibility Model + Least Privilege
├── JURNAL.md
├── .gitignore                          # Sudah disediakan sebagai contoh
├── .env.example                        # Template config (nilai asli TIDAK PERNAH di-commit)
└── bukti/
    ├── gitleaks-report.json
    └── (screenshot GitHub Secrets settings, log workflow run)

# Catatan: file workflow-nya ada di root repo, BUKAN di folder ini:
# .github/workflows/tugas-14-ci-example.yml   # Lengkapi TODO di sini
```

## Rubrik Penilaian (Tugas 14)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Hasil scan Gitleaks & dokumentasinya | 25% | Laporan lengkap, temuan (jika ada) dijelaskan |
| Implementasi GitHub Secrets & workflow | 30% | Secret dipakai benar, tidak pernah tercetak plain text di log |
| Analisis Shared Responsibility Model | 30% | Pemetaan tanggung jawab spesifik ke skenario kebocoran, bukan definisi umum |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya ke AI gambaran umum Shared Responsibility Model/IAM untuk brainstorming; **tidak boleh** meminta AI menuliskan isi `# TODO` di workflow atau analisis akhir. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- `README.md` wajib menjelaskan mengapa GitHub bisa otomatis mem-mask nilai secret di log Actions (apa mekanismenya, dan apa keterbatasannya — mis. tetap bisa bocor jika secret di-decode/encode ulang dalam log).
