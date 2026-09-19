"""
Tugas 13 - Contoh Aplikasi "Sebelum" Audit Twelve-Factor App

JANGAN diubah file ini - ini adalah bukti "before" untuk laporan audit kalian.
Buat perbaikannya di file terpisah: fixed_app.py

(Kode ini sengaja tidak lengkap secara fungsional - fokus tugas adalah
menemukan pelanggaran prinsip Twelve-Factor App di dalamnya, bukan
menjalankan aplikasi ini sebagai aplikasi produksi.)
"""

import requests  # dipakai tapi tidak pernah dicantumkan di file dependency manapun

DATABASE_URL = "postgresql://admin:SuperSecret123@db.internal.foodgo.com:5432/orders"
PAYMENT_API_KEY = "sk_live_4f9a8b2c1d3e4f5a6b7c8d9e0f1a2b3c"

LOG_PATH = "/Users/developer-a/foodgo/logs/app.log"


def kirim_notifikasi_pembayaran(user_id, jumlah):
    """Kirim notifikasi ke payment gateway eksternal (contoh saja, tidak benar-benar dipanggil)."""
    response = requests.post(
        "https://api.paymentgateway.example.com/v1/notify",
        headers={"Authorization": f"Bearer {PAYMENT_API_KEY}"},
        json={"user_id": user_id, "jumlah": jumlah},
    )
    return response.status_code


def catat_log(pesan):
    with open(LOG_PATH, "a") as f:
        f.write(pesan + "\n")


if __name__ == "__main__":
    print(f"Menghubungkan ke database: {DATABASE_URL}")
    catat_log("Aplikasi dimulai")
