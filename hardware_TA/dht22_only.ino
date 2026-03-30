/**
 * DHT22 Temperature & Humidity Sensor
 * Wemos D1 Mini - ESP8266
 *
 * Pin: D4 (GPIO2)
 * Library: Adafruit DHT sensor library
 */

#include <DHT.h>

// ----------- CONFIG -----------
#define DHTPIN D4         // Pin DHT22 (GPIO2)
#define DHTTYPE DHT22      // Tipe sensor

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  delay(1000);

  dht.begin();

  Serial.println("=== DHT22 Sensor ===");
  Serial.println("Pin: D4 (GPIO2)");
  Serial.println();
}

void loop() {
  delay(2000);  // Baca setiap 2 detik

  float h = dht.readHumidity();      // Kelembaban (%)
  float t = dht.readTemperature();   // Suhu (Celcius)

  // Cek error pembacaan
  if (isnan(h) || isnan(t)) {
    Serial.println("Gagal baca sensor!");
    return;
  }

  // Tampilkan data
  Serial.print("Suhu: ");
  Serial.print(t, 1);
  Serial.print(" *C | Kelembaban: ");
  Serial.print(h, 1);
  Serial.println(" %");
}
