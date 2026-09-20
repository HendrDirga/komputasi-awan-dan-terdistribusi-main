# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [kelompok 5]

| Nama | NIM | Kontribusi |
|---|---|---|
| Hendra DIrga Dwi Saputra | 103072430018 | Latency Is Zero |
| [nama 2] | [nim] | [pitfall/bagian yang dikerjakan] |
| [nama 3] | [nim] | [pitfall/bagian yang dikerjakan] |

## Pitfall 1: Latency Is Zero — ditulis oleh Hendra Dirga

**Bukti di skenario:**  
Pada skenario FoodGo dijelaskan bahwa modul pesanan memanggil modul pembayaran dan kemudian menunggu tanpa batas waktu. Selain itu, ketika jumlah pesanan meningkat, aplikasi menjadi sangat lambat dan beberapa permintaan mengalami `timeout`. Kondisi tersebut menunjukkan bahwa sistem belum memperhitungkan adanya waktu tunggu dalam komunikasi antar-modul.

**Kenapa ini keliru:**  
Jika latency nol berarti sistem akan menganggap komunikasi antara satu modul dengan yang lain berlangsung secara langsung dan tanpa keterlambatan. Pada sistem terdistribusi, setiap komunikasi antar-service membutuhkan waktu untuk mengirim request, memproses request, dan mengembalikan response. Waktu tersebut tidak selalu sama dan dapat meningkat ketika jaringan atau service yang dituju sedang mengalami beban tinggi.

modul pesanan harus berkomunikasi dengan modul pembayaran. Ketika jumlah pesanan meningkat, jumlah request yang diterima oleh modul pembayaran juga meningkat. Jika modul pembayaran menjadi lebih sibuk, waktu yang dibutuhkan untuk memberikan response dapat bertambah. Jika modul pesanan tetap menunggu tanpa batas waktu, request yang sedang berjalan akan terus menggunakan resource meskipun response dari modul pembayaran belum diterima.

Masalah ini dapat menjadi semakin besar karena satu request yang lambat dapat membuat resource yang tersedia untuk menangani request lain menjadi berkurang. Dengan begitu, keterlambatan pada satu service dapat ikut memengaruhi service lain yang bergantung padanya.

**Dampak ke FoodGo:**  
meningkatnya waktu respons ketika pengguna melakukan pemesanan. Ketika modul pesanan mengirim request ke modul pembayaran dan pembayaran membutuhkan waktu lebih lama untuk memberikan response, modul pesanan harus menunggu lebih lama sebelum dapat melanjutkan proses.

Ketika hanya terdapat sedikit request, kondisi tersebut mungkin belum terlalu terlihat. Namun, pada saat promo atau jam makan siang ketika jumlah pesanan meningkat, banyak request dapat berada dalam kondisi menunggu secara bersamaan. Akibatnya, resource pada backend dapat semakin banyak digunakan untuk menangani request yang belum selesai.

Lonjakan pesanan

→ request ke service pembayaran meningkat

→ service pembayaran semakin sibuk

→ response pembayaran semakin lambat

→ modul pesanan menunggu lebih lama

→ banyak request tertahan

→ resource backend semakin terbebani

→ request lain ikut melambat

→ terjadi timeout

Kondisi ini sesuai dengan akibat yang terjadi pada FoodGo, Efeknya aplikasi menjadi sangat lambat dan beberapa permintaan mengalami `timeout`. Masalahnya bukan hanya karena jumlah user yang meningkat meningkat, tetapi karena desain sistem membuat modul pesanan harus terus menunggu service lain yang responsnya tidak dapat dijamin selalu cepat.

jika tidak terdapat batas waktu pada komunikasi tersebut, sebuah request dapat menunggu jauh lebih lama daripada waktu yang seharusnya. Jika kondisi ini terjadi pada banyak request secara bersamaan, keterlambatan dapat berkembang menjadi masalah yang lebih besar pada keseluruhan backend.

**Solusi desain awal:**  
FoodGo dapat menerapkan batas waktu (`timeout`) pada komunikasi antara modul pesanan dan modul pembayaran. Dengan adanya timeout, modul pesanan tidak akan menunggu respons pembayaran tanpa batas waktu. Jika respons tidak diterima dalam waktu yang telah ditentukan, sistem dapat menghentikan proses menunggu dan memberikan status bahwa pembayaran belum dapat dikonfirmasi.

Untuk proses yang tidak harus selesai sebelum pengguna mendapatkan respons utama, FoodGo juga dapat menggunakan pemrosesan asynchronous. Contohnya, proses notifikasi tidak perlu membuat modul pesanan terus menunggu sampai notifikasi selesai dikirim. Dengan cara ini, modul utama dapat menyelesaikan prosesnya tanpa terlalu bergantung pada proses lain yang lebih lambat.

Pendekatan ini relatif sederhana untuk diterapkan pada tahap awal karena FoodGo tidak harus langsung memisahkan seluruh sistem menjadi banyak service atau menggunakan infrastruktur yang kompleks. Fokus awalnya adalah memberikan batas waktu pada komunikasi dan mengurangi proses yang tidak perlu ditunggu secara langsung.

**Trade-off:**  
Timeout menyebabkan sistem berhenti menunggu meskipun service pembayaran sebenarnya masih memproses request. Oleh karena itu, FoodGo perlu membedakan antara transaksi yang gagal dan masi proses agar tidak terjadi kesalahan status atau pembayaran ganda.


---

## Pitfall 2: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Pitfall 3: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
