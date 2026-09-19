# Tugas 11 (Pekan 11) — Implementasi IaaS

**Materi terkait:** Infrastructure as a Service (IaaS).

## Studi Kasus

Sebuah perusahaan butuh **server Linux kustom** untuk menjalankan script otomasi internal (mis. backup rutin, pembersihan log, health check) dengan **biaya minimal**.

## Kenapa Docker, Bukan AWS/Azure Free Tier?

Materi IaaS biasanya diajarkan dengan provisioning VM sungguhan di AWS EC2/Azure Free Tier. Di kelas ini, kita **sengaja mengganti dengan Docker container** sebagai simulasi VM, supaya:
- Tidak ada risiko tidak sengaja kena biaya (VM cloud tetap bisa menagih walau "free tier" jika lupa dimatikan, kena data transfer, dsb).
- Tidak perlu kartu kredit/verifikasi identitas untuk daftar akun cloud.
- Semua bisa dikerjakan offline di laptop, kapan saja, tanpa kuota internet besar.

**Konsekuensi yang harus kalian sadari dan analisis** (bagian penting dari penilaian tugas ini): container Docker **bukan virtualisasi penuh** seperti VM sungguhan — container berbagi kernel dengan host, sedangkan VM (baik on-premise via VirtualBox maupun di cloud) punya kernel sendiri yang terisolasi penuh lewat hypervisor. Ini akan kalian bahas di bagian analisis.

## Tugas Kelompok

1. Buat `Dockerfile` yang mensimulasikan "VM Linux kustom" — mulai dari base image OS penuh (bukan `-slim`/`-alpine`), lalu install tools yang dibutuhkan skrip otomasi kalian (mis. `cron`, `rsync`, `curl`).
2. Tulis `provision.sh` — script Bash otomasi **perusahaan** yang benar-benar berguna, pilih salah satu skenario (atau buat versi kalian sendiri, jelaskan di README):
   - **Backup otomatis**: mem-backup sebuah folder ke folder lain terjadwal (pakai `cron`).
   - **Log rotation & cleanup**: menghapus/mengompres log lebih dari N hari.
   - **Health check**: mengecek periodik apakah sebuah service (mis. port tertentu) masih hidup, dan mencatat ke file log jika mati.
3. `Dockerfile` harus meng-copy `provision.sh` ke dalam image dan menjalankannya sebagai bagian dari startup container (simulasi: begitu "VM" menyala, otomasi langsung aktif — seperti *user data script* di EC2).
4. Buktikan otomasi benar-benar berjalan di dalam container (mis. tunjukkan file backup baru muncul, atau log rotation terjadi, atau health check mendeteksi service mati) — screenshot/log di `bukti/`.

## Cara Menjalankan

```bash
docker build -t foodgo-custom-vm .
docker run --rm -it foodgo-custom-vm
```

## Analisis yang Wajib Ditulis di `README.md`

1. Jelaskan mengapa skenario ini termasuk **IaaS** (bukan PaaS/SaaS) — kaitkan dengan siapa yang bertanggung jawab mengelola apa (OS, runtime, aplikasi) di model IaaS.
2. Jelaskan **perbedaan Docker container vs VM sungguhan** (isolasi kernel, overhead, use case mana yang lebih cocok untuk container vs VM) — dan kapan simulasi Docker ini **tidak cukup** merepresentasikan IaaS asli (mis. jika perusahaan butuh kernel Linux custom atau OS berbeda dari host).
3. Estimasi kasar: jika ini benar-benar di-deploy ke VM cloud (mis. AWS EC2 t2.micro Free Tier), instance seperti apa yang dibutuhkan dan berapa biayanya jika keluar dari batas free tier?

## Struktur Submission

```
tugas-11-implementasi-iaas/
├── README.md      # Analisis IaaS + perbedaan Docker vs VM
├── JURNAL.md
├── Dockerfile
├── provision.sh
└── bukti/          # Bukti otomasi berjalan (log, screenshot)
```

## Rubrik Penilaian (Tugas 11)

| Komponen | Bobot | Kriteria |
|---|---|---|
| `Dockerfile` valid & ter-build | 20% | Image berhasil dibangun dari base OS penuh |
| Script otomasi benar-benar berfungsi | 35% | Bukti nyata (log/screenshot) otomasi berjalan sesuai skenario dipilih |
| Analisis IaaS & keterbatasan simulasi Docker | 30% | Paham perbedaan container vs VM, bukan sekadar definisi |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya opsi skenario otomasi apa saja yang umum dipakai; **tidak boleh** meminta AI menuliskan isi `provision.sh` atau `Dockerfile` secara lengkap. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- `JURNAL.md` wajib menjelaskan fungsi tiap bagian `provision.sh` yang kalian tulis, termasuk apa yang terjadi jika salah satu baris dihapus (coba sendiri dan catat hasilnya).
