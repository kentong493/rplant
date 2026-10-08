import requests
import json
import time
import os

def verify_api_key(api_key):
    """Melakukan verifikasi awal (login) menggunakan API Key."""
    endpoint = "https://recordedfuture.com"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("[*] Tahap 1: Memverifikasi API Key Anda...")
    try:
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            print("[+] LOGIN SUKSES! API Key Terverifikasi.")
            print(f"[*] Pengguna: {user_data.get('username', 'N/A')} ({user_data.get('email', 'N/A')})")
            print("-" * 60)
            return True
        elif response.status_code == 401:
            print("[-] LOGIN GAGAL: API Key tidak valid. Periksa kembali!")
            return False
        else:
            print(f"[-] Gagal verifikasi. Status Code: {response.status_code}")
            return False
    except Exception as e:
        print(f"[-] Terjadi kesalahan koneksi saat verifikasi: {e}")
        return False

def submit_url_to_triage(api_key, target_url):
    """Mengirimkan satu URL ke Recorded Future Triage."""
    endpoint = "https://recordedfuture.com"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "kind": "url",
        "url": target_url
    }
    
    try:
        response = requests.post(endpoint, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            print(f"[+] SUKSES | URL: {target_url} | ID Analisis: {result.get('id')}")
            return True
        else:
            print(f"[-] GAGAL  | URL: {target_url} | Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"[-] ERROR  | URL: {target_url} | Keterangan: {e}")
        return False

def start_auto_submit_process(api_key, file_path):
    """Menjalankan alur integrasi dengan jeda 10 menit setiap 2 submit."""
    if not verify_api_key(api_key):
        print("[-] Proses dihentikan karena masalah autentikasi API Key.")
        return

    if not os.path.exists(file_path):
        print(f"[-] Error: File '{file_path}' tidak ditemukan!")
        return

    print(f"[*] Tahap 2: Membaca daftar URL dari '{file_path}'...")
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
        
    total_urls = len(urls)
    if total_urls == 0:
        print("[-] File 'urls.txt' kosong. Tidak ada URL untuk dikirim.")
        return
        
    print(f"[*] Ditemukan {total_urls} URL. Memulai pengiriman otomatis...")
    print("=" * 60)
    
    for index, url in enumerate(urls, 1):
        print(f"[{index}/{total_urls}] Sedang mengirim...")
        submit_url_to_triage(api_key, url)
        
        # Logika Jeda: Jika sudah mengirim 2 URL dan BUKAN URL terakhir di dalam daftar
        if index % 2 == 0 and index < total_urls:
            print("\n[!] Sudah mengirim 2 URL. Mengaktifkan jeda aman...")
            # Melakukan hitung mundur menit demi menit agar Termux terlihat tetap aktif
            for menit_tersisa in range(10, 0, -1):
                print(f"[*] Menunggu waktu jeda... Sisa: {menit_tersisa} menit lagi.", end="\r")
                time.sleep(60)
            print("\n[+] Jeda selesai. Melanjutkan pengiriman berikutnya...\n" + "-"*40)
        
        # Jeda standar 2 detik antar URL biasa (jika belum mencapai kelipatan 2)
        elif index < total_urls:
            time.sleep(2)
            
    print("=" * 60)
    print("[+] Selesai! Semua tugas dalam file telah diproses.")

# --- Pengaturan Utama ---
if __name__ == "__main__":
    # Ganti dengan API Key milik Anda
    MY_API_KEY = "3c506a4497d84d04d97110ccddc307b2d37feb8e"
    FILE_TARGET = "urls.txt"
    
    start_auto_submit_process(MY_API_KEY, FILE_TARGET)
