# Jurnal Proses — Tugas 2

## [Tanggal]
- Opsi arsitektur yang dipertimbangkan: Sempat dipertimbangkan SOA untuk semua komunikasi, tapi ini akan membuat modul pesanan harus terus diubah setiap ada modul notifikasi baru. Akhirnya dipertimbangkan kombinasi SOA dan Pub-Sub.
- Kenapa akhirnya pilih [SOA/Pub-Sub]: Karena kebutuhan komunikasi yang berbeda — modul pesanan-pembayaran butuh respons pasti (berhasil/gagal), sehingga cocok pakai SOA; sementara notifikasi ke kurir dan resto cukup di-broadcast tanpa perlu respons langsung, sehingga cocok pakai Pub-Sub
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa): ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
