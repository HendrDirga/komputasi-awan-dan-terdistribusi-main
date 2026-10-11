"""
Tugas 4 - Jalur B: Consumer (simulasi modul Kurir/Notifikasi)
Jalankan file ini SEBELUM publisher.py untuk uji normal, atau SESUDAHNYA
untuk membuktikan pesan tetap tersimpan di antrean (asynchronous decoupling).
"""

import pika
import json
import time

QUEUE_NAME = "pembayaran_berhasil"


def callback(ch, method, properties, body):
    pesan = json.loads(body)
    print(
        f"Kurir menerima notifikasi pembayaran untuk {pesan['user_id']} "
        f"sejumlah {pesan['jumlah']} (dikirim {time.ctime(pesan['timestamp'])})"
    )

    # Ack manual SETELAH selesai diproses: kalau consumer crash sebelum baris ini,
    # pesan tidak hilang dan akan dikirim ulang oleh RabbitMQ.
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # Ambil 1 pesan per waktu, pesan berikutnya baru dikirim setelah ack
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    print("Menunggu event dari antrean 'pembayaran_berhasil'... (Ctrl+C untuk berhenti)")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()


if __name__ == "__main__":
    main()
