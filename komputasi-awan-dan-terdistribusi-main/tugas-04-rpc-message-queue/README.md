# Tugas 4 – Komunikasi Antar Komponen (RPC & Message Queue)

**Kelompok:** [kelompok 5]

| Nama | NIM | Kontribusi |
|---|---|---|
| Hendra DIrga Dwi Saputra | 103072430018 | Mengerjakan Jalur A (RPC), yaitu fungsi `cek_saldo` dan `proses_pembayaran` di server serta pemanggilannya di client. Menguji client menunggu respons dan skenario server mati di tengah proses. |
| Alif Luthfan Adeefa | 103072400163 | Mengerjakan Jalur B (message queue), yaitu menjalankan RabbitMQ lewat Docker serta membuat publisher dan consumer. Menguji skenario consumer mati lalu dinyalakan lagi untuk membuktikan pesan tidak hilang. |
| Setyo Nugroho | 103072400045 | Menulis analisis kenapa cek saldo dan pembayaran memakai RPC sedangkan notifikasi kurir memakai message queue, beserta dampaknya kalau tertukar. Mengumpulkan log di folder `bukti/` dan menyusun README. |
---

Kami mengerjakan dua jalur. Jalur A (RPC) dipakai untuk cek saldo dan proses pembayaran, sedangkan Jalur B (RabbitMQ) dipakai untuk notifikasi pembayaran berhasil ke modul kurir. Log hasil percobaan ada di folder `bukti/`.

## Cara Menjalankan

Jalur A:
```
python rpc/server.py     # terminal 1
python rpc/client.py     # terminal 2
```

Jalur B:
```
cd mq
docker compose up -d
pip install -r requirements.txt
python consumer.py       # terminal 1
python publisher.py      # terminal 2
```

## Jalur A – RPC

Server kami beri jeda 2 detik di setiap fungsi supaya kelihatan kalau client ikut menunggu. Hasilnya, setiap panggilan dari client butuh sekitar 2 detik dan client tidak lanjut ke baris berikutnya sebelum dapat balasan.

```
Memanggil cek_saldo('user1') ... menunggu respons sinkron
  -> saldo user1 = 50000 (menunggu 2.03 detik)
Memanggil proses_pembayaran('user1', 20000) ...
  -> hasil = {'status': 'sukses', 'pesan': 'pembayaran berhasil', 'saldo_akhir': 30000} (menunggu 2.06 detik)
```

Kalau `user_id` tidak ada, `cek_saldo` kami buat mengembalikan error, bukan 0. Alasannya, saldo 0 itu bisa saja saldo asli user, jadi kalau user yang tidak ada juga dijawab 0, client tidak bisa membedakan keduanya. Untuk `proses_pembayaran`, kalau saldo tidak cukup hasilnya `status: gagal` karena itu kondisi normal, bukan error.

Kami juga mencoba mematikan server saat request sedang diproses. Client langsung dapat `ConnectionRefusedError` dan tidak tahu apakah saldo sudah terpotong atau belum. Ternyata `xmlrpc` juga otomatis mengirim ulang request sekali kalau koneksi putus. Untuk pembayaran ini bisa berbahaya, karena kalau server sempat hidup lagi, saldo bisa terpotong dua kali.

Catatan kecil: awalnya client memakai `localhost` dan setiap panggilan malah butuh sekitar 4 detik. Di Windows, `localhost` dicoba lewat IPv6 dulu, jadi kami ganti ke `127.0.0.1`.

## Jalur B – Message Queue

Antrean dibuat `durable=True` dan pesan dikirim sebagai persistent. Consumer baru mengirim ack setelah pesan selesai diproses.

### Uji pesan tidak hilang

Langkah yang kami lakukan:

1. Matikan `consumer.py`.
2. Jalankan `publisher.py` dua kali, jadi ada 6 pesan. Publisher tetap jalan normal tanpa error.
3. Cek antrean pakai `rabbitmqctl list_queues`, isinya 6 pesan.
4. Restart RabbitMQ (`docker compose restart`), isi antrean masih 6.
5. Nyalakan lagi `consumer.py`, keenam pesan langsung diproses berurutan.
6. Cek antrean lagi, isinya jadi 0.

Output consumer setelah dinyalakan:
```
Kurir menerima notifikasi pembayaran untuk user1 sejumlah 20000 (dikirim Mon Oct 12 02:20:41 2026)
Kurir menerima notifikasi pembayaran untuk user2 sejumlah 40000 (dikirim Mon Oct 12 02:20:42 2026)
Kurir menerima notifikasi pembayaran untuk user3 sejumlah 60000 (dikirim Mon Oct 12 02:20:43 2026)
Kurir menerima notifikasi pembayaran untuk user1 sejumlah 20000 (dikirim Mon Oct 12 02:20:44 2026)
Kurir menerima notifikasi pembayaran untuk user2 sejumlah 40000 (dikirim Mon Oct 12 02:20:45 2026)
Kurir menerima notifikasi pembayaran untuk user3 sejumlah 60000 (dikirim Mon Oct 12 02:20:46 2026)
```

Jadi selama consumer mati, pesannya tidak hilang, tapi tertahan di antrean `pembayaran_berhasil` di RabbitMQ. Karena persistent, pesan juga disimpan ke disk, makanya masih ada walaupun RabbitMQ di-restart. Pesan baru dihapus setelah consumer mengirim ack.

Tapi kalau container RabbitMQ dihapus (`docker compose down`), pesan yang belum diambil akan ikut hilang, karena datanya ada di dalam container.

## Analisis

Cek saldo dan proses pembayaran cocok memakai RPC karena modul Pesanan butuh jawabannya saat itu juga. Pesanan tidak bisa lanjut sebelum tahu saldo cukup atau pembayaran berhasil, jadi menunggu memang wajar.

Notifikasi ke kurir cocok memakai message queue karena modul Pembayaran tidak butuh balasan dari kurir. Di percobaan kami, publisher tetap bisa mengirim walaupun consumer mati, dan pesannya diproses belakangan.

Kalau notifikasi kurir memakai RPC, modul Pembayaran harus menunggu kurir setiap kali ada pembayaran. Kalau kurir lambat, pembayaran ikut lambat. Kalau kurir mati, pembayaran dapat error seperti yang kami lihat di uji server mati, padahal pembayarannya sendiri sudah berhasil.

Sebaliknya, kalau cek saldo memakai message queue, jawabannya bisa telat. Misalnya consumer saldo sedang mati, permintaannya akan menumpuk di antrean dan baru dijawab nanti, padahal user sedang menunggu di halaman checkout.
