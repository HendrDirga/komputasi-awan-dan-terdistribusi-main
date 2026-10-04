"""
Tugas 3 - Simulasi Pesanan Masuk dengan Multithreading

Skeleton ini sengaja belum lengkap. Isi bagian bertanda TODO.
Jangan mengubah nama fungsi (dipakai untuk pengecekan otomatis oleh asisten).
"""

import threading
import random
import time

NUM_ORDERS = 100       
NUM_WORKERS = 10       

processed_count = 0

def process_order(order_id: int) -> None:
    """Proses satu pesanan. Dipanggil oleh tiap thread pekerja."""
    global processed_count

    time.sleep(random.uniform(0.001, 0.01))

    pass


def worker(order_ids: list) -> None:
    """Satu thread pekerja memproses sekumpulan order_id."""
    for order_id in order_ids:
        process_order(order_id)


def main() -> None:
    order_ids = list(range(1, NUM_ORDERS + 1))

    threads = []


    for t in threads:
        t.join()

    print(f"Total pesanan diproses: {processed_count} (seharusnya {NUM_ORDERS})")
    if processed_count != NUM_ORDERS:
        print("RACE CONDITION TERDETEKSI - lengkapi TODO 1 & TODO 2 dengan Lock!")


if __name__ == "__main__":
    main()
