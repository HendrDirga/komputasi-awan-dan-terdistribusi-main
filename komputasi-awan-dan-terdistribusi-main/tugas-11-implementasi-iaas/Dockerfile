# Simulasi "VM Linux kustom" - pakai base image OS penuh, BUKAN slim/alpine,
# supaya mendekati pengalaman provisioning VM (banyak tool tersedia).
FROM ubuntu:22.04

# TODO 1: install tool yang dibutuhkan script otomasi kalian.
# Contoh (sesuaikan dengan skenario yang dipilih):
#   RUN apt-get update && apt-get install -y cron rsync curl && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y __ISI_PACKAGE_YANG_DIBUTUHKAN__ && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/provision

COPY provision.sh .
RUN chmod +x provision.sh

# TODO 2: tentukan entrypoint yang menjalankan provision.sh saat container start
# (simulasi user-data script yang jalan otomatis saat VM cloud pertama kali menyala).
ENTRYPOINT ["./provision.sh"]
