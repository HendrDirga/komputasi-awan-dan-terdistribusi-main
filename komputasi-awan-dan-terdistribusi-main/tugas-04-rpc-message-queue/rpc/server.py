"""
Tugas 4 - Jalur A: RPC Server (simulasi modul Pembayaran)
Memakai xmlrpc.server dari Python standard library - tidak perlu install apa pun.
"""

import time
from xmlrpc.server import SimpleXMLRPCServer

# Simulasi "database" saldo user
saldo_user = {
    "user1": 50000,
    "user2": 120000,
}

# Simulasi waktu proses di sisi server (mis. query DB / validasi ke bank),
# supaya terlihat jelas bahwa client ikut menunggu (blocking).
DELAY_PROSES = 2


def cek_saldo(user_id: str) -> float:
    """Kembalikan saldo user_id saat ini."""
    # Keputusan: user yang tidak terdaftar dianggap error (bukan saldo 0),
    # karena saldo 0 adalah kondisi valid untuk user yang ada. Error dikirim
    # ke client sebagai xmlrpc.client.Fault.
    print(f"[server] cek_saldo({user_id!r}) diterima, memproses...")
    time.sleep(DELAY_PROSES)
    if user_id not in saldo_user:
        raise ValueError(f"user_id '{user_id}' tidak ditemukan")
    return saldo_user[user_id]


def proses_pembayaran(user_id: str, jumlah: float) -> dict:
    """Kurangi saldo user sejumlah `jumlah`. Kembalikan status hasil."""
    print(f"[server] proses_pembayaran({user_id!r}, {jumlah}) diterima, memproses...")
    time.sleep(DELAY_PROSES)
    if user_id not in saldo_user:
        return {"status": "gagal", "pesan": "user tidak ditemukan", "saldo_akhir": 0}
    if jumlah <= 0:
        return {"status": "gagal", "pesan": "jumlah harus > 0", "saldo_akhir": saldo_user[user_id]}
    if saldo_user[user_id] < jumlah:
        return {"status": "gagal", "pesan": "saldo tidak cukup", "saldo_akhir": saldo_user[user_id]}

    saldo_user[user_id] -= jumlah
    return {"status": "sukses", "pesan": "pembayaran berhasil", "saldo_akhir": saldo_user[user_id]}


def main():
    server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
    server.register_function(cek_saldo, "cek_saldo")
    server.register_function(proses_pembayaran, "proses_pembayaran")
    print("RPC server modul Pembayaran berjalan di port 8000...")
    server.serve_forever()


if __name__ == "__main__":
    main()
