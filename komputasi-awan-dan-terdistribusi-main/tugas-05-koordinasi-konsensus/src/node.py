"""
Tugas 5 - Simulasi Node untuk Bully Algorithm

Jalankan 5 node pada terminal terpisah:
    python3 node.py --id 1 --port 5001 --peers 5002,5003,5004,5005
    python3 node.py --id 2 --port 5002 --peers 5001,5003,5004,5005
    python3 node.py --id 3 --port 5003 --peers 5001,5002,5004,5005
    python3 node.py --id 4 --port 5004 --peers 5001,5002,5003,5005
    python3 node.py --id 5 --port 5005 --peers 5001,5002,5003,5004
"""

import argparse
import socket
import threading
import time

ELECTION_TIMEOUT = 2.0
CONNECT_TIMEOUT = 0.7
MONITOR_INTERVAL = 2.0


class Node:
    def __init__(self, node_id: int, port: int, peers: dict):
        self.node_id = node_id
        self.port = port
        self.peers = peers  
        self.leader_id = None

        self.lock = threading.RLock()
        self.election_lock = threading.Lock()
        self.election_in_progress = False
        self.ok_received = threading.Event()
        self.coordinator_received = threading.Event()
        self.last_leader_contact = 0.0

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", self.port))
        server.listen()
        print(f"[Node {self.node_id}] Listening di port {self.port}", flush=True)

        while True:
            try:
                conn, _ = server.accept()
                threading.Thread(
                    target=self.handle_connection,
                    args=(conn,),
                    daemon=True,
                ).start()
            except OSError as exc:
                print(f"[Node {self.node_id}] Kesalahan server: {exc}", flush=True)

    def handle_connection(self, conn: socket.socket):
        with conn:
            try:
                conn.settimeout(CONNECT_TIMEOUT)
                data = conn.recv(1024).decode("utf-8").strip()
                if not data:
                    return

                parts = data.split(":", 1)
                if len(parts) != 2:
                    return

                sender_id = int(parts[0])
                msg_type = parts[1]

                
                response = self.on_message(sender_id, msg_type)
                if response:
                    conn.sendall(response.encode("utf-8"))
            except (ValueError, OSError, socket.timeout) as exc:
                print(f"[Node {self.node_id}] Koneksi/pesan tidak valid: {exc}", flush=True)

    def send_message(self, target_port: int, msg_type: str) -> bool:
        """Kirim pesan dan tunggu balasan protokol jika ada."""
        try:
            with socket.create_connection(
                ("localhost", target_port), timeout=CONNECT_TIMEOUT
            ) as sock:
                sock.settimeout(CONNECT_TIMEOUT)
                sock.sendall(f"{self.node_id}:{msg_type}".encode("utf-8"))
                
                if msg_type in ("PING", "ELECTION"):
                    response = sock.recv(1024).decode("utf-8").strip()
                    if msg_type == "PING":
                        return response == f"{target_port - 5000}:PONG"
                    if msg_type == "ELECTION":
                        expected_ok = f"{target_port - 5000}:OK"
                        if response == expected_ok:
                            print(
                                f"[Node {self.node_id}] Menerima OK dari Node "
                                f"{target_port - 5000}",
                                flush=True,
                            )
                            self.ok_received.set()
                            return True
                        return False

                return True
        except (ConnectionRefusedError, socket.timeout, OSError):
            return False


    def on_message(self, sender_id: int, msg_type: str):
        """Proses pesan masuk dan kembalikan respons bila diperlukan."""
        if msg_type == "ELECTION":
            print(
                f"[Node {self.node_id}] Menerima ELECTION dari Node {sender_id}",
                flush=True,
            )
            if self.node_id > sender_id:
                
                threading.Thread(
                    target=self.start_election, daemon=True
                ).start()
                return f"{self.node_id}:OK"
            return None

        if msg_type == "OK":
            print(f"[Node {self.node_id}] Menerima OK dari Node {sender_id}", flush=True)
            self.ok_received.set()
            return None

        if msg_type == "COORDINATOR":
            if sender_id < self.node_id:
                print(
                    f"[Node {self.node_id}] Mengabaikan COORDINATOR dari Node "
                    f"{sender_id} (ID lebih rendah)",
                    flush=True,
                )
                
                threading.Thread(target=self.start_election, daemon=True).start()
                return None

            with self.lock:
                previous = self.leader_id
                self.leader_id = sender_id
                self.last_leader_contact = time.monotonic()

            self.coordinator_received.set()
            if previous != sender_id:
                print(
                    f"[Node {self.node_id}] Leader diperbarui: Node {sender_id}",
                    flush=True,
                )
            return None

        if msg_type == "PING":
            return f"{self.node_id}:PONG"

        if msg_type == "PONG":
            return None

        print(
            f"[Node {self.node_id}] Pesan tidak dikenal: '{msg_type}' "
            f"dari Node {sender_id}",
            flush=True,
        )
        return None

    def start_election(self):
        """Jalankan satu election pada satu waktu."""
        if not self.election_lock.acquire(blocking=False):
            return

        try:
            with self.lock:
                
                if self.leader_id == self.node_id:
                    return
                self.election_in_progress = True
                self.ok_received.clear()
                self.coordinator_received.clear()

            higher_peers = {
                peer_id: peer_port
                for peer_id, peer_port in self.peers.items()
                if peer_id > self.node_id
            }
            print(
                f"[Node {self.node_id}] Memulai election; "
                f"peer lebih tinggi: {list(higher_peers)}",
                flush=True,
            )

            
            if not higher_peers:
                self.declare_leader()
                return

            
            higher_responded = False
            for peer_id, peer_port in higher_peers.items():
                if self.send_message(peer_port, "ELECTION"):
                    higher_responded = True

            if not higher_responded:
                
                self.declare_leader()
                return

            
            if self.ok_received.wait(ELECTION_TIMEOUT):
                
                if not self.coordinator_received.wait(ELECTION_TIMEOUT * 2):

                    with self.lock:
                        known_leader = self.leader_id
                    if known_leader is None or known_leader < self.node_id:
                        print(
                            f"[Node {self.node_id}] Belum menerima COORDINATOR; "
                            "akan mencoba election lagi",
                            flush=True,
                        )
                        
                        threading.Thread(
                            target=self.start_election, daemon=True
                        ).start()
            else:
                
                higher_alive = any(
                    self.send_message(port, "PING")
                    for port in higher_peers.values()
                )
                if not higher_alive:
                    self.declare_leader()
                else:
                    print(
                        f"[Node {self.node_id}] Node lebih tinggi aktif, "
                        "menunggu COORDINATOR",
                        flush=True,
                    )
        finally:
            with self.lock:
                self.election_in_progress = False
            self.election_lock.release()

    def declare_leader(self):
        """Jadikan node sebagai leader dan umumkan kepada semua peer."""
        with self.lock:
            if self.leader_id == self.node_id:
                return
            self.leader_id = self.node_id
            self.last_leader_contact = time.monotonic()

        print(f"[Node {self.node_id}] Menjadi LEADER", flush=True)

        for peer_id, peer_port in self.peers.items():
            if self.send_message(peer_port, "COORDINATOR"):
                print(
                    f"[Node {self.node_id}] COORDINATOR dikirim ke Node {peer_id}",
                    flush=True,
                )

    def monitor_leader(self):
        """Pantau leader; jika gagal, mulai election."""
        while True:
            time.sleep(MONITOR_INTERVAL)

            with self.lock:
                current_leader = self.leader_id

            if current_leader is None:
                self.start_election()
                continue

            if current_leader == self.node_id:
                continue

            leader_port = self.peers.get(current_leader)
            alive = (
                leader_port is not None
                and self.send_message(leader_port, "PING")
            )

            if alive:
                with self.lock:
                    if self.leader_id == current_leader:
                        self.last_leader_contact = time.monotonic()
                continue

            with self.lock:
               
                if self.leader_id == current_leader:
                    self.leader_id = None

            print(
                f"[Node {self.node_id}] Leader Node {current_leader} "
                "tidak merespons; memulai election",
                flush=True,
            )
            self.start_election()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=int, required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument(
        "--peers",
        type=str,
        required=True,
        help="daftar port peer dipisah koma, mis. 5002,5003,5004,5005",
    )
    args = parser.parse_args()

    peer_ports = [int(p.strip()) for p in args.peers.split(",") if p.strip()]
    peers = {port - 5000: port for port in peer_ports}

    if args.port != 5000 + args.id:
        parser.error("Konvensi tugas: port harus 5000 + ID node.")
    if args.id in peers:
        parser.error("Daftar --peers tidak boleh berisi port node itu sendiri.")

    node = Node(args.id, args.port, peers)

    threading.Thread(target=node.start_server, daemon=True).start()
    time.sleep(0.3)
    threading.Thread(target=node.monitor_leader, daemon=True).start()

    time.sleep(1.0)
    node.start_election()

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print(f"\n[Node {node.node_id}] Dihentikan.", flush=True)


if __name__ == "__main__":
    main()
