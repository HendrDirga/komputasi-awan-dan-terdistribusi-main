# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock

Hasil `processed_count` yang didapat pada demonstrasi race condition:
Tanpa Lock: 10 (seharusnya 100)
Alasan meleset: beberapa thread dapat membaca nilai `processed_count` yang sama sebelum thread lain menulis hasil increment-nya. Ketika hasil tersebut ditulis kembali, pembaruan dari thread lain dapat tertimpa. Akibatnya jumlah akhir lebih kecil daripada jumlah order yang sebenarnya diproses.

## Percobaan dengan Lock

Hasil pengujian lokal versi final:
Total pesanan diproses: 100 (seharusnya 100)
Semua pesanan berhasil diproses dengan aman.

Hasil menunjukkan counter mencapai 100 pada setiap percobaan karena perubahan terhadap shared counter dilakukan di dalam `with lock:`.

## Kendala Docker

Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya: 
1. `WSL not installed` pada Docker Desktop: dijalankan `wsl --install` di PowerShell administrator, lalau tinggal restart laptop.
3. `meta.json ... being used by another process`: Docker Desktop belum selesai startup, tunggu sampai berstatus running lalu `docker build` diulang.


## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 2026-10-04 | ChatGPT | Meminta penjelasan konsep multithreading, race condition, penggunaan Lock, dan struktur umum Docker pada studi kasus pemrosesan pesanan. | Memberikan penjelasan mengenai konsep multithreading, kemungkinan terjadinya race condition pada shared variable, fungsi Lock untuk sinkronisasi, serta gambaran umum tahapan implementasi dan pengujian. | Penjelasan digunakan sebagai referensi untuk memahami konsep dan menyusun langkah pengerjaan. Implementasi kode, pengujian, dan penjelasan akhir disesuaikan dan diverifikasi sendiri.. |
