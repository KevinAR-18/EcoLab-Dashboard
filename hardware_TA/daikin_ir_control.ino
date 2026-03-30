#include <IRremoteESP8266.h>
#include <IRsend.h>
#include <ir_Daikin.h>
#include <DHT.h>

// ----------- IR CONFIG -----------
const uint16_t kIrLed = D1;   // pin IR LED
IRDaikinESP ac(kIrLed);       // Objek Daikin AC

// ----------- DHT CONFIG -----------
const uint8_t dhtPin = D2;    // pin DHT22
#define DHTTYPE DHT22
DHT dht(dhtPin, DHTTYPE);

unsigned long lastDHTRead = 0;
const unsigned long dhtInterval = 2000;  // baca setiap 2 detik

String input = "";

// ----------- SETUP -----------
void setup() {
  Serial.begin(115200);

  ac.begin();
  dht.begin();

  // default kondisi awal
  ac.on();
  ac.setMode(kDaikinCool);
  ac.setTemp(24);
  ac.setFan(kDaikinFanAuto);
  ac.send();

  Serial.println("=== AC READY ===");
  Serial.println("Command:");
  Serial.println("ON / OFF");
  Serial.println("TEMP_UP / TEMP_DOWN");
  Serial.println("MODE_COOL / MODE_FAN");
}

// ----------- LOOP -----------
void loop() {
  // Baca DHT setiap 2 detik
  unsigned long currentMillis = millis();
  if (currentMillis - lastDHTRead >= dhtInterval) {
    lastDHTRead = currentMillis;
    readDHT();
  }

  // Baca serial command
  if (Serial.available()) {
    input = Serial.readStringUntil('\n');
    input.trim(); // hapus spasi / enter

    Serial.print("Command: ");
    Serial.println(input);

    if (input == "ON") {
      ac.on();
    }
    else if (input == "OFF") {
      ac.off();
    }
    else if (input == "MODE_COOL") {
      ac.setMode(kDaikinCool);
    }
    else if (input == "MODE_FAN") {
      ac.setMode(kDaikinFan);
    }
    else if (input == "TEMP_UP") {
      uint8_t t = ac.getTemp();
      if (t < 30) ac.setTemp(t + 1);
    }
    else if (input == "TEMP_DOWN") {
      uint8_t t = ac.getTemp();
      if (t > 18) ac.setTemp(t - 1);
    }

    // setting tambahan
    ac.setFan(kDaikinFanAuto);
    ac.setSwingVertical(false);

    // kirim IR
    ac.send();

    Serial.println("IR command sent!");
    Serial.print("Current Temp: ");
    Serial.println(ac.getTemp());
  }
}

// ----------- DHT FUNCTION -----------
void readDHT() {
  float temp = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temp) || isnan(humidity)) {
    Serial.println("Gagal baca DHT!");
    return;
  }

  Serial.print("Suhu: ");
  Serial.print(temp, 1);
  Serial.print(" C | Kelembaban: ");
  Serial.print(humidity, 1);
  Serial.println(" %");
}