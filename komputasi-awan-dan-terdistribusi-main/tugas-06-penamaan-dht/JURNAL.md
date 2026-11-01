# Jurnal Proses — Tugas 6

## Implementasi find_successor
- Kesalahan pertama yang ditemui (mis. lupa wrap-around di ring): saat pertama dijalankan program langsung `SyntaxError: unterminated string literal` di baris `print("\n--- ...")`, karena `\n` tertulis sebagai ganti baris sungguhan waktu kode ditempel. Masalah logikanya ada di wrap-around: key 178–255 tidak punya node dengan id >= key, jadi daftar kandidatnya kosong.
- Cara memperbaikinya: string `print` dibetulkan jadi `\n` lagi. Untuk wrap-around, kalau kandidat kosong `find_successor` mengembalikan `min(self.nodes)`. Sudah dicek: key 178 dan 255 jatuh ke node 40, key 177 tetap di node 177.
- Catatan soal petunjuk TODO 3: kondisi "key dengan hash <= node_id" tidak cukup kalau node baru menjadi id terkecil. Dicoba dengan node id 8 yang masuk ke ring berisi node 40 dan 177, kurir-006 (hash 217) harus ikut pindah ke node 8 padahal 217 > 8. Karena itu `join` memakai `find_successor(key) == node_id` setelah node baru masuk.
- Tabrakan hash juga ketemu: kurir-012 dan kurir-024 sama-sama 116. Karena `self.data` memakai hash sebagai key, pendaftaran kedua bisa menimpa kurir pertama, jadi `register_kurir` menolaknya dan `lookup` mengecek ID kurirnya.

## Skenario join/leave
- Skenario bawaan hanya punya kurir-001 s/d 003 (hash 50, 28, 132). Ternyata node-medan-1 (id 123) dan node-jakarta-1 (id 177) sama-sama tidak memegang satu pun dari ketiganya, jadi tidak ada perpindahan yang terlihat. Kurir ditambah sampai kurir-012 supaya perpindahannya kelihatan.
- Hasil sebelum & sesudah node baru bergabung: sebelum, kurir-012 ditangani node 136. Sesudah node-medan-1 masuk, kurir-012 ditangani node 123 dengan IP yang sama (192.168.1.21). 11 kurir lain tidak pindah.
- Hasil sebelum & sesudah node keluar: sebelum, kurir-005 dan kurir-009 ditangani node 177. Sesudah node-jakarta-1 keluar, keduanya ditangani node 40 (wrap-around) dengan IP yang sama. 10 kurir lain tidak pindah.
- Pengujian tambahan: 200 putaran join/leave acak dengan 54 kurir, semua lookup tetap mengembalikan IP yang benar. Kasus ring kosong, node yang tidak ada, dan node terakhir keluar juga dicoba.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 31 Nov 2026 | ChatGPT | jelaskan konsep successor dan aturan wrap around pada topology chord dht | Penjelasan cara menentukan node penanggung jawab key (ID node terkecil yang >= hash key) dan memutar kembali ke node ID terkecil jika nilai hash key melewati semua ID node di ring. | Memakai konsep tersebut untuk menyusun logika `find_successor` serta memahami perpindahan key saat node baru bergabung atau keluar dari ring. |
| 31 Nov 2026 | Claude | bagaimana perpindahan tanggung jawab key saat terjadi join dan leave node pada consistent hashing chord? | Penjelasan bahwa saat node baru masuk, ia hanya mengambil alih sebagian key dari successor lamanya, dan saat node keluar, seluruh key miliknya dialihkan ke successor berikutnya tanpa mengganggu node lain. | Menghubungkan penjelasan tersebut dengan skenario masuknya `node-medan-1` dan keluarnya `node-jakarta-1`, lalu mengamati serta mencatat perpindahan key kurir pada hasil program. |
| 1 Nov 2026 | Claude | apa kelebihan dht/chord dibanding dns dan tabel terpusat untuk memetakan IP yang sering berubah? | Poin perbandingan terkait bottleneck/single point of failure pada server pusat, masalah cache TTL pada DNS untuk IP dinamis, serta pembagian beban update secara merata di Chord. | Mengembangkan poin-poin tersebut menjadi analisis perbandingan di `README.md` dengan mengaitkannya langsung pada kasus kurir FoodGo dan temuan dari hasil simulasi. |
