/*
 * ================= TEST RTC DS1302 SAJA =================
 * Tanpa WiFi, MQTT, PZEM - hanya RTC
 * Untuk cek apakah RTC jalan dengan benar
 */

#include <DS1302.h>

// ================= RTC PIN =================
#define RTC_CE   4
#define RTC_IO   3
#define RTC_SCLK 2

DS1302 rtc(RTC_CE, RTC_IO, RTC_SCLK);

void setup()
{
    Serial.begin(115200);
    delay(1000);

    Serial.println("\n\n========================================");
    Serial.println("       RTC DS1302 TEST PROGRAM");
    Serial.println("========================================\n");

    // Init RTC
    rtc.writeProtect(false);
    rtc.halt(false);

    // Baca waktu saat ini
    Time now = rtc.time();

    Serial.print("Waktu RTC saat ini: ");
    Serial.print(now.yr);
    Serial.print("-");
    Serial.print(now.mon);
    Serial.print("-");
    Serial.print(now.date);
    Serial.print(" ");
    Serial.print(now.hr);
    Serial.print(":");
    Serial.print(now.min);
    Serial.print(":");
    Serial.println(now.sec);

    Serial.print("\nTahun: ");
    Serial.println(now.yr);

    // Cek apakah RTC valid (tahun >= 2025)
    if (now.yr >= 2025)
    {
        Serial.println("Status: RTC SUDAH VALID (tahun >= 2025)");
        Serial.println("Apa mau set waktu baru? (ketik 'y' di Serial Monitor untuk set)");
    }
    else
    {
        Serial.println("Status: RTC BELUM VALID (tahun < 2025)");
        Serial.println("Menunggu input waktu dari Serial Monitor...\n");
        printInstructions();
    }

    Serial.println("\n========================================\n");
}

void loop()
{
    // Baca RTC terus menerus
    static unsigned long lastPrint = 0;

    if (millis() - lastPrint > 1000)  // Setiap 1 detik
    {
        lastPrint = millis();

        Time now = rtc.time();

        // Print waktu
        char buffer[30];
        sprintf(buffer, "%04d-%02d-%02d %02d:%02d:%02d",
                now.yr, now.mon, now.date,
                now.hr, now.min, now.sec);

        Serial.print("RTC: ");
        Serial.println(buffer);

        // Cek relay (opsional - untuk test schedule)
        // Serial.print("Relay: ");
        // Serial.println(digitalRead(RELAY_PIN) ? "ON" : "OFF");
    }

    // Cek input dari Serial Monitor
    if (Serial.available())
    {
        String input = Serial.readStringUntil('\n');
        input.trim();

        if (input == "y" || input == "Y")
        {
            Serial.println("\nMasukkan waktu dalam format:");
            Serial.println("YYYY MM DD HH MM SS DOW");
            Serial.println("Contoh: 2026 03 22 14 30 00 5");
            Serial.println("DOW: 0=Minggu, 1=Senin, ..., 6=Sabtu");
            Serial.println("Kirim waktu sekarang...\n");
        }
        else if (input.length() > 0)
        {
            // Parse waktu
            int year, month, day, hour, minute, second, dow;

            int count = sscanf(input.c_str(), "%d %d %d %d %d %d %d",
                              &year, &month, &day, &hour, &minute, &second, &dow);

            if (count == 7)
            {
                // Set RTC
                Time newTime(year, month, day, hour, minute, second, (Time::Day)dow);
                rtc.time(newTime);

                Serial.println("\n========================================");
                Serial.println("      RTC BERHASIL DISET!");
                Serial.println("========================================\n");

                // Konfirmasi dengan baca lagi
                delay(100);
                Time now = rtc.time();

                Serial.print("Waktu RTC sekarang: ");
                Serial.print(now.yr);
                Serial.print("-");
                Serial.print(now.mon);
                Serial.print("-");
                Serial.print(now.date);
                Serial.print(" ");
                Serial.print(now.hr);
                Serial.print(":");
                Serial.print(now.min);
                Serial.print(":");
                Serial.println(now.sec);

                Serial.print("\nTahun: ");
                Serial.println(now.yr);

                if (now.yr >= 2025)
                {
                    Serial.println("Status: RTC SUDAH VALID ✓\n");
                }
                else
                {
                    Serial.println("Status: RTC MASIH BELUM VALID ✗\n");
                }
            }
            else
            {
                Serial.println("\n✗ Format salah!");
                Serial.println("Gunakan format: YYYY MM DD HH MM SS DOW");
                Serial.println("Contoh: 2026 03 22 14 30 00 5\n");
                printInstructions();
            }
        }
    }
}

void printInstructions()
{
    Serial.println("========================================");
    Serial.println("         CARA SET WAKTU RTC:");
    Serial.println("========================================");
    Serial.println("1. Ketik 'y' lalu Enter untuk lihat format");
    Serial.println("2. Atau langsung ketik:");
    Serial.println("   YYYY MM DD HH MM SS DOW");
    Serial.println("   Contoh: 2026 03 22 14 30 00 5");
    Serial.println("========================================\n");
}
