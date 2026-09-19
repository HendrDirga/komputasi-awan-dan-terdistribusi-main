"""
Tugas 4 - Jalur B: Publisher (simulasi modul Pembayaran)
Pastikan `docker compose up -d` sudah jalan sebelum menjalankan file ini.
"""

import pika
import json
import time

QUEUE_NAME = "pembayaran_berhasil"


def main():
    # TODO 1: buat koneksi ke RabbitMQ di localhost (pika.BlockingConnection
    # dengan ConnectionParameters(host="localhost")), lalu buat channel.
    connection = None
    channel = None

    # TODO 2: deklarasikan queue dengan nama QUEUE_NAME (channel.queue_declare),
    # gunakan durable=True supaya pesan tidak hilang walau RabbitMQ restart.

    for i in range(1, 4):
        pesan = {
            "user_id": f"user{i}",
            "jumlah": 20000 * i,
            "timestamp": time.time(),
        }
        # TODO 3: publish `pesan` (di-encode json) ke QUEUE_NAME memakai
        # channel.basic_publish(...). Cetak log "Event terkirim: ..." setiap publish.
        print(f"[TODO] Event belum benar-benar terkirim: {pesan}")
        time.sleep(1)

    # TODO 4: tutup koneksi (connection.close()) setelah selesai.
    print("Publisher selesai mengirim event.")


if __name__ == "__main__":
    main()
