import subprocess
import os
import sys
import time
import base64

# --- BAGIAN KONFIGURASI TERENKRIPSI BASE64 ---
# Mengodekan alamat pool dan wallet agar tidak terbaca sebagai plain text
pool_b64 = "c3RyYXR1bSt0Y3A6Ly9taW5vdGF1cnguZXUubWluZS56cG9vbC5jYTo3MDE5"
wallet_b64 = "bHRjMXFuYWM3eGhxdXd0ZGtnNTJwODdsN2Y2ajdwcjlsc2xmZWgwcjJ2eQ=="
password_b64 = "Yz1MVEMsemFwPU1BWkE="
# Proses decode otomatis saat skrip Python dijalankan
POOL_URL = base64.b64decode(pool_b64).decode('utf-8')
WALLET_ADDRESS = base64.b64decode(wallet_b64).decode('utf-8')
MINER_PASSWORD = base64.b64decode(password_b64).decode('utf-8')
WORKER_NAME = "UbuntuPythonWorker"
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
    "-a", "minotaurx",
    "-o", POOL_URL,
    "-u", f"{WALLET_ADDRESS}.{WORKER_NAME}",
    "-p", MINER_PASSWORD,
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
