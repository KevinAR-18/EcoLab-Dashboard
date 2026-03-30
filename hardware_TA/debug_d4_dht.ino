/**
 * Debug D4 - Cek Input dari DHT
 * Wemos D1 Mini - ESP8266
 *
 * Untuk mengecek apakah DHT mengirim sinyal ke pin D4
 */

#define PIN_D4 D4  // GPIO2

void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(PIN_D4, INPUT);

  Serial.println("=== DEBUG D4 (GPIO2) ===");
  Serial.println("Mendeteksi input DHT di pin D4...");
  Serial.println();
  Serial.println("HIGH = Tidak ada sinyal");
  Serial.println("LOW  = Ada sinyal/data");
  Serial.println();

  Serial.println("Wiring DHT ke Wemos:");
  Serial.println("  DHT VCC  -> 3V3");
  Serial.println("  DHT DATA -> D4");
  Serial.println("  DHT GND  -> GND");
  Serial.println();
  Serial.println("Monitor dibawah...\n");
}

void loop() {
  int state = digitalRead(PIN_D4);

  if (state == HIGH) {
    Serial.print("[HIGH] ");
  } else {
    Serial.print("[LOW]  ");
  }

  // Tampilkan waktu
  Serial.print(millis());
  Serial.println(" ms");

  delay(100);  // Baca setiap 100ms
}
