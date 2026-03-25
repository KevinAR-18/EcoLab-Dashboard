#include <DS1302.h>

// ================= RTC =================
#define RTC_CE   4
#define RTC_IO   3
#define RTC_SCLK 2

DS1302 rtc(RTC_CE, RTC_IO, RTC_SCLK);

void setup() {
  Serial.begin(115200);

  // Inisialisasi RTC
  rtc.writeProtect(false);
  rtc.halt(false);

  // ===== SET WAKTU SEKALI SAJA =====
  Time t(2026, 2, 6, 10, 30, 0, Time::kFriday);
  rtc.time(t);
}

void loop() {
  // Baca waktu dari RTC
  Time now = rtc.time();

  Serial.print("Tanggal: ");
  Serial.print(now.yr); Serial.print("-");
  Serial.print(now.mon); Serial.print("-");
  Serial.print(now.date);

  Serial.print(" | Waktu: ");
  Serial.print(now.hr); Serial.print(":");
  Serial.print(now.min); Serial.print(":");
  Serial.println(now.sec);

  Serial.println("--------------------------");

  delay(1000); // update tiap 1 detik
}