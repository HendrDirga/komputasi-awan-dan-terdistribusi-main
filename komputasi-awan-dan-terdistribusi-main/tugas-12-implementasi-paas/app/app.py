"""
Tugas 12 - Aplikasi Flask sederhana untuk dideploy ke platform PaaS.
"""

import os
import datetime
from flask import Flask, jsonify

app = Flask(__name__)

NAMA_KELOMPOK = "TODO: isi nama kelompok kalian"


@app.route("/")
def index():
    # TODO 1: kembalikan response yang menampilkan NAMA_KELOMPOK dan
    # waktu server saat ini (datetime.datetime.now()).
    return f"TODO: tampilkan info kelompok - {NAMA_KELOMPOK}"


@app.route("/health")
def health():
    # TODO 2: kembalikan JSON status sehat, mis. {"status": "ok", "timestamp": ...}
    return jsonify({"status": "TODO"})


if __name__ == "__main__":
    # Platform PaaS umumnya menyediakan PORT lewat environment variable.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
