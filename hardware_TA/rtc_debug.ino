#include <DS1302.h>

// ================= RTC PIN =================
#define RTC_CE   4
#define RTC_IO   3
#define RTC_SCLK 2

DS1302 rtc(RTC_CE, RTC_IO, RTC_SCLK);

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("=================================");
  Serial.println("RTC DS1302 Debug Test");
  Serial.println("=================================");
  Serial.println();

  // Cek pin config
  Serial.println("Pin Configuration:");
  Serial.print("  CE (RST):  GPIO ");
  Serial.println(RTC_CE);
  Serial.print("  IO (DAT):  GPIO ");
  Serial.println(RTC_IO);
  Serial.print("  SCLK (CLK): GPIO ");
  Serial.println(RTC_SCLK);
  Serial.println();

  // Init RTC
  Serial.println("Inisialisasi RTC...");
  rtc.writeProtect(false);
  rtc.halt(false);
  delay(100);

  // Baca waktu pertama kali
  Time now = rtc.time();

  Serial.println();
  Serial.println("Waktu saat ini di RTC:");
  Serial.print("  Tanggal: ");
  Serial.print(now.yr);
  Serial.print("-");
  Serial.print(now.mon);
  Serial.print("-");
  Serial.println(now.date);
  Serial.print("  Waktu:   ");
  Serial.print(now.hr);
  Serial.print(":");
  Serial.print(now.min);
  Serial.print(":");
  Serial.println(now.sec);
  Serial.println();

  // Jika waktu 2000-00-00, RTC kosong/belum diset
  if (now.yr == 2000 && now.mon == 0 && now.date == 0) {
    Serial.println("⚠ RTC BELUM DISET atau TIDAK TERDETEKSI!");
    Serial.println("   Setting waktu default...");

    // Set waktu default
    Time t(2026, 3, 22, 10, 0, 0, Time::kSunday);
    rtc.time(t);

    delay(100);

    // Baca lagi untuk verifikasi
    now = rtc.time();

    Serial.println();
    Serial.println("Setelah diset:");
    Serial.print("  Tanggal: ");
    Serial.print(now.yr);
    Serial.print("-");
    Serial.print(now.mon);
    Serial.print("-");
    Serial.println(now.date);
    Serial.print("  Waktu:   ");
    Serial.print(now.hr);
    Serial.print(":");
    Serial.print(now.min);
    Serial.print(":");
    Serial.println(now.sec);
    Serial.println();

    // Cek lagi apakah masih 2000-00-00
    if (now.yr == 2000 && now.mon == 0) {
      Serial.println("❌ RTC TIDAK TERDETEKSI!");
      Serial.println("   Cek wiring:");
      Serial.println("   1. Pastikan VCC terhubung ke 5V atau 3.3V");
      Serial.println("   2. Pastikan GND terhubung ke GND");
      Serial.println("   3. Cek koneksi CE, IO, SCLK");
      Serial.println("   4. Coba ganti pin jika perlu");
    } else {
      Serial.println("✅ RTC BERHASIL DISET!");
    }
  } else {
    Serial.println("✅ RTC TERDETEKSI!");
  }

  Serial.println();
  Serial.println("=================================");
  Serial.println("Monitoring waktu (update tiap detik):");
  Serial.println("=================================");
}

void loop() {
  Time now = rtc.time();

  Serial.print("[");

  // Jam dengan leading zero
  if (now.hr < 10) Serial.print("0");
  Serial.print(now.hr);
  Serial.print(":");

  // Menit dengan leading zero
  if (now.min < 10) Serial.print("0");
  Serial.print(now.min);
  Serial.print(":");

  // Detik dengan leading zero
  if (now.sec < 10) Serial.print("0");
  Serial.print(now.sec);
  Serial.print("] ");

  // Tanggal
  Serial.print(now.yr);
  Serial.print("-");
  if (now.mon < 10) Serial.print("0");
  Serial.print(now.mon);
  Serial.print("-");
  if (now.date < 10) Serial.print("0");
  Serial.print(now.date);

  // Cek apakah RTC valid
  if (now.yr == 2000 && now.mon == 0 && now.date == 0) {
    Serial.print(" ❌ RTC ERROR");
  }

  Serial.println();

  delay(1000);
}
