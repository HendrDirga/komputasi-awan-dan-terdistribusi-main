"""
Tugas 15 - Simulasi Sensor Smart City

Beberapa "sensor" (thread berbeda) mengirim data periodik ke RabbitMQ.
Lengkapi TODO. Pastikan `docker compose up -d` sudah jalan.
"""

import pika
import json
import random
import threading
import time

QUEUE_NAME = "data_sensor"

SENSOR_LIST = [
    {"id": "sensor-lampu-01", "tipe": "lampu_jalan"},
    {"id": "sensor-udara-01", "tipe": "kualitas_udara"},
    {"id": "sensor-parkir-01", "tipe": "okupansi_parkir"},
]


def buat_channel():
    # TODO 1: buat koneksi & channel ke RabbitMQ (localhost), deklarasikan
    # QUEUE_NAME dengan durable=True (sama seperti pola di Tugas 4).
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    return connection, channel


def baca_nilai_sensor(tipe: str) -> float:
    # TODO 2: kembalikan nilai simulasi sesuai tipe sensor, misalnya:
    # - lampu_jalan: 0 (mati) atau 1 (nyala)
    # - kualitas_udara: nilai AQI acak 20-200
    # - okupansi_parkir: jumlah slot terisi acak 0-50
    return random.uniform(0, 100)


def jalankan_sensor(sensor: dict):
    connection, channel = buat_channel()
    try:
        while True:
            pesan = {
                "sensor_id": sensor["id"],
                "tipe": sensor["tipe"],
                "nilai": baca_nilai_sensor(sensor["tipe"]),
                "timestamp": time.time(),
            }
            # TODO 3: publish `pesan` (json-encoded) ke QUEUE_NAME.
            print(f"[{sensor['id']}] TODO: kirim {pesan}")
            time.sleep(random.uniform(2, 5))
    finally:
        connection.close()


def main():
    threads = []
    for sensor in SENSOR_LIST:
        t = threading.Thread(target=jalankan_sensor, args=(sensor,), daemon=True)
        threads.append(t)
        t.start()

    print(f"{len(SENSOR_LIST)} sensor berjalan, kirim data ke queue '{QUEUE_NAME}'. Ctrl+C untuk berhenti.")
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
