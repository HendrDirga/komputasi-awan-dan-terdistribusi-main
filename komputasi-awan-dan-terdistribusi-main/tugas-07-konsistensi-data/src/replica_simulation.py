"""
Tugas 7 (opsional) - Simulasi Replikasi Dua Server (Jakarta & Bandung)

Mensimulasikan delay replikasi dan masalah inconsistent read,
lalu memperbaikinya dengan mekanisme Read-Your-Writes sederhana.
"""

import time
import threading

REPLICATION_DELAY = 2.0


class Replica:
    def __init__(self, name: str):
        self.name = name
        self.saldo: dict[str, float] = {}
        self.last_write_version: dict[str, int] = {}
        self._lock = threading.Lock()

    def write(self, user_id: str, saldo_baru: float, version: int):
        with self._lock:
            if version <= self.last_write_version.get(user_id, 0):
                return
            self.saldo[user_id] = saldo_baru
            self.last_write_version[user_id] = version
        print(f"[{self.name}] WRITE saldo {user_id} = {saldo_baru} (versi {version})")

    def read(self, user_id: str) -> float:
        with self._lock:
            return self.saldo.get(user_id, 0.0)

    def version_of(self, user_id: str) -> int:
        with self._lock:
            return self.last_write_version.get(user_id, 0)


class ReplicationSystem:
    def __init__(self):
        self.jakarta = Replica("Jakarta")
        self.bandung = Replica("Bandung")
        self.version_counter = 0

    def top_up(self, user_id: str, jumlah: float) -> int:
        """Top-up selalu ditulis dulu ke server Jakarta (mis. server terdekat pelanggan).
        Mengembalikan nomor versi write, yang disimpan client sebagai 'versi_minimal'."""
        self.version_counter += 1
        version = self.version_counter
        saldo_baru = self.jakarta.read(user_id) + jumlah
        self.jakarta.write(user_id, saldo_baru, version)

        timer = threading.Timer(
            REPLICATION_DELAY,
            self.bandung.write,
            args=(user_id, saldo_baru, version),
        )
        timer.start()
        print(f"[Replikasi] Jakarta -> Bandung akan tiba dalam {REPLICATION_DELAY} detik")
        return version

    def baca_saldo_naif(self, user_id: str, server: str) -> float:
        """Baca saldo TANPA mekanisme Read-Your-Writes - bisa saja stale."""
        replica = self.jakarta if server == "Jakarta" else self.bandung
        return replica.read(user_id)

    def baca_saldo_read_your_writes(
        self,
        user_id: str,
        server: str,
        versi_minimal: int,
        strategi: str = "redirect",
        timeout: float = 5.0,
    ) -> float:
        """Read-Your-Writes: client membawa versi write terakhirnya (versi_minimal).
        Replika yang dituju hanya boleh menjawab jika versinya >= versi_minimal.

        strategi:
          - "redirect": jika replika tertinggal, langsung baca dari Jakarta
            (replika yang pasti sudah punya write tersebut).
          - "polling" : tunggu sampai replika menyusul (atau timeout, lalu
            fallback redirect ke Jakarta agar tidak menggantung selamanya).
        """
        replica = self.jakarta if server == "Jakarta" else self.bandung

        if replica.version_of(user_id) >= versi_minimal:
            return replica.read(user_id)

        if strategi == "polling":
            print(f"[RYW] {replica.name} tertinggal, menunggu sampai versi >= {versi_minimal}...")
            deadline = time.time() + timeout
            while time.time() < deadline:
                if replica.version_of(user_id) >= versi_minimal:
                    return replica.read(user_id)
                time.sleep(0.1)
            print(f"[RYW] Timeout menunggu {replica.name}, fallback ke Jakarta")

        else:
            print(f"[RYW] {replica.name} tertinggal (versi {replica.version_of(user_id)} "
                  f"< {versi_minimal}), redirect baca ke Jakarta")

        return self.jakarta.read(user_id)


def main():
    system = ReplicationSystem()
    user_id = "user1"

    print("=== Skenario NAIF (tanpa Read-Your-Writes) ===")
    system.top_up(user_id, 50000)
    time.sleep(0.5)
    hasil = system.baca_saldo_naif(user_id, "Bandung")
    print("Baca saldo dari Bandung (naif):", hasil)
    if hasil != 50000:
        print("-> BUG: seharusnya 50000, tapi replikasi tertunda sehingga transaksi bisa ditolak")

    time.sleep(REPLICATION_DELAY + 0.5)
    print("Setelah replikasi selesai, Bandung:", system.baca_saldo_naif(user_id, "Bandung"))

    print("\n=== Skenario dengan Read-Your-Writes ===")
    system.top_up(user_id, 20000)
    versi_terakhir = system.version_counter
    time.sleep(0.5)

    print("Baca naif dari Bandung (stale):", system.baca_saldo_naif(user_id, "Bandung"))

    hasil_redirect = system.baca_saldo_read_your_writes(
        user_id, "Bandung", versi_terakhir, strategi="redirect"
    )
    print("Baca RYW (redirect) dari Bandung:", hasil_redirect)
    assert hasil_redirect == 70000, "RYW redirect harus mengembalikan saldo terbaru"

    hasil_polling = system.baca_saldo_read_your_writes(
        user_id, "Bandung", versi_terakhir, strategi="polling"
    )
    print("Baca RYW (polling) dari Bandung:", hasil_polling)
    assert hasil_polling == 70000, "RYW polling harus mengembalikan saldo terbaru"

    print("-> Saldo SELALU benar (70000) walau dibaca segera setelah top-up")


if __name__ == "__main__":
    main()
