# Tugas 2 — Service-Oriented Architecture (SOA)

**Kelompok:** [kelompok 5]

| Nama | NIM |
|---|---|---|
| Hendra DIrga Dwi Saputra | 103072430018 |
| Alif Luthfan Adeefa | 103072400163 |
| Setyo Nugroho | 103072400045 |

Pada rancangan FoodGo, Service-Oriented Architecture (SOA) digunakan untuk
memisahkan fungsi utama aplikasi menjadi beberapa service yang memiliki
tanggung jawab masing-masing. Pada bagian ini, Service Pesanan dan Service
Pembayaran dipisahkan sehingga proses yang berkaitan dengan pesanan tidak
menjadi satu implementasi dengan proses pembayaran.

### 1. Service Pesanan

Service Pesanan bertanggung jawab menangani proses pemesanan yang dilakukan
oleh pelanggan. Service ini menerima permintaan pembuatan pesanan,
mengelola informasi dan status pesanan, serta berkomunikasi dengan Service
Pembayaran ketika pesanan membutuhkan proses pembayaran.

Dengan Service Pesanan yang berdiri sebagai service tersendiri, perubahan
pada implementasi internal proses pesanan tidak harus dilakukan bersamaan
dengan perubahan pada implementasi Service Pembayaran.

### 2. Service Pembayaran

Service Pembayaran bertanggung jawab menangani proses pembayaran pesanan.
Service ini menerima permintaan pembayaran dari Service Pesanan, memproses
pembayaran, kemudian mengembalikan hasil atau status pembayaran kepada
Service Pesanan.

Pemisahan ini membuat fungsi pembayaran tidak lagi menjadi bagian internal
dari Service Pesanan. Service Pembayaran dapat dikembangkan dan dikelola
sebagai service tersendiri selama kontrak komunikasi dengan Service Pesanan
tetap dipenuhi.

### 3. Komunikasi Service Pesanan dan Service Pembayaran

Service Pesanan dan Service Pembayaran menggunakan komunikasi sinkron
dengan pola request-response.

Alurnya adalah sebagai berikut:

1. Pelanggan membuat pesanan melalui Service Pesanan.
2. Service Pesanan mengirimkan request pembayaran kepada Service Pembayaran.
3. Service Pembayaran memproses request tersebut.
4. Service Pembayaran mengirimkan response berupa status hasil pembayaran.
5. Service Pesanan menerima hasil tersebut dan melanjutkan proses pesanan
   sesuai status pembayaran.

Secara sederhana, komunikasi tersebut dapat digambarkan sebagai:

```text
Pelanggan
    |
    | membuat pesanan
    v
Service Pesanan
    |
    | request pembayaran
    v
Service Pembayaran
    |
    | response status pembayaran
    v
Service Pesanan
