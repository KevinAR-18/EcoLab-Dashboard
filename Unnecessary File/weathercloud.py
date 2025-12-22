import requests
import time
import os # Untuk membersihkan terminal

# --- Konfigurasi ---
URL_DATA = "https://app.weathercloud.net/device/values/5476957392"
DELAY_SECONDS = 2 # Delay antar pembaruan
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://app.weathercloud.net/device/5476957392",
    "Accept": "application/json, text/javascript, */*; q=0.01",
}
# ---------------------

def clear_terminal():
    """Membersihkan terminal (untuk Windows dan Linux/macOS)"""
    # 'cls' untuk Windows, 'clear' untuk Linux/macOS
    os.system('cls' if os.name == 'nt' else 'clear')

def fetch_and_display_data():
    """Mengambil data dari API dan menampilkannya di terminal"""
    try:
        # 1. Melakukan permintaan GET
        r = requests.get(URL_DATA, headers=HEADERS)

        # 2. Membersihkan terminal untuk tampilan real-time
        clear_terminal()

        print(f"--- Pembaruan Data Cuaca | Terakhir: {time.strftime('%H:%M:%S')} ---")
        print(f"Status Code: {r.status_code}")

        # 3. Memproses response
        if r.status_code == 200:
            try:
                # Coba parse JSON
                data = r.json()
                print("\n=== Data Cuaca Diterjemahkan ===")
                for key, value in data.items():
                    # Format tampilan lebih rapi
                    print(f"- {key.replace('_', ' ').title()}: {value}")
            except Exception:
                # Jika bukan JSON valid
                print("\n⚠️ Data bukan JSON valid, tampilkan teks mentah:")
                print(r.text)
        else:
            print(f"⚠️ Gagal mendapatkan data. Response code: {r.status_code}")

    except requests.exceptions.RequestException as e:
        # Menangani error koneksi, DNS, dll.
        print(f"Terjadi Error Jaringan: {e}")
    except Exception as e:
        # Menangani error lain
        print(f"Terjadi Error Tak Terduga: {e}")

# --- Loop Utama ---
print(f"Memulai pembaruan data setiap {DELAY_SECONDS} detik. Tekan Ctrl+C untuk menghentikan.")
try:
    # Loop tak terbatas
    while True:
        fetch_and_display_data() # Panggil fungsi untuk ambil dan tampilkan data
        time.sleep(DELAY_SECONDS) # Jeda selama 10 detik

except KeyboardInterrupt:
    # Menangani ketika pengguna menekan Ctrl+C
    clear_terminal()