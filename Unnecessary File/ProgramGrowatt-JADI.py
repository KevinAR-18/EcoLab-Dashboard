import growattServer
import datetime
import getpass
import os
import time

# === Fungsi bantu format angka kWh ===
def format_kwh_string(value):
    """
    Ambil string seperti '611.8000000000001 kWh' atau '609kWh'
    → ubah jadi '611.8 kWh'
    """
    if not isinstance(value, str):
        return "-"
    # ambil hanya angka dan titik
    clean = ''.join(ch for ch in value if (ch.isdigit() or ch == '.'))
    try:
        return f"{float(clean):.1f} kWh"
    except:
        return value

# === LOGIN ===
username = input("Enter username: ")
user_pass = getpass.getpass("Enter password: ")

user_agent = 'ShinePhone/8.1.17 (iPhone; iOS 15.6.1; Scale/2.00)'
api = growattServer.GrowattApi(agent_identifier=user_agent)

print("🔄 Login ke server Growatt...")
login_response = api.login(username, user_pass)
user_id = login_response['user']['id']
print("✅ Login berhasil! User ID:", user_id)

# === AMBIL PLANT ID ===
print("📡 Mengambil daftar plant...")
plant_list = api.plant_list_two()
plant_id = plant_list[0]['id']
print(f"📍 Plant ID: {plant_id}")

# === LOOP DASHBOARD ===
while True:
    try:
        # Ambil data
        energy_data = api.plant_energy_data(plant_id)
        devices = api.device_list(plant_id)

        # Cari storage
        storages = {}
        for device in devices:
            if device['deviceType'] == 'storage':
                storage_sn = device['deviceSn']
                storage_params = api.storage_params(storage_sn)
                storages[storage_sn] = storage_params

        # Ambil data utama
        weather = energy_data.get("weatherMap", {})
        energy = energy_data
        device = devices[0]
        storage_sn = list(storages.keys())[0]
        storage = storages[storage_sn].get("storageDetailBean", {})

        # === Ekstraksi nilai ===
        temp = weather.get("tmp", "-")

        today_energy_fmt = format_kwh_string(energy.get("todayStr", "0"))
        total_energy_fmt = format_kwh_string(energy.get("totalStr", "0"))

        eChargeToday_fmt = format_kwh_string(storage.get("eChargeTodayText", "0"))
        eChargeTotal_fmt = format_kwh_string(storage.get("eChargeTotalText", "0"))

        eDischargeToday_fmt = format_kwh_string(storage.get("eDischargeTodayText", "0"))
        eDischargeTotal_fmt = format_kwh_string(storage.get("eDischargeTotalText", "0"))

        eopToday_fmt = format_kwh_string(str(storage.get("eopDischrToday", "0")))
        eopTotal_fmt = format_kwh_string(str(storage.get("eopDischrTotal", "0")))

        activePower = device.get("activePower", "-")
        pvPower = storage.get("ppv2","-")
        rateVA = storage.get("rateVA", "-")
        capacity = device.get("capacity", "-")
        

        # Filter pCharge agar selalu positif
        try:
            pCharge_val = abs(float(storage.get("pCharge", 0)))
        except:
            pCharge_val = "-"

        # Bersihkan layar
        os.system('cls' if os.name == 'nt' else 'clear')

        # === Dashboard ===
        print("📊 === DASHBOARD ECOLAB ===")
        print("⏱️ Update:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print(f"🌡️ Temperatur       : {temp}°C\n")
        
        print("☀️  PV Power")
        print(f"   PV Power      : {pvPower} W\n")

        print("☀️  Photovoltaic")
        print(f"   Hari ini         : {today_energy_fmt}")
        print(f"   Total            : {total_energy_fmt}\n")

        print("🔋 Charging")
        print(f"   Hari ini         : {eChargeToday_fmt}")
        print(f"   Total            : {eChargeTotal_fmt}\n")

        print("🔻 Discharging")
        print(f"   Hari ini         : {eDischargeToday_fmt}")
        print(f"   Total            : {eDischargeTotal_fmt}\n")

        print("💡 Load Consumption")
        print(f"   Hari ini         : {eopToday_fmt}")
        print(f"   Total            : {eopTotal_fmt}\n")

        print("⚡ Consumption Power")
        print(f"   {activePower} W / {rateVA} VA\n")

        print("🔌 Charging Power & SOC")
        print(f"   Power            : {pCharge_val} W")
        print(f"   Capacity         : {capacity}\n")

        print("🔁 Dashboard akan refresh setiap 10 detik...\nTekan Ctrl+C untuk keluar.")
        time.sleep(10)

    except KeyboardInterrupt:
        print("\n🛑 Monitoring dihentikan oleh user.")
        break
    except Exception as e:
        print("⚠️ Terjadi error:", e)
        time.sleep(10)
