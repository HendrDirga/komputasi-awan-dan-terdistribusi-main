"""
Tugas 6 - Simulasi Chord DHT (single-process, tanpa jaringan sungguhan)

Memetakan ID Kurir ke alamat IP terkininya pakai aturan successor Chord.
"""

import hashlib

M_BITS = 8               # ruang identifier 0..255 (disederhanakan dari Chord asli yang pakai 160-bit)
RING_SIZE = 2 ** M_BITS


def hash_id(key: str) -> int:
    """Hash string (ID node atau ID kurir) ke ruang identifier 0..RING_SIZE-1."""
    digest = hashlib.sha1(key.encode()).digest()
    return int.from_bytes(digest, "big") % RING_SIZE


class ChordRing:
    def __init__(self):
        # node_id (hasil hash) -> alamat IP node tersebut
        self.nodes: dict[int, str] = {}
        # key kurir (hasil hash) -> IP kurir yang disimpan node yang bertanggung jawab
        self.data: dict[int, tuple[str, str]] = {}  # hash -> (kurir_id, ip_kurir)

    def join(self, node_name: str, node_ip: str):
        """Tambahkan node baru ke ring. Pindahkan data yang seharusnya
        menjadi tanggung jawab node baru ini dari successor lamanya."""
        node_id = hash_id(node_name)
        if node_id in self.nodes:
            print(f"[JOIN] Gagal: id {node_id} sudah dipakai node lain")
            return

        # successor lama harus dicari sebelum node baru masuk ke self.nodes
        succ_lama = self.find_successor(node_id)
        self.nodes[node_id] = node_ip
        print(f"[JOIN] Node '{node_name}' (id={node_id}) bergabung, alamat {node_ip}")

        # sengaja tidak pakai kondisi key <= node_id saja: kalau node baru jadi
        # id terkecil, key di ujung ring (wrap-around) juga pindah ke node ini
        pindah = [k for k in self.data if self.find_successor(k) == node_id]
        for key_hash in pindah:
            print(f"  {self.data[key_hash][0]} (hash={key_hash}) pindah dari node {succ_lama} ke node {node_id}")
        if succ_lama is not None and not pindah:
            print("  Tidak ada key yang pindah")

    def leave(self, node_name: str):
        """Keluarkan sebuah node dari ring. Data yang dipegangnya harus
        berpindah ke successor-nya."""
        node_id = hash_id(node_name)
        if node_id not in self.nodes:
            print(f"[LEAVE] Gagal: node '{node_name}' tidak ada di ring")
            return

        # catat dulu key milik node ini, sebelum node-nya dihapus
        titipan = [k for k in self.data if self.find_successor(k) == node_id]
        del self.nodes[node_id]
        print(f"[LEAVE] Node '{node_name}' (id={node_id}) keluar dari ring")

        if not self.nodes:
            print("  Ring kosong, semua data ikut hilang")
            self.data.clear()
            return

        for key_hash in titipan:
            print(f"  {self.data[key_hash][0]} (hash={key_hash}) pindah dari node {node_id} ke node {self.find_successor(key_hash)}")
        if not titipan:
            print("  Tidak ada key yang pindah")

    def find_successor(self, key_hash: int) -> int | None:
        """Cari node_id dengan nilai hash TERKECIL yang >= key_hash
        (successor menurut aturan Chord). Jika tidak ada, wrap-around
        ke node dengan hash terkecil di ring (karena ring melingkar)."""
        if not self.nodes:
            return None
        kandidat = [n for n in self.nodes if n >= key_hash]
        return min(kandidat) if kandidat else min(self.nodes)

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """Simpan mapping ID Kurir -> IP di node yang bertanggung jawab.
        Kalau kurir sudah terdaftar, IP lamanya ditimpa."""
        key_hash = hash_id(kurir_id)
        node_id = self.find_successor(key_hash)
        if node_id is None:
            print(f"[REGISTER] Gagal: ring masih kosong, {kurir_id} tidak bisa disimpan")
            return

        # ruang id cuma 256, jadi dua kurir bisa saja dapat hash yang sama
        lama = self.data.get(key_hash)
        if lama and lama[0] != kurir_id:
            print(f"[REGISTER] Gagal: hash {key_hash} sudah dipakai {lama[0]}")
            return

        self.data[key_hash] = (kurir_id, ip_kurir)
        print(f"[REGISTER] {kurir_id} (hash={key_hash}) -> {ip_kurir}, disimpan di node {node_id}")

    def lookup(self, kurir_id: str) -> str | None:
        """Cari alamat IP terkini untuk sebuah ID Kurir."""
        key_hash = hash_id(kurir_id)
        node_id = self.find_successor(key_hash)
        if node_id is None:
            return None

        print(f"[LOOKUP] {kurir_id} (hash={key_hash}) ditangani node {node_id}")
        entry = self.data.get(key_hash)
        if entry is None or entry[0] != kurir_id:
            return None
        return entry[1]

    def tampilkan_ring(self):
        """Print isi ring: tiap node dan kurir yang jadi tanggung jawabnya."""
        for node_id in sorted(self.nodes):
            kurir = [f"{self.data[k][0]}({k})" for k in sorted(self.data)
                     if self.find_successor(k) == node_id]
            print(f"  node {node_id} ({self.nodes[node_id]}): {', '.join(kurir) or '-'}")


def main():
    ring = ChordRing()

    # Skenario awal: 4 node bergabung
    ring.join("node-jakarta-1", "10.0.0.1")
    ring.join("node-jakarta-2", "10.0.0.2")
    ring.join("node-bandung-1", "10.0.0.3")
    ring.join("node-surabaya-1", "10.0.0.4")

    # Daftarkan 12 kurir. Kalau cuma kurir-001 s/d 003, tidak ada key yang
    # kena dampak saat node-medan-1 masuk atau node-jakarta-1 keluar.
    print()
    for i in range(1, 13):
        ring.register_kurir(f"kurir-{i:03d}", f"192.168.1.{9 + i}")

    print("\n--- Isi ring awal ---")
    ring.tampilkan_ring()

    print("\n--- Lookup sebelum perubahan topologi ---")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))
    print("kurir-012 ->", ring.lookup("kurir-012"))
    print("kurir-005 ->", ring.lookup("kurir-005"))

    print("\n--- Node baru bergabung ---")
    ring.join("node-medan-1", "10.0.0.5")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-012 ->", ring.lookup("kurir-012"))
    ring.tampilkan_ring()

    print("\n--- Sebuah node keluar ---")
    ring.leave("node-jakarta-1")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))
    print("kurir-005 ->", ring.lookup("kurir-005"))
    print("kurir-009 ->", ring.lookup("kurir-009"))
    ring.tampilkan_ring()

    print("\n--- IP kurir berubah ---")
    ring.register_kurir("kurir-001", "192.168.7.25")
    print("kurir-001 ->", ring.lookup("kurir-001"))


if __name__ == "__main__":
    main()
