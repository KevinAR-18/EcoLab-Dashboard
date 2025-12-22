# install: pip install tinytuya
import tinytuya
import time
import json

# ganti ini dengan data perangkatmu
DEVICE_ID = "a366ecc0ab15070f5dtf9x"
DEVICE_IP = "202.43.94.33"
LOCAL_KEY = "p1758594750818nj8ycn"

# buat object device (tipe device bisa apa saja)
d = tinytuya.BulbDevice(DEVICE_ID, DEVICE_IP, LOCAL_KEY)  # BulbDevice sering dipakai; untuk sensor hasil get_status sama
d.set_version(3.3)  # coba 3.1 atau 3.3 tergantung versi perangkat

def read_status():
    try:
        data = d.status()  # memanggil DP/Status dari device secara lokal
        # data berupa dict; print seluruh data dulu untuk lihat dp id untuk suhu
        print(json.dumps(data, indent=2))
        # contoh ambil nilai spesifik jika perangkat mengembalikan dp tertentu:
        # mis. jika temperatur berada di data['dps']['20'], ambil seperti:
        # temp = data['dps'].get('20')
        # print("Temperature:", temp)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    while True:
        read_status()
        time.sleep(10)
