import growattServer
import getpass
import time
import datetime
import os

# ================= LOGIN =================
username = input("Username Growatt: ")
password = getpass.getpass("Password: ")

api = growattServer.GrowattApi(
    agent_identifier="ShinePhone/8.1.17 (Android)"
)

print("\n🔄 Login...")
api.login(username, password)

plant_id = api.plant_list_two()[0]["id"]

print("✅ Login OK | Plant ID:", plant_id)

# ================= LOOP =================
while True:
    try:
        energy = api.plant_energy_data(plant_id)
        devices = api.device_list(plant_id)

        # cari storage
        storage_sn = None
        for d in devices:
            if d["deviceType"] == "storage":
                storage_sn = d["deviceSn"]
                break

        storage = api.storage_params(storage_sn)["storageDetailBean"]

        # ================= FILTER DATA =================
        pv_power = storage.get("ppv2", 0)
        grid_import = storage.get("pAcInPut", 0)
        pbat = storage.get("pBat", 0)
        soc = storage.get("capacity", 0)
        load_power = storage.get("outPutPower", 0)

        pv_today = storage.get("epvToday", 0)
        pv_total = storage.get("epvTotal", 0)

        dis_today = storage.get("eDischargeToday", 0)
        dis_total = storage.get("eDischargeTotal", 0)

        chg_today = storage.get("eChargeToday", 0)
        chg_total = storage.get("eChargeTotal", 0)

        load_today = storage.get("eopDischrToday", 0)
        load_total = storage.get("eopDischrTotal", 0)
        
        # GRID ENERGY
        grid_today = (
            storage.get("eacChargeToday", 0) +
            storage.get("eacDisChargeToday", 0)
        )

        grid_total = (
            storage.get("eacChargeTotal", 0) +
            storage.get("eacDisChargeTotal", 0)
        )


        # ================= CLEAR =================
        os.system("cls" if os.name == "nt" else "clear")

        # ================= DISPLAY =================
        print("📊 ECOLAB SYSTEM DIAGRAM")
        print("⏱️ ", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("=" * 45)

        print("☀️ PV POWER")
        print(f"   Power      : {pv_power} W")
        print(f"   Today      : {pv_today} kWh")
        print(f"   Total      : {pv_total} kWh\n")

        print("🔌 GRID")
        print(f"   Import     : {grid_import} W\n")

        print("🔋 BATTERY")
        print(f"   SoC        : {soc} %")

        if pbat < 0:
            print(f"   Charging   : {abs(pbat)} W")
        else:
            print(f"   Discharge  : {pbat} W")

        print(f"   Chg Today  : {chg_today} kWh")
        print(f"   Chg Total  : {chg_total} kWh")
        print(f"   Dis Today  : {dis_today} kWh")
        print(f"   Dis Total  : {dis_total} kWh\n")

        print("💡 LOAD")
        print(f"   Power      : {load_power} W")
        print(f"   Today      : {load_today} kWh")
        print(f"   Total      : {load_total} kWh")
        
        print("🔌 GRID")
        print(f"   Import Power : {grid_import} W")
        print(f"   Today Energy : {grid_today} kWh")
        print(f"   Total Energy : {grid_total} kWh\n")


        print("\n🔁 Refresh 10 detik | Ctrl+C keluar")

        time.sleep(10)

    except KeyboardInterrupt:
        print("\n🛑 Dihentikan user")
        break

    except Exception as e:
        print("⚠️ Error:", e)
        time.sleep(5)
