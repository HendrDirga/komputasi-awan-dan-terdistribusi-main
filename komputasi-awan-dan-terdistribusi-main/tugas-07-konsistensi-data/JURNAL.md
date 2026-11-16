# Jurnal Proses — Tugas 7

## Hasil Simulasi: Skenario Naif vs Read-Your-Writes

### 1. Skenario tanpa Read-Your-Writes

- Top-up Rp50.000 ditulis ke Jakarta (versi 1), lalu replikasi ke Bandung baru tiba setelah 2 detik.
- Saat saldo dibaca dari Bandung 0,5 detik setelah top-up, hasilnya **0.0**, padahal seharusnya **50.000**. Ini adalah *stale read*.
- Dampaknya: transaksi pembayaran bisa ditolak dengan alasan "saldo tidak cukup" walaupun top-up sudah berhasil.
- Setelah replikasi selesai, Bandung menunjukkan 50.000. Data akhirnya konsisten, tetapi hanya setelah jeda (*eventual consistency*).

### 2. Skenario dengan Read-Your-Writes

- Top-up kedua Rp20.000 menghasilkan saldo **70.000** di Jakarta (versi 2). Bandung masih menyimpan 50.000 (terlihat dari baca naif).
- **Strategi redirect:** Bandung terdeteksi tertinggal (versi 1 < 2), sehingga bacaan dialihkan ke Jakarta dan hasilnya langsung benar, **70.000**.
- **Strategi polling:** sistem menunggu sampai Bandung menerima versi 2, lalu membaca dari Bandung dan hasilnya juga benar, **70.000**.
- Kedua strategi menjamin pengguna selalu melihat hasil write-nya sendiri.

### 3. Argumen yang perlu dipertimbangkan

| Aspek | Naif | RYW Redirect | RYW Polling |
|---|---|---|---|
| Kebenaran saldo setelah top-up | Bisa stale | Selalu benar | Selalu benar |
| Latensi baca | Rendah | Rendah, tetapi lintas kota ke Jakarta | Lebih tinggi (menunggu hingga ~2 detik) |
| Beban ke Jakarta | Normal | Naik, karena replika tertinggal mengalihkan bacaan | Normal |
| Kompleksitas | Rendah | Perlu pelacakan versi | Pelacakan versi + timeout/fallback |
| Ketersediaan | Tinggi | Bergantung pada Jakarta | Tinggi (ada fallback timeout) |

### 4. Kesimpulan akhir

Eventual consistency murni tidak aman untuk saldo e-wallet, karena stale read (0 vs 50.000) dapat menolak transaksi yang sah. Read-Your-Writes menyelesaikan masalah ini dengan biaya kecil: client membawa nomor versi write terakhir, dan replika hanya boleh menjawab bila versinya cukup baru.

Untuk FoodGo, **RYW dengan redirect** adalah pilihan utama karena respons tetap cepat. **Polling dengan timeout fallback** menjadi alternatif bila ingin mengurangi beban ke Jakarta. Pendekatan ini mempertahankan keunggulan replikasi (baca lokal yang cepat di Bandung) sambil memastikan pengguna tidak pernah melihat saldo lama setelah top-up sendiri.

### 5. Alasan

Bukti percobaan mendukung kesimpulan ini: baca naif menghasilkan **0.0** (bug), sedangkan baca RYW menghasilkan **70.000** pada kedua strategi. Assertion lolos dan program selesai dengan `code=0`.
## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
