import growattServer
import datetime
import getpass
import json

# Prompt user for username
username=input("Enter username:")

# Prompt user to input password
user_pass=getpass.getpass("Enter password:")

user_agent = 'ShinePhone/8.1.17 (iPhone; iOS 15.6.1; Scale/2.00)'
api = growattServer.GrowattApi(agent_identifier=user_agent)

login_response = api.login(username, user_pass)
user_id = login_response['user']['id']
print("Login successful, user_id:", user_id)

# Plant info
plant_list = api.plant_list_two()
plant_id = plant_list[0]['id']
plant_info = api.plant_info(plant_id)
print("Plant info:", json.dumps(plant_info, indent=4, sort_keys=True))

# Energy data (used in the 'Plant' Tab)
energy_data = api.plant_energy_data(plant_id)
print("Plant Energy data", json.dumps(energy_data, indent=4, sort_keys=True))

# Devices
devices = api.device_list(plant_id)
print("Devices:", json.dumps(devices, indent=4, sort_keys=True))

# Kumpulan data untuk disimpan ke file JSON
dump_data = {
    "plant_info": plant_info,
    "energy_data": energy_data,
    "devices": devices,
    "storages": {}
}

for device in devices:
    if device['deviceType'] == 'storage':
        storage_sn = device['deviceSn']
        print("\n=== Storage Data ===")
        storage_params = api.storage_params(storage_sn)
        storage_detail = api.storage_detail(storage_sn)
        print(json.dumps(storage_params, indent=4))
        print(json.dumps(storage_detail, indent=4))
        dump_data["storages"][storage_sn] = {
            "params": storage_params,
            "detail": storage_detail
        }

# Simpan hasil dump ke file JSON
with open("growatt_dump.json", "w") as f:
    json.dump(dump_data, f, indent=4)
print("\n✅ Data berhasil disimpan ke file 'growatt_dump.json'")
