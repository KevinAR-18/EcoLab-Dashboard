"""HTTP client untuk data WeatherCloud yang ditampilkan di dashboard."""

import requests


class WeatherCloudBackend:
    """Mengambil dan menormalkan payload public WeatherCloud device."""

    def __init__(self, device_id: str):
        """Menyimpan device ID, endpoint, dan header request WeatherCloud."""
        self.device_id = device_id
        self.url = f"https://app.weathercloud.net/device/values/{device_id}"

        # Endpoint public ini lebih stabil jika request-nya mirip browser biasa.
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/117.0.0.0 Safari/537.36"
            ),
            "X-Requested-With": "XMLHttpRequest",
            "Referer": f"https://app.weathercloud.net/device/{device_id}",
            "Accept": "application/json, text/javascript, */*; q=0.01",
        }

    def fetch(self) -> dict:
        """Memetakan response mentah WeatherCloud ke key yang ramah untuk UI."""
        response = requests.get(self.url, headers=self.headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            "temperature": data.get("temp"),
            "humidity": data.get("hum"),
            "pressure": data.get("bar"),
            "wind_speed": data.get("wspd"),
            "wind_speed_avg": data.get("wspdavg"),
            "wind_direction": data.get("wdir"),
            "rain_total": data.get("rain"),
            "rain_rate": data.get("rainrate"),
            "heat_index": data.get("heat"),
        }
