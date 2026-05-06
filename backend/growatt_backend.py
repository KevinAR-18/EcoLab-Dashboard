"""Client Growatt cloud untuk kebutuhan dashboard utama EcoLab."""

import growattServer

from config.firebase_settings import get_required_env


class GrowattBackend:
    """Mengambil metric inverter dan storage dari Growatt cloud API."""

    def __init__(self):
        """Login sekali ke Growatt API lalu menyiapkan plant ID aktif."""
        # Credential disimpan di `.env` agar build desktop tetap aman di luar Git.
        self.username = get_required_env("ECOLAB_GROWATT_USERNAME")
        self.password = get_required_env("ECOLAB_GROWATT_PASSWORD")

        self.api = growattServer.GrowattApi(
            agent_identifier="ShinePhone/8.1.17 (Android)"
        )

        # Login sekali saat startup lalu reuse client yang sama untuk polling.
        self.api.login(self.username, self.password)
        self.plant_id = self.api.plant_list_two()[0]["id"]

    def fetch(self) -> dict:
        """Mengambil satu snapshot storage lalu menormalkannya untuk dashboard."""
        devices = self.api.device_list(self.plant_id)

        storage_sn = None
        for device in devices:
            if device.get("deviceType") == "storage":
                storage_sn = device.get("deviceSn")
                break

        if not storage_sn:
            raise RuntimeError("Storage device tidak ditemukan")

        storage = self.api.storage_params(storage_sn)["storageDetailBean"]

        # Nilai power dipakai pada halaman utama energy flow.
        pv_power = int(storage.get("ppv2", 0))
        grid_import = int(storage.get("pAcInPut", 0))
        battery_power = float(storage.get("pBat", 0))
        soc = int(storage.get("capacity", 0))
        load_power = int(storage.get("outPutPower", 0))
        rate_va = int(storage.get("rateVA", 0))

        # Counter harian dan total dipakai oleh summary label serta popup detail.
        pv_today = float(storage.get("epvToday", 0))
        pv_total = float(storage.get("epvTotal", 0))

        charge_today = float(storage.get("eChargeToday", 0))
        charge_total = round(float(storage.get("eChargeTotal", 0)), 1)

        discharge_today = float(storage.get("eDischargeToday", 0))
        discharge_total = float(storage.get("eDischargeTotal", 0))

        load_today = float(storage.get("eopDischrToday", 0))
        load_total = float(storage.get("eopDischrTotal", 0))

        grid_today = (
            float(storage.get("eacChargeToday", 0))
            + float(storage.get("eacDisChargeToday", 0))
        )
        grid_total = (
            float(storage.get("eacChargeTotal", 0))
            + float(storage.get("eacDisChargeTotal", 0))
        )

        # Popup memakai subset data yang lebih detail dari payload yang sama.
        storage_popup = self.api.storage_params(storage_sn)["storageDetailBean"]
        flow_info = {
            "battery_voltage": storage_popup.get("vBat"),
            "pv1_voltage": storage_popup.get("vpv"),
            "pv2_voltage": storage_popup.get("vpv2"),
            "pv1_charge_current": storage_popup.get("iChargePV1"),
            "pv2_charge_current": storage_popup.get("iChargePV2"),
            "rateVA": storage_popup.get("rateVA"),
            "total_charge_current": storage_popup.get("chgCurr"),
            "ac_input_voltage": storage_popup.get("vGrid"),
            "ac_input_frequency": storage_popup.get("freqGrid"),
            "ac_output_voltage": storage_popup.get("outPutVolt"),
            "ac_output_frequency": storage_popup.get("freqOutPut"),
            "consumption_power": storage_popup.get("outPutPower"),
            "load_percentage": storage_popup.get("loadPercent"),
        }

        return {
            "pv_power": pv_power,
            "grid_import_power": grid_import,
            "battery_power": battery_power,
            "load_power": load_power,
            "rateVA_power": rate_va,
            "soc": soc,
            "pv_today": pv_today,
            "pv_total": pv_total,
            "battery_charge_today": charge_today,
            "battery_charge_total": charge_total,
            "battery_discharge_today": discharge_today,
            "battery_discharge_total": discharge_total,
            "load_today": load_today,
            "load_total": load_total,
            "grid_today": grid_today,
            "grid_total": grid_total,
            "flow_info": flow_info,
        }
