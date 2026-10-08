import subprocess
import os
import sys
import time

# ==========================================
# BAGIAN 1: KONFIGURASI UTAMA (UBAH DI SINI)
# ==========================================
# Masukkan alamat dompet Tidecoin (TDC) Anda yang valid
WALLET_ADDRESS = "TVq2k9N8HQ7RH4h1J6LRsykfYhqMn4hQeR"

# Masukkan URL Stratum Pool Rplant untuk Tidecoin
POOL_URL = "stratum+tcp://stratum-eu.rplant.xyz:7059"

# Berikan nama untuk perangkat worker Anda (Bebas)
WORKER_NAME = "UbuntuPythonWorker"

# Jumlah inti CPU yang digunakan (Kosongkan atau sesuaikan)
CPU_THREADS = "4"

# ==========================================
# BAGIAN 2: LOGIKA EKSEKUSI BINER C
# ==========================================
# Skrip ini memanggil berkas biner bernama 'rplant' di folder yang sama
binary_path = "./rplant"

if not os.path.exists(binary_path):
    print(f"Error: Berkas biner '{binary_path}' tidak ditemukan!")
    sys.exit(1)

# Menyusun argumen perintah miner
arguments = [
    binary_path,
    "-a", "yespowerTIDE",
    "-o", POOL_URL,
    "-u", f"{WALLET_ADDRESS}.{WORKER_NAME}",
    "-t", CPU_THREADS
]

print("=== Memulai Otomatisasi Penambangan via bot.py ===")

try:
    # Menjalankan biner C di latar belakang dan membaca log secara real-time
    process = subprocess.Popen(
        arguments,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    for line in iter(process.stdout.readline, ''):
        log = line.strip()
        print(f"[Miner]: {log}")
        
        # Logika otomatisasi tambahan (jika ada)
        if "accepted" in log.lower():
            print(">>> [Bot Info]: Selamat! Hash diterima oleh Pool.")

except KeyboardInterrupt:
    print("\n[Bot]: Menghentikan aktivitas miner secara aman...")
    process.terminate()
    sys.exit(0)
