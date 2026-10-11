"""
Tugas 4 - Jalur A: RPC Client (simulasi modul Pesanan)
Jalankan server.py di terminal lain terlebih dahulu.
"""

import xmlrpc.client
import time


def main():
    proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:8000", allow_none=True)

    print("Memanggil cek_saldo('user1') ... menunggu respons sinkron")
    start = time.time()
    saldo = proxy.cek_saldo("user1")
    print(f"  -> saldo user1 = {saldo} (menunggu {time.time() - start:.2f} detik)")

    print("Memanggil proses_pembayaran('user1', 20000) ...")
    start = time.time()
    hasil = proxy.proses_pembayaran("user1", 20000)
    print(f"  -> hasil = {hasil} (menunggu {time.time() - start:.2f} detik)")

    print("Memanggil proses_pembayaran('user1', 999999) (saldo tidak cukup) ...")
    hasil = proxy.proses_pembayaran("user1", 999999)
    print(f"  -> hasil = {hasil}")

    print("Memanggil cek_saldo('user99') (user tidak terdaftar) ...")
    try:
        proxy.cek_saldo("user99")
    except xmlrpc.client.Fault as e:
        print(f"  -> Fault dari server: {e.faultString}")


if __name__ == "__main__":
    main()
