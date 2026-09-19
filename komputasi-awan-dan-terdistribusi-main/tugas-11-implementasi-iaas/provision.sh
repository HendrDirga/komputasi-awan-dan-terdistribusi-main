#!/bin/bash
# Tugas 11 - Script Otomasi Perusahaan
#
# Pilih SATU skenario di bawah (atau buat versi kalian sendiri, jelaskan di README.md):
#   1. Backup otomatis terjadwal
#   2. Log rotation & cleanup
#   3. Health check periodik
#
# Skeleton ini memberi kerangka umum. Isi TODO sesuai skenario pilihan kelompok.

set -euo pipefail

LOG_FILE="/opt/provision/provision.log"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log "Provisioning dimulai - simulasi VM baru menyala"

# TODO 1: implementasikan skenario otomasi yang kalian pilih di sini.
# Contoh skenario Backup:
#   SOURCE_DIR="/data/penting"
#   BACKUP_DIR="/data/backup"
#   mkdir -p "$SOURCE_DIR" "$BACKUP_DIR"
#   cp -r "$SOURCE_DIR"/* "$BACKUP_DIR/backup-$(date +%Y%m%d-%H%M%S)/" 2>/dev/null || true
#   log "Backup selesai ke $BACKUP_DIR"
#
# Contoh skenario Log Rotation:
#   LOG_DIR="/var/log/aplikasi"
#   find "$LOG_DIR" -type f -mtime +7 -exec rm {} \;
#   log "Log lebih dari 7 hari dibersihkan"
#
# Contoh skenario Health Check:
#   while true; do
#     if ! curl -sf http://localhost:8000/health > /dev/null; then
#       log "PERINGATAN: service tidak merespons!"
#     else
#       log "Service sehat"
#     fi
#     sleep 30
#   done

log "TODO: implementasikan skenario otomasi yang dipilih kelompok"

log "Provisioning selesai"

# Jaga container tetap hidup agar bisa diamati (hapus baris ini jika skenario
# kalian memang dimaksudkan untuk exit setelah selesai, mis. one-shot backup).
tail -f /dev/null
