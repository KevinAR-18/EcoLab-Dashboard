#include <PZEM004Tv30.h>
#include <HardwareSerial.h>
#include <DS1302.h>

// ================= OUTPUT =================
#define RELAY_PIN 7
#define RED_LED_PIN 8
#define GREEN_LED_PIN 9
#define BLUE_LED_PIN 10

// ================= RTC =================
#define RTC_CE 4
#define RTC_IO 3
#define RTC_SCLK 2
DS1302 rtc(RTC_CE, RTC_IO, RTC_SCLK);

// ================= PZEM =================
#define PZEM_RX_PIN 5   // ESP32 RX <- PZEM TX
#define PZEM_TX_PIN 6   // ESP32 TX -> PZEM RX
HardwareSerial PZEMSerial(1);
PZEM004Tv30 pzem(PZEMSerial, PZEM_RX_PIN, PZEM_TX_PIN);

void setup() {
  Serial.begin(115200);

  // Inisialisasi pin output
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(BLUE_LED_PIN, OUTPUT);

  // Matikan semua output awal
  digitalWrite(RELAY_PIN, LOW);
  digitalWrite(RED_LED_PIN, LOW);
  digitalWrite(GREEN_LED_PIN, LOW);
  digitalWrite(BLUE_LED_PIN, LOW);

  // ===== SET WAKTU RTC SEKALI SAJA =====
  rtc.writeProtect(false);
  rtc.halt(false);
  Time t(2026, 2, 6, 10, 30, 0, Time::kFriday);
  rtc.time(t);

  // Inisialisasi PZEM
  PZEMSerial.begin(9600, SERIAL_8N1, PZEM_RX_PIN, PZEM_TX_PIN);

  Serial.println("System Ready. Ketik perintah RELAY ON/OFF atau LED ON/OFF.");
}

void loop() {
  // ----- Baca waktu dari RTC -----
  Time now = rtc.time();
  Serial.print("Tanggal: ");
  Serial.print(now.yr);
  Serial.print("-");
  Serial.print(now.mon);
  Serial.print("-");
  Serial.print(now.date);
  Serial.print(" | Waktu: ");
  Serial.print(now.hr);
  Serial.print(":");
  Serial.print(now.min);
  Serial.print(":");
  Serial.println(now.sec);

  // ----- Baca data PZEM -----
  float voltage = pzem.voltage();
  float current = pzem.current();
  float power = pzem.power();
  float energy = pzem.energy();
  float frequency = pzem.frequency();
  float pf = pzem.pf();

  if (isnan(voltage)) voltage = 0;
  if (isnan(current)) current = 0;
  if (isnan(power)) power = 0;
  if (isnan(energy)) energy = 0;
  if (isnan(frequency)) frequency = 0;
  if (isnan(pf)) pf = 0;

  Serial.print("Voltage: ");
  Serial.print(voltage);
  Serial.println(" V");
  Serial.print("Current: ");
  Serial.print(current);
  Serial.println(" A");
  Serial.print("Power:   ");
  Serial.print(power);
  Serial.println(" W");
  Serial.print("Energy:  ");
  Serial.print(energy);
  Serial.println(" Wh");
  Serial.print("Frequency: ");
  Serial.print(frequency);
  Serial.println(" Hz");
  Serial.print("PF:      ");
  Serial.println(pf);
  Serial.println("-----------------------------");

  // ----- Kontrol relay / LED via serial -----
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command.equalsIgnoreCase("RELAY ON")) digitalWrite(RELAY_PIN, HIGH);
    else if (command.equalsIgnoreCase("RELAY OFF")) digitalWrite(RELAY_PIN, LOW);
    else if (command.equalsIgnoreCase("RED ON")) digitalWrite(RED_LED_PIN, HIGH);
    else if (command.equalsIgnoreCase("RED OFF")) digitalWrite(RED_LED_PIN, LOW);
    else if (command.equalsIgnoreCase("GREEN ON")) digitalWrite(GREEN_LED_PIN, HIGH);
    else if (command.equalsIgnoreCase("GREEN OFF")) digitalWrite(GREEN_LED_PIN, LOW);
    else if (command.equalsIgnoreCase("BLUE ON")) digitalWrite(BLUE_LED_PIN, HIGH);
    else if (command.equalsIgnoreCase("BLUE OFF")) digitalWrite(BLUE_LED_PIN, LOW);
    else Serial.println("Perintah tidak dikenal!");
  }

  delay(2000);  // Update setiap 2 detik
}
