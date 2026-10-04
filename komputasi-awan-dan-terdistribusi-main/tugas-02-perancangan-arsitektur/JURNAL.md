# Jurnal Proses — Tugas 2

## 18/9/2026 

### Proses Perancangan

* **Opsi arsitektur yang dipertimbangkan:**
  Pada awal perancangan, kelompok mempertimbangkan penggunaan **SOA secara keseluruhan**. Dalam pendekatan tersebut, setiap service berkomunikasi secara langsung menggunakan request-response. Namun, pendekatan ini masih dapat menyebabkan ketergantungan antarmodul, terutama ketika Service Pesanan harus menunggu respons dari service lain.

* **Kenapa akhirnya pilih SOA + Pub-Sub:**
  Kelompok memilih kombinasi **SOA dan Publish-Subscribe** karena tidak semua komunikasi dalam FoodGo memiliki kebutuhan yang sama. Komunikasi yang membutuhkan hasil secara langsung, seperti validasi katalog dan pembayaran, lebih sesuai menggunakan komunikasi sinkron. Sementara itu, aktivitas setelah pembayaran seperti pemberitahuan ke restoran, penugasan kurir, dan pembaruan status lebih sesuai menggunakan komunikasi asinkron melalui event dan message broker. Pendekatan ini diharapkan dapat mengurangi ketergantungan langsung antarservice.

* **Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa):**
  Pada versi awal, komunikasi antarservice lebih banyak menggunakan komunikasi sinkron. Setelah mengevaluasi alur FoodGo, beberapa komunikasi diubah menjadi asinkron menggunakan Publish-Subscribe. Message Broker ditambahkan sebagai perantara event. API Gateway juga digunakan sebagai pintu masuk komunikasi dari aplikasi klien ke service. Perubahan ini dilakukan agar service yang menghasilkan event tidak perlu mengetahui secara langsung service mana saja yang akan menerima dan memproses event tersebut.

### Hasil Akhir Perancangan

Kelompok menggunakan **Hybrid SOA + Publish-Subscribe**. Service inti seperti Pesanan, Pembayaran, Katalog Resto, dan Kurir/Notifikasi dipisahkan sehingga dapat dikembangkan dan di-deploy secara independen. Komunikasi sinkron digunakan pada bagian yang membutuhkan respons langsung, sedangkan komunikasi asinkron digunakan untuk proses yang tidak perlu menahan alur utama pengguna.

---

## Log Penggunaan AI (Level 2)

AI digunakan hanya sebagai alat bantu **brainstorming dan penyusunan outline awal**. Keputusan arsitektur, penyesuaian dengan studi kasus FoodGo, diagram, analisis trade-off, dan teks akhir disusun serta diverifikasi oleh kelompok.

| Tanggal    | Tool AI | Prompt yang diberikan                                                                                                                                                          | Ringkasan saran/ide AI                                                                                                                                                                                          | Bagaimana diolah jadi tulisan/kode sendiri                                                                                                                                                                                                               |
| ---------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 18/9/2026  | ChatGPT | Meminta ide awal mengenai pilihan arsitektur yang dapat digunakan untuk mengurangi coupling pada sistem FoodGo dan meminta perbandingan umum antara SOA dan Publish-Subscribe. | Memberikan ide bahwa SOA dapat digunakan untuk memisahkan fungsi menjadi beberapa service, sedangkan Publish-Subscribe dapat digunakan untuk komunikasi berbasis event yang tidak membutuhkan respons langsung. | Ide tersebut digunakan sebagai bahan brainstorming. Kelompok kemudian menentukan sendiri kombinasi SOA + Pub-Sub yang paling sesuai dengan kebutuhan FoodGo dan menyusun keputusan arsitektur berdasarkan studi kasus tugas.                             |
| 18/9/2026  | ChatGPT | Meminta outline umum untuk membedakan komunikasi sinkron dan asinkron pada alur pemesanan makanan.                                                                             | Memberikan gambaran bahwa proses yang membutuhkan respons langsung dapat menggunakan komunikasi sinkron, sedangkan notifikasi dan event lanjutan dapat menggunakan komunikasi asinkron.                         | Outline digunakan sebagai dasar untuk menentukan bagian mana yang menggunakan request-response dan bagian mana yang menggunakan event. Detail alur, nama service, event, dan hubungan antar-komponen ditentukan serta disesuaikan sendiri oleh kelompok. |
| 18/9/2026  | ChatGPT | Meminta ide umum mengenai trade-off yang perlu diperhatikan ketika sistem monolitik dipecah menjadi beberapa service.                                                          | Memberikan beberapa topik yang perlu dipertimbangkan, seperti kompleksitas operasional, debugging, konsistensi data, dan komunikasi antarservice.                                                               | Topik tersebut digunakan sebagai daftar awal untuk diskusi kelompok. Kelompok kemudian memilih dan mengembangkan trade-off yang relevan dengan rancangan FoodGo, serta menentukan cara penanganannya sendiri.                                            |
