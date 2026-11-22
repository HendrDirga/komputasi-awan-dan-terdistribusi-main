# Jurnal Proses — Tugas 9

## Diskusi deployment model
- Opsi yang dipertimbangkan dan kenapa akhirnya memilih salah satu: Hybrid Cloud untuk menjaga data sensitif di lingkungan private, dan hanya lapisan yang tidak sensitif yang boleh menggunakan public cloud. Salah satu hal yang paling lama kami diskusikan adalah garis batas antara keduanya. Kami harus memutuskan dengan jelas: data apa saja yang boleh keluar dari sistem internal. Kami sepakat bahwa NIK utuh dan data biometrik tidak boleh keluar sama sekali. Itu adalah batas yang tidak bisa dilanggar. Kami juga sadar bahwa hybrid cloud membawa risiko baru. Ada risiko dari sinkronisasi data antara private dan public, dan risiko dari titik sambung yang menjadi jalan masuk bagi serangan. Kami bahas kedua risiko itu secara khusus. Kami cari cara untuk mengurangi risikonya. Kami memperkuat keamanan di titik-titik sambung. Kami pastikan sinkronisasi data hanya bisa dilakukan dengan enkripsi kuat dan kontrol akses yang ketat. Kami buat aturan yang jelas dan diterapkan secara konsisten.

## Diskusi service model per komponen
- Database inti dan penyimpanan data biometrik masuk ke IaaS. Alasannya, kami butuh kendali penuh atas enkripsi, kunci, dan pengaturan database.

- API verifikasi kami taruh di PaaS, pakai platform container privat. Awalnya kami bingung antara IaaS dan PaaS. Akhirnya pilih PaaS karena autoscaling lebih gampang dan tim bisa konsentrasi ke aplikasinya.

- Portal publik untuk cek status juga di PaaS, di segmen public. Ringan, gampang diskalakan, dan tidak menyimpan data pribadi lengkap.

- Helpdesk, notifikasi, dan monitoring pakai SaaS. Semuanya alat standar yang tidak perlu dibangun sendiri, dan tidak menyimpan data kependudukan.

- Ada satu hal yang sempat kami debat: apakah SaaS aman untuk monitoring. Kesimpulannya boleh, asal log yang dikirim sudah bersih dari data pribadi.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
||---|---|---|---|
| 22 November 2026 | Gemini | "Bandingkan kelebihan dan kekurangan 4 deployment model cloud (Public, Private, Community, Hybrid) untuk studi kasus sistem kependudukan nasional dengan kebutuhan keamanan data sensitif tinggi namun memiliki lonjakan trafik musiman (seperti pemilu/PPDB)." | Memberikan analisis trade-off tiap model: Public unggul di skalabilitas tapi lemah di kedaulatan data; Private aman tapi boros kapasitas saat idle; Community cocok untuk kolaborasi instansi tapi kurang fleksibel untuk akses publik/perbankan; Hybrid disarankan sebagai jalan tengah dengan pemisahan zona data sensitif dan publik, beserta risiko latency/sinkronisasi antar-lingkungan. | Memilih Hybrid Cloud sebagai keputusan final kelompok, lalu merumuskan batasan teknis spesifik bahwa NIK utuh dan data biometrik dilarang keras keluar dari zona private, serta menambahkan pembahasan khusus mengenai mitigasi risiko titik sambung dan sinkronisasi data. |
