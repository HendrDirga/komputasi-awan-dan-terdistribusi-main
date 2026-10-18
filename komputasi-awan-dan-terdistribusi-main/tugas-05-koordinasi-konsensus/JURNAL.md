# Jurnal Proses — Tugas 5

## Implementasi Bully
- Kendala saat mengisi TODO 1-4: Saat menjalankan simulasi, kami melihat banyak election berulang di log dan awalnya mengira itu bug. Setelah mempelajari kode, kami paham bahwa itu perilaku normal Bully: node yang menerima ELECTION membalas OK lalu memulai election sendiri. kami juga mempelajari bahwa kode memakai election_lock agar satu node tidak menjalankan beberapa election sekaligus, dan timeout untuk mencegah node menunggu COORDINATOR selamanya.

## Skenario 1: Start normal
- Leader yang terpilih: Node 5 (ID tertinggi).
- Log/observasi: 
    - Node 5 tidak punya peer dengan ID lebih tinggi (peer lebih tinggi: []), jadi langsung mencetak Menjadi LEADER dan mengirim COORDINATOR ke Node 1-4.
    - Node 1-4 lalu mencetak Leader diperbarui: Node 5.
    - Karena kelima node tidak dinyalakan benar-benar bersamaan, ada beberapa node yang memulai election lebih dari sekali dan saling bertukar ELECTION dan OK. Ini normal di Bully, dan pada akhirnya semua node sepakat memilih Node 5.
## Skenario 2: Leader dimatikan
- Leader baru yang terpilih: Node 4 (ID tertinggi yang masih hidup).
- Berapa lama waktu sampai leader baru terdeteksi: : sekitar 2-3 detik. Ini perkiraan dari kode, belum diukur dengan stopwatch.
    - Alasannya, monitor_leader() mengecek leader tiap 2 detik (MONITOR_INTERVAL), dan PING ke node yang sudah mati langsung gagal (koneksi ditolak, paling lama timeout 0.7 detik). Setelah itu Node 4 langsung jadi leader karena ELECTION yang dikirim ke Node 5 tidak dibalas.
- Observasi tambahan: Node 1-3 sadar leader hilang, lalu mengirim ELECTION ke node yang lebih tinggi dan menerima OK dari Node 4. Setelah itu mereka menerima COORDINATOR dari Node 4 dan mencatat Leader diperbarui: Node 4.
## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 18 Okt 2026 | ChatGPT | Jelaskan cara kerja algoritma Bully dalam pemilihan leader pada sistem terdistribusi. | Penjelasan alur election dan coordinator pada Bully. | Mempelajari alur election dan coordinator, lalu menjelaskan kembali proses pemilihan leader berdasarkan hasil pengamatan program. |
| 18 Okt 2026 | Claude | Bagaimana proses pemilihan leader baru jika coordinator sebelumnya dimatikan? | Alur Bully: leader mati terdeteksi lewat PING, node mengirim ELECTION ke ID lebih besar, ada OK atau tidak, lalu pemenang mengirim COORDINATOR. Disertai contoh Node 5 mati lalu Node 4 terpilih. | Memakai penjelasan tersebut untuk memahami hasil skenario ketika Node 5 dimatikan dan mengamati perubahan leader menjadi Node 4. |
| 18 Okt 2026 | Claude | Apa fungsi timeout dan election lock dalam implementasi algoritma Bully? | Fungsi timeout (CONNECT_TIMEOUT, ELECTION_TIMEOUT, MONITOR_INTERVAL) untuk menunggu balasan, dan election_lock untuk mencegah dua election berjalan bersamaan di satu node. Dibedakan dari self.lock yang melindungi data bersama. | Menghubungkan penjelasan tersebut dengan mekanisme timeout dan election lock pada implementasi, kemudian merangkum fungsinya dengan bahasa sendiri. |