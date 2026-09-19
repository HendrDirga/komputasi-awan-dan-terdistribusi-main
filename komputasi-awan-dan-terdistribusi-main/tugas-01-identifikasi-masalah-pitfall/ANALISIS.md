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
Asumsi bahwa latency adalah nol berarti sistem seolah-olah menganggap komunikasi antara satu modul dengan modul lainnya berlangsung secara langsung dan tanpa keterlambatan. Pada sistem terdistribusi, setiap komunikasi antar-service membutuhkan waktu untuk mengirim request, memproses request, dan mengembalikan response. Waktu tersebut tidak selalu sama dan dapat meningkat ketika jaringan atau service yang dituju sedang mengalami beban tinggi.

Pada kasus FoodGo, modul pesanan harus berkomunikasi dengan modul pembayaran. Ketika jumlah pesanan meningkat, jumlah request yang diterima oleh modul pembayaran juga meningkat. Jika modul pembayaran menjadi lebih sibuk, waktu yang dibutuhkan untuk memberikan response dapat bertambah. Jika modul pesanan tetap menunggu tanpa batas waktu, request yang sedang berjalan akan terus menggunakan resource meskipun response dari modul pembayaran belum diterima.

Masalah tersebut dapat menjadi semakin besar karena satu request yang lambat dapat membuat resource yang tersedia untuk menangani request lain menjadi berkurang. Dengan demikian, keterlambatan pada satu service dapat ikut memengaruhi service lain yang bergantung padanya.

**Dampak ke FoodGo:**  
Dampak pertama adalah meningkatnya waktu respons ketika pengguna melakukan pemesanan. Ketika modul pesanan mengirim request ke modul pembayaran dan pembayaran membutuhkan waktu lebih lama untuk memberikan response, modul pesanan harus menunggu lebih lama sebelum dapat melanjutkan proses.

Ketika hanya terdapat sedikit request, kondisi tersebut mungkin belum terlalu terlihat. Namun, pada saat promo atau jam makan siang ketika jumlah pesanan meningkat, banyak request dapat berada dalam kondisi menunggu secara bersamaan. Akibatnya, resource pada backend dapat semakin banyak digunakan untuk menangani request yang belum selesai.

Rantai kegagalannya dapat digambarkan sebagai berikut:

`Lonjakan pesanan`

→ `request ke service pembayaran meningkat`

→ `service pembayaran semakin sibuk`

→ `response pembayaran semakin lambat`

→ `modul pesanan menunggu lebih lama`

→ `banyak request tertahan`

→ `resource backend semakin terbebani`

→ `request lain ikut melambat`

→ `terjadi timeout`

Kondisi tersebut sesuai dengan gejala yang terjadi pada FoodGo, yaitu aplikasi menjadi sangat lambat dan beberapa permintaan mengalami `timeout`. Masalahnya bukan hanya karena jumlah pengguna meningkat, tetapi karena desain sistem membuat modul pesanan harus terus menunggu service lain yang responsnya tidak dapat dijamin selalu cepat.

Selain itu, jika tidak terdapat batas waktu pada komunikasi tersebut, sebuah request dapat menunggu jauh lebih lama daripada waktu yang seharusnya. Jika kondisi ini terjadi pada banyak request secara bersamaan, keterlambatan dapat berkembang menjadi masalah yang lebih besar pada keseluruhan backend.

**Solusi desain awal:**  
FoodGo dapat menerapkan `timeout` pada komunikasi antara modul pesanan dan modul pembayaran. Dengan adanya timeout, modul pesanan tidak akan menunggu response tanpa batas waktu. Jika service pembayaran tidak memberikan response dalam batas waktu tertentu, request dapat dianggap mengalami kegagalan sementara atau masuk ke mekanisme penanganan berikutnya.

Selain timeout, FoodGo dapat menggunakan `asynchronous processing` untuk proses yang tidak harus menghasilkan response secara langsung. Salah satu pendekatannya adalah menggunakan `message queue`. Modul pesanan dapat memasukkan pekerjaan pembayaran ke dalam queue, kemudian service pembayaran mengambil dan memproses pekerjaan tersebut.

Pendekatan tersebut dapat mengurangi ketergantungan langsung antara modul pesanan dan pembayaran. Modul pesanan tidak harus mempertahankan request dalam kondisi menunggu sampai seluruh proses pembayaran selesai.

Untuk komunikasi yang memang harus dilakukan secara langsung, timeout dapat dikombinasikan dengan mekanisme seperti `retry` terbatas dan `exponential backoff`. Retry sebaiknya tidak dilakukan tanpa batas karena service yang sedang mengalami beban tinggi justru dapat menerima request tambahan dari proses retry.

Dengan demikian, rancangan awal yang dapat digunakan adalah:

`Request pesanan`

→ `Service pembayaran`

→ `timeout jika terlalu lama`

→ `retry terbatas jika kegagalan bersifat sementara`

Sedangkan untuk proses yang tidak harus selesai pada request yang sama:

`Request pesanan`

→ `Message Queue`

→ `Service pembayaran`

→ `proses asynchronous`

→ `update status pembayaran`

**Trade-off:**  
Penerapan timeout memang mencegah sebuah request menunggu tanpa batas, tetapi timeout tidak otomatis menyelesaikan proses yang sedang berjalan pada service tujuan. Misalnya, modul pesanan berhenti menunggu karena timeout, tetapi modul pembayaran mungkin masih sedang memproses transaksi tersebut. Karena itu, FoodGo perlu memiliki mekanisme untuk menentukan status transaksi agar tidak terjadi pembayaran ganda atau status pesanan yang tidak konsisten.

Penggunaan retry juga memiliki risiko. Retry dapat membantu ketika kegagalan disebabkan oleh gangguan jaringan yang hanya sementara, tetapi jika service pembayaran sedang overload, terlalu banyak retry justru akan menambah jumlah request yang masuk. Hal tersebut dapat memperbesar beban dan memperparah kondisi sistem.

Sementara itu, penggunaan message queue dan asynchronous processing dapat mengurangi waktu tunggu pada request utama, tetapi konsekuensinya adalah arsitektur menjadi lebih kompleks. FoodGo harus menangani status pekerjaan di dalam queue, kemungkinan pesan diproses ulang, kegagalan pemrosesan, serta sinkronisasi status antara pesanan dan pembayaran.

Jadi, solusi tidak cukup hanya dengan membuat komunikasi menjadi lebih cepat. FoodGo perlu merancang sistem agar keterlambatan komunikasi dapat ditangani tanpa menyebabkan seluruh request ikut tertahan. Trade-off utamanya adalah peningkatan ketahanan dan kemampuan menangani beban harus dibayar dengan tambahan kompleksitas pada pengelolaan timeout, retry, queue, dan status transaksi.

---

## Pitfall 2: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Pitfall 3: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
