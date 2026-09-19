"""
Tugas 15 - Processor: konsumsi data sensor dari RabbitMQ, simpan ke MinIO
sebagai object JSON (simulasi menyimpan data ke "cloud storage").
"""

import pika
import json
import io
from datetime import datetime
from minio import Minio

QUEUE_NAME = "data_sensor"
BUCKET_NAME = "smart-city-data"

minio_client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False,
)


def pastikan_bucket_ada():
    # TODO 1: cek apakah BUCKET_NAME sudah ada (minio_client.bucket_exists),
    # jika belum, buat (minio_client.make_bucket).
    pass


def simpan_ke_minio(pesan: dict):
    """Simpan satu data sensor sebagai object JSON terpisah di MinIO."""
    nama_object = f"{pesan['sensor_id']}/{datetime.now().strftime('%Y%m%d-%H%M%S-%f')}.json"
    data_bytes = json.dumps(pesan).encode()

    # TODO 2: upload `data_bytes` ke MinIO (minio_client.put_object) dengan
    # bucket=BUCKET_NAME, object_name=nama_object, data=io.BytesIO(data_bytes),
    # length=len(data_bytes).
    print(f"[TODO] Belum benar-benar tersimpan ke MinIO: {nama_object}")


def callback(ch, method, properties, body):
    pesan = json.loads(body)
    print(f"Menerima data dari {pesan['sensor_id']}: {pesan['nilai']:.2f}")
    simpan_ke_minio(pesan)

    # TODO 3: kirim acknowledgement (ch.basic_ack) setelah berhasil disimpan,
    # supaya jika processor crash SEBELUM basic_ack, pesan tidak hilang dan
    # akan diproses ulang (bagian penting dari bukti "data tidak hilang").


def main():
    pastikan_bucket_ada()

    # TODO 4: buat koneksi & channel ke RabbitMQ (sama seperti sensor_publisher.py),
    # deklarasikan queue yang SAMA (durable=True), daftarkan `callback` via
    # channel.basic_consume(...), lalu channel.start_consuming().
    print(f"Menunggu data sensor dari queue '{QUEUE_NAME}'... (Ctrl+C untuk berhenti)")


if __name__ == "__main__":
    main()
