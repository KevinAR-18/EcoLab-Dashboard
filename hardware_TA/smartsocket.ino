#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <PZEM004Tv30.h>
#include <DS1302.h>
#include <time.h>
#include <EEPROM.h>  // Untuk menyimpan schedule agar tidak hilang saat reboot

// ================= OUTPUT =================
#define RELAY_PIN 7
#define RED_LED_PIN 8
#define BLUE_LED_PIN 9
#define GREEN_LED_PIN 10

// ================= WIFI =================
const char *ssid = "3KSERA";
const char *password = "04115474";

// ================= NTP CONFIG =================
const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 7 * 3600;  // GMT+7 (WIB)
const int   daylightOffset_sec = 0;    // Tidak ada daylight saving di Indonesia

// ================= MQTT =================
const char *mqtt_server = "10.33.11.148";
const int mqtt_port = 8883;

const char *mqtt_user = "smartsocket1";
const char *mqtt_pass = "smart1";

const char* client_id = "smartsocket1";

// MQTT topics
const char *topic_control = "ecolab/socket/1/control";
const char *topic_energy = "ecolab/socket/1/energy";
const char *topic_device_status = "ecolab/socket/1/devicestatus";
const char *topic_statusrelay = "ecolab/socket/1/relaystatus";

// ================= MQTT TOPIC TAMBAHAN =================
const char *topic_timer = "ecolab/socket/1/timer";
const char *topic_timer_status = "ecolab/socket/1/timer/status";

// Schedule Topics (Start/Stop + Mode)
const char *topic_schedule_start = "ecolab/socket/1/schedule/start";
const char *topic_schedule_stop = "ecolab/socket/1/schedule/stop";
const char *topic_schedule_mode = "ecolab/socket/1/schedule/mode";
const char *topic_schedule_status = "ecolab/socket/1/schedule/status";

// ================= TLS CERT =================
const char *ca_cert = R"EOF(
-----BEGIN CERTIFICATE-----
MIIDrTCCApWgAwIBAgIUKjQ9PvlPW8wZDIeg0DCHL2DpIQMwDQYJKoZIhvcNAQEL
BQAwZjELMAkGA1UEBhMCSUQxDDAKBgNVBAgMA0RJWTETMBEGA1UEBwwKWW9neWFr
YXJ0YTEPMA0GA1UECgwGRWNvTGFiMQ8wDQYDVQQLDAZFY29MYWIxEjAQBgNVBAMM
CUVjb0xhYi1DQTAeFw0yNjAzMDYxMjUxMTJaFw0zNjAzMDMxMjUxMTJaMGYxCzAJ
BgNVBAYTAklEMQwwCgYDVQQIDANESVkxEzARBgNVBAcMCllvZ3lha2FydGExDzAN
BgNVBAoMBkVjb0xhYjEPMA0GA1UECwwGRWNvTGFiMRIwEAYDVQQDDAlFY29MYWIt
Q0EwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDJAu6y7j1MM+AR9Siw
0MEK6e6QI905aMgZ8Xowsv2iybu+VKeIZvOCya0lO2u0oNO/4S3ZKTlhhloqYAoW
9dFGincAHv6An95zC7zyfO4vqcgwPCaAEuQcEAd7RQaTaBwqBvj/Ljcbi5KjaFIs
uj7+zuuLAjUnz82p+DK58c4SsetB+g+fd2wo0NTt8zvbzp6FlLFViF1Ijvpu79KJ
/rJfVX5luLKG1ECxGXDOc2igrYM4oS5tyS7oY5GQq/ZHJcDkdgzA3xRRXTOKJlgS
dRsZ+CFqTZh8FPWBC/GxG/Ntoc9N2q5XcQv0ML3FVsLjzgotKEkCUcC79NutZuyh
hPKNAgMBAAGjUzBRMB0GA1UdDgQWBBTZhc7myGBXCv3dX99yLgC9DHQupDAfBgNV
HSMEGDAWgBTZhc7myGBXCv3dX99yLgC9DHQupDAPBgNVHRMBAf8EBTADAQH/MA0G
CSqGSIb3DQEBCwUAA4IBAQBWILO6oem3OQBptjzyd4nQA14Qrqfso/g+Oh0INtNy
GSjKmctZrZyI8mbHXm/TrC9XqtGUha/1gmle0y6gXR+Wk+4cszuAkCx3B0cay4Hc
MeKcZ+qTdZqNrTEY6DfmSBPuBLjEducTfxvtZcpkqRhhXxYvc8jY+6VAxVnNa0+P
Vy0wBX5/dkGFNzqiVZnUuqrAu6Vy7/dWnJ5LNJP/rsORm1+4V55SSig+UtPyyOvs
IIOGLn4YjG4Ijw7HUNXFCVtLvdhzUCH64YxA1tUgYFTYpSyLQndKHPsYgpu0RTTc
DpDUqFzRsufKUh18I7xgFSL4x8YKZNlmyCcLA27gg3Jv
-----END CERTIFICATE-----
)EOF";

// ================= PZEM =================
#define PZEM_RX_PIN 5
#define PZEM_TX_PIN 6

HardwareSerial PZEMSerial(1);
PZEM004Tv30 pzem(PZEMSerial, PZEM_RX_PIN, PZEM_TX_PIN);

// ================= RTC =================
#define RTC_CE 4
#define RTC_IO 3
#define RTC_SCLK 2

DS1302 rtc(RTC_CE, RTC_IO, RTC_SCLK);

// ================= EEPROM ADDRESSES =================
// Untuk menyimpan schedule agar tidak hilang saat reboot
#define EEPROM_SIZE 64  // Ukuran EEPROM yang digunakan
#define ADDR_SCHEDULE_START_ACTIVE    0
#define ADDR_SCHEDULE_STOP_ACTIVE     1
#define ADDR_SCHEDULE_START_HOUR      2
#define ADDR_SCHEDULE_START_MINUTE    3
#define ADDR_SCHEDULE_STOP_HOUR       4
#define ADDR_SCHEDULE_STOP_MINUTE     5
#define ADDR_SCHEDULE_DAILY_MODE      6
#define ADDR_MANUAL_RELAY_STATE       7

// ================= MQTT =================
WiFiClientSecure espClient;
PubSubClient client(espClient);

// ================= GLOBAL =================
unsigned long lastEnergy = 0;
unsigned long lastStatusSync = 0;
unsigned long lastDebugPrint = 0;
unsigned long lastWiFiRetry = 0;
unsigned long lastMQTTRetry = 0;
bool relayState = false;
bool ntpSynced = false;
bool pzemError = false;

// ================= TIMER =================
bool timerActive = false;
unsigned long timerStartMillis = 0;
unsigned long timerDuration = 0;

// ================= SCHEDULE (Start/Stop + Daily/Onetime Mode) =================
bool scheduleStartActive = false;
bool scheduleStopActive = false;
int schedStartHour = 0;
int schedStartMinute = 0;
int schedStopHour = 0;
int schedStopMinute = 0;

// Schedule Mode: true = Daily (repeat), false = Onetime (once only)
bool scheduleDailyMode = true;

// For onetime mode - track last triggered day
int lastTriggeredDay = 0;
bool startTriggered = false;
bool stopTriggered = false;

void saveManualRelayStateToEEPROM()
{
    EEPROM.write(ADDR_MANUAL_RELAY_STATE, relayState ? 1 : 0);
    EEPROM.commit();
    Serial.print("Saved manual relay state: ");
    Serial.println(relayState ? "ON" : "OFF");
}

void restoreManualRelayStateFromEEPROM()
{
    bool savedRelayState = EEPROM.read(ADDR_MANUAL_RELAY_STATE) == 1;

    if (scheduleStartActive || scheduleStopActive)
    {
        Serial.println("Manual relay restore skipped because schedule is active");
        return;
    }

    relayState = savedRelayState;
    digitalWrite(RELAY_PIN, relayState ? HIGH : LOW);

    Serial.print("Restored manual relay state: ");
    Serial.println(relayState ? "ON" : "OFF");
}

// ================= LED FUNCTION =================
void blinkLED(int pin, int times, int delayMs)
{
    for (int i = 0; i < times; i++)
    {
        digitalWrite(pin, HIGH);
        delay(delayMs);
        digitalWrite(pin, LOW);
        delay(delayMs);
    }
}

void blinkDualLED(int times)
{
    for (int i = 0; i < times; i++)
    {
        digitalWrite(RED_LED_PIN, HIGH);
        digitalWrite(GREEN_LED_PIN, HIGH);
        delay(150);
        digitalWrite(RED_LED_PIN, LOW);
        digitalWrite(GREEN_LED_PIN, LOW);
        delay(150);
    }
}

// ================= LED STATUS (NON-BLOCKING) =================
void updateLEDIndicators()
{
    unsigned long now = millis();

    // Biru: koneksi
    // OFF = WiFi putus, blink = WiFi OK tapi MQTT belum connect, ON = WiFi + MQTT OK
    if (WiFi.status() != WL_CONNECTED)
    {
        digitalWrite(BLUE_LED_PIN, LOW);
    }
    else if (client.connected())
    {
        digitalWrite(BLUE_LED_PIN, HIGH);
    }
    else
    {
        digitalWrite(BLUE_LED_PIN, ((now / 500) % 2) ? HIGH : LOW);
    }

    // Hijau: output socket
    // Blink saat timer aktif, selain itu mengikuti status relay
    if (timerActive)
    {
        digitalWrite(GREEN_LED_PIN, ((now / 500) % 2) ? HIGH : LOW);
    }
    else
    {
        digitalWrite(GREEN_LED_PIN, relayState ? HIGH : LOW);
    }

    // Merah: error
    // Prioritas blink cepat untuk RTC/NTP belum sync, blink pelan untuk PZEM error
    if (!ntpSynced)
    {
        digitalWrite(RED_LED_PIN, ((now / 250) % 2) ? HIGH : LOW);
    }
    else if (pzemError)
    {
        digitalWrite(RED_LED_PIN, ((now / 750) % 2) ? HIGH : LOW);
    }
    else
    {
        digitalWrite(RED_LED_PIN, LOW);
    }
}

// ================= NTP TO RTC =================
void syncNTPtoRTC() {
    Serial.println("Syncing NTP time to RTC...");

    // Config NTP
    configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);

    // Tunggu waktu NTP tersedia
    struct tm timeinfo;
    int retry = 0;
    while (!getLocalTime(&timeinfo) && retry < 10) {
        Serial.print(".");
        delay(500);
        retry++;
    }

    if (retry >= 10) {
        Serial.println("\n❌ NTP Sync FAILED! RTC not set.");
        return;
    }

    Serial.println("\n✅ NTP Sync successful!");

    // Convert tm ke Time format untuk DS1302
    // tm_year: tahun sejak 1900 (2026 = 126)
    // tm_mon: 0-11 (0 = Jan, 11 = Dec)
    // tm_wday: 0-6 (0 = Sunday, 1 = Monday, ...)
    // DS1302 Time::Day: 1-7 (1=Monday, 7=Sunday)

    int year = timeinfo.tm_year + 1900;
    int month = timeinfo.tm_mon + 1;
    int day = timeinfo.tm_mday;
    int hour = timeinfo.tm_hour;
    int minute = timeinfo.tm_min;
    int second = timeinfo.tm_sec;

    // Convert tm_wday (0=Sunday) ke Time::Day (1=Monday, 7=Sunday)
    Time::Day dow;
    switch (timeinfo.tm_wday) {
        case 0: dow = Time::kSunday;    break;
        case 1: dow = Time::kMonday;    break;
        case 2: dow = Time::kTuesday;   break;
        case 3: dow = Time::kWednesday; break;
        case 4: dow = Time::kThursday;  break;
        case 5: dow = Time::kFriday;    break;
        case 6: dow = Time::kSaturday;  break;
        default: dow = Time::kMonday;   break;
    }

    // Set RTC
    Time newTime(year, month, day, hour, minute, second, dow);
    rtc.time(newTime);

    Serial.print("RTC Set to: ");
    Serial.print(year); Serial.print("-");
    Serial.print(month); Serial.print("-");
    Serial.print(day); Serial.print(" ");
    Serial.print(hour); Serial.print(":");
    Serial.print(minute); Serial.print(":");
    Serial.println(second);
    ntpSynced = true;
}

// ================= WIFI CONNECT =================
void start_wifi()
{
    WiFi.mode(WIFI_STA);
    WiFi.setSleep(false);
    WiFi.setAutoReconnect(true);
    WiFi.persistent(false);
    WiFi.setTxPower(WIFI_POWER_8_5dBm);

    WiFi.begin(ssid, password);

    Serial.print("WiFi connecting");

    unsigned long startAttempt = millis();
    while (WiFi.status() != WL_CONNECTED && millis() - startAttempt < 15000)
    {
        delay(500);
        Serial.print(".");
    }

    if (WiFi.status() == WL_CONNECTED)
    {
        Serial.println("\nWiFi connected");
        Serial.println(WiFi.localIP());
        syncNTPtoRTC();
    }
    else
    {
        Serial.println("\nWiFi not connected, continuing in offline mode");
    }
}

void ensureWiFiConnection()
{
    if (WiFi.status() == WL_CONNECTED)
    {
        if (!ntpSynced)
        {
            syncNTPtoRTC();
        }
        return;
    }

    if (millis() - lastWiFiRetry < 10000)
    {
        return;
    }

    lastWiFiRetry = millis();
    Serial.println("WiFi disconnected, retrying...");
    WiFi.disconnect();
    WiFi.begin(ssid, password);
}
void callback(char *topic, byte *payload, unsigned int length)
{
    String msg = "";
    for (int i = 0; i < length; i++)
    {
        msg += (char)payload[i];
    }

    Serial.print("Topic: ");
    Serial.println(topic);
    Serial.print("Message: ");
    Serial.println(msg);

    // ================= CONTROL RELAY =================
    if (String(topic) == topic_control)
    {
        if (msg == "ON")
        {
            digitalWrite(RELAY_PIN, HIGH);
            relayState = true;
            saveManualRelayStateToEEPROM();
            client.publish(topic_statusrelay, "ON");
        }
        else if (msg == "OFF")
        {
            digitalWrite(RELAY_PIN, LOW);
            relayState = false;
            pzemError = false;
            saveManualRelayStateToEEPROM();
            client.publish(topic_statusrelay, "OFF");
        }
    }

    // ================= TIMER =================
    else if (String(topic) == topic_timer)
    {
        int duration = msg.toInt();

        if (duration == 0)
        {
            // Cancel timer
            timerActive = false;
            client.publish(topic_timer_status, "INACTIVE", true);
            Serial.println("Timer cancelled");
        }
        else
        {
            // Set timer normal
            timerDuration = duration * 1000; // detik → ms
            timerStartMillis = millis();
            timerActive = true;

            // Publish status immediately
            publishStatusSync();
        }
    }

    // ================= SCHEDULE START =================
    else if (String(topic) == topic_schedule_start)
    {
        if (msg == "CLEAR")
        {
            // Cancel start schedule
            scheduleStartActive = false;
            startTriggered = false;
            publishStatusSync();
            saveScheduleToEEPROM();  // Simpan ke EEPROM
            Serial.println("Start schedule cancelled");
        }
        else
        {
            // format: HH:MM
            int separator = msg.indexOf(':');
            if (separator != -1)
            {
                schedStartHour = msg.substring(0, separator).toInt();
                schedStartMinute = msg.substring(separator + 1).toInt();

                scheduleStartActive = true;
                startTriggered = false; // Reset trigger

                publishStatusSync();
                saveScheduleToEEPROM();  // Simpan ke EEPROM
            }
            else
            {
                client.publish(topic_schedule_status, "FORMAT ERROR");
            }
        }
    }

    // ================= SCHEDULE STOP =================
    else if (String(topic) == topic_schedule_stop)
    {
        if (msg == "CLEAR")
        {
            // Cancel stop schedule
            scheduleStopActive = false;
            stopTriggered = false;
            publishStatusSync();
            saveScheduleToEEPROM();  // Simpan ke EEPROM
            Serial.println("Stop schedule cancelled");
        }
        else
        {
            // format: HH:MM
            int separator = msg.indexOf(':');
            if (separator != -1)
            {
                schedStopHour = msg.substring(0, separator).toInt();
                schedStopMinute = msg.substring(separator + 1).toInt();

                scheduleStopActive = true;
                stopTriggered = false; // Reset trigger

                publishStatusSync();
                saveScheduleToEEPROM();  // Simpan ke EEPROM
            }
            else
            {
                client.publish(topic_schedule_status, "FORMAT ERROR");
            }
        }
    }

    // ================= SCHEDULE MODE =================
    else if (String(topic) == topic_schedule_mode)
    {
        // format: "daily" or "onetime"
        if (msg == "daily")
        {
            scheduleDailyMode = true;
            lastTriggeredDay = 0;
            publishStatusSync();
            saveScheduleToEEPROM();  // Simpan ke EEPROM
            Serial.println("Schedule mode: Daily");
        }
        else if (msg == "onetime")
        {
            scheduleDailyMode = false;
            lastTriggeredDay = 0;
            startTriggered = false;
            stopTriggered = false;
            publishStatusSync();
            saveScheduleToEEPROM();  // Simpan ke EEPROM
            Serial.println("Schedule mode: Onetime");
        }
        else
        {
            client.publish(topic_schedule_status, "MODE ERROR");
        }
    }

}

// ================= EEPROM SAVE/LOAD =================
void saveScheduleToEEPROM()
{
    Serial.println("Saving schedule to EEPROM...");
    EEPROM.write(ADDR_SCHEDULE_START_ACTIVE, scheduleStartActive ? 1 : 0);
    EEPROM.write(ADDR_SCHEDULE_STOP_ACTIVE, scheduleStopActive ? 1 : 0);
    EEPROM.write(ADDR_SCHEDULE_START_HOUR, schedStartHour);
    EEPROM.write(ADDR_SCHEDULE_START_MINUTE, schedStartMinute);
    EEPROM.write(ADDR_SCHEDULE_STOP_HOUR, schedStopHour);
    EEPROM.write(ADDR_SCHEDULE_STOP_MINUTE, schedStopMinute);
    EEPROM.write(ADDR_SCHEDULE_DAILY_MODE, scheduleDailyMode ? 1 : 0);
    EEPROM.commit();  // Wajib untuk ESP32
    Serial.println("Schedule saved to EEPROM!");
}

void loadScheduleFromEEPROM()
{
    Serial.println("Loading schedule from EEPROM...");
    scheduleStartActive = EEPROM.read(ADDR_SCHEDULE_START_ACTIVE) == 1;
    scheduleStopActive = EEPROM.read(ADDR_SCHEDULE_STOP_ACTIVE) == 1;
    schedStartHour = EEPROM.read(ADDR_SCHEDULE_START_HOUR);
    schedStartMinute = EEPROM.read(ADDR_SCHEDULE_START_MINUTE);
    schedStopHour = EEPROM.read(ADDR_SCHEDULE_STOP_HOUR);
    schedStopMinute = EEPROM.read(ADDR_SCHEDULE_STOP_MINUTE);
    scheduleDailyMode = EEPROM.read(ADDR_SCHEDULE_DAILY_MODE) == 1;

    // Print loaded schedule
    Serial.print("Loaded Schedule - ");
    Serial.print(scheduleStartActive ? "Start: " : "Start: N/A, ");
    if (scheduleStartActive) {
        Serial.print(schedStartHour);
        Serial.print(":");
        Serial.print(schedStartMinute);
    }
    Serial.print(", ");
    Serial.print(scheduleStopActive ? "Stop: " : "Stop: N/A, ");
    if (scheduleStopActive) {
        Serial.print(schedStopHour);
        Serial.print(":");
        Serial.print(schedStopMinute);
    }
    Serial.print(", Mode: ");
    Serial.println(scheduleDailyMode ? "Daily" : "Onetime");
}

// ================= MQTT CONNECT =================
void reconnect()
{
    if (client.connected() || WiFi.status() != WL_CONNECTED)
    {
        return;
    }
    if (millis() - lastMQTTRetry < 5000)
    {
        return;
    }
    lastMQTTRetry = millis();
    Serial.print("Connecting MQTT...");
    if (client.connect(client_id, mqtt_user, mqtt_pass,
                       topic_device_status, 0, false, "OFFLINE"))
    {
        Serial.println("connected");
        // KIRIM STATUS ONLINE
        client.publish(topic_device_status, "ONLINE", true);
        // SUBSCRIBE
        client.subscribe(topic_control);
        client.subscribe(topic_timer);
        client.subscribe(topic_schedule_start);
        client.subscribe(topic_schedule_stop);
        client.subscribe(topic_schedule_mode);
        // PUBLISH STATUS SAAT CONNECT (untuk sync GUI)
        publishStatusSync();
    }
    else
    {
        Serial.print("failed, rc=");
        Serial.println(client.state());
    }
}
// ================= LOOP TAMBAHAN =================
void handleTimer()
{
    if (timerActive)
    {
        if (millis() - timerStartMillis >= timerDuration)
        {
            timerActive = false;

            digitalWrite(RELAY_PIN, LOW);
            relayState = false;
            pzemError = false;

            client.publish(topic_timer_status, "TIMER_DONE");
        }
    }
}

void handleSchedule()
{
    // Check if any schedule is active
    if (!scheduleStartActive && !scheduleStopActive)
    {
        return;
    }

    Time timeRTC = rtc.time();
    int currentDay = timeRTC.date;

    // ================= RESET FOR NEW DAY (ONETIME MODE) =================
    if (!scheduleDailyMode && currentDay != lastTriggeredDay)
    {
        lastTriggeredDay = currentDay;
        startTriggered = false;
        stopTriggered = false;
    }

    // ================= SCHEDULE START (TURN ON) =================
    if (scheduleStartActive)
    {
        if (timeRTC.hr == schedStartHour && timeRTC.min == schedStartMinute)
        {
            // Check if already triggered this minute
            if (!startTriggered)
            {
                startTriggered = true;

                digitalWrite(RELAY_PIN, HIGH);
                relayState = true;

                client.publish(topic_statusrelay, "ON");
                client.publish(topic_schedule_status, "START_TRIGGER");

                Serial.println("Schedule START triggered!");
            }
        }
    }

    // ================= SCHEDULE STOP (TURN OFF) =================
    if (scheduleStopActive)
    {
        if (timeRTC.hr == schedStopHour && timeRTC.min == schedStopMinute)
        {
            // Check if already triggered this minute
            if (!stopTriggered)
            {
                stopTriggered = true;

                digitalWrite(RELAY_PIN, LOW);
                relayState = false;
                pzemError = false;

                client.publish(topic_statusrelay, "OFF");
                client.publish(topic_schedule_status, "STOP_TRIGGER");

                Serial.println("Schedule STOP triggered!");
            }
        }
    }

    // ================= RESET TRIGGERS (DAILY MODE) =================
    // For daily mode: reset triggers when time passes to next minute
    // This ensures it can trigger again at the same time tomorrow
    if (scheduleDailyMode)
    {
        // Track last checked minute
        static int lastCheckedMinute = -1;

        // When minute changes, reset triggers if we're past the scheduled time
        if (timeRTC.min != lastCheckedMinute)
        {
            lastCheckedMinute = timeRTC.min;

            // Reset start trigger if we're past the start time (different minute)
            if (timeRTC.hr != schedStartHour || timeRTC.min != schedStartMinute)
            {
                // Only reset if we already triggered it before
                if (startTriggered)
                {
                    startTriggered = false;
                    Serial.println("Start trigger reset (daily mode)");
                }
            }

            // Reset stop trigger if we're past the stop time (different minute)
            if (timeRTC.hr != schedStopHour || timeRTC.min != schedStopMinute)
            {
                // Only reset if we already triggered it before
                if (stopTriggered)
                {
                    stopTriggered = false;
                    Serial.println("Stop trigger reset (daily mode)");
                }
            }
        }
    }

    // ================= RECOVERY LOGIC =================
    // Kalau relay mati tapi seharusnya nyala (dalam rentang schedule), nyalakan lagi
    // Ini untuk recovery setelah reboot/power loss
    if (!timerActive)  // Timer lebih prioritas, jangan override
    {
        if (scheduleStartActive && scheduleStopActive)
        {
            // Cek apakah sekarang dalam rentang schedule
            int nowMinutes = timeRTC.hr * 60 + timeRTC.min;
            int startMinutes = schedStartHour * 60 + schedStartMinute;
            int stopMinutes = schedStopHour * 60 + schedStopMinute;

            bool should_be_on = false;

            // Untuk schedule yang melewati tengah malam (misal 23:00 - 02:00)
            if (startMinutes < stopMinutes)
            {
                // Normal: 07:00 - 20:00
                should_be_on = (nowMinutes >= startMinutes && nowMinutes < stopMinutes);
            }
            else
            {
                // Lewat tengah malam: 23:00 - 02:00
                should_be_on = (nowMinutes >= startMinutes || nowMinutes < stopMinutes);
            }

            // Recovery: Nyalakan jika seharusnya ON tapi sekarang OFF
            if (should_be_on && !relayState)
            {
                digitalWrite(RELAY_PIN, HIGH);
                relayState = true;

                client.publish(topic_statusrelay, "ON");
                publishStatusSync();

                char buf[100];
                sprintf(buf, "[RECOVERY] Relay ON (within schedule range: %02d:%02d - %02d:%02d)",
                        schedStartHour, schedStartMinute, schedStopHour, schedStopMinute);
                Serial.println(buf);
            }
        }
    }
}

// ================= STATUS SYNC (untuk multi-GUI) =================
void publishStatusSync()
{
    // Publish relay status
    if (relayState)
    {
        client.publish(topic_statusrelay, "ON", true);  // retain = true
    }
    else
    {
        client.publish(topic_statusrelay, "OFF", true); // retain = true
    }

    // Publish timer status
    if (timerActive)
    {
        unsigned long elapsed = millis() - timerStartMillis;
        unsigned long remaining = timerDuration - elapsed;
        int remainingSec = remaining / 1000;

        String timerPayload = "ACTIVE:" + String(remainingSec) + "s";
        client.publish(topic_timer_status, timerPayload.c_str(), true);
    }
    else
    {
        client.publish(topic_timer_status, "INACTIVE", true);
    }

    // Publish schedule status (JSON format)
    String schedulePayload = "{";

    // Start schedule
    if (scheduleStartActive)
    {
        char timeStr[6];
        sprintf(timeStr, "%02d:%02d", schedStartHour, schedStartMinute);
        schedulePayload += "\"start\":\"" + String(timeStr) + "\",";
    }
    else
    {
        schedulePayload += "\"start\":null,";
    }

    // Stop schedule
    if (scheduleStopActive)
    {
        char timeStr[6];
        sprintf(timeStr, "%02d:%02d", schedStopHour, schedStopMinute);
        schedulePayload += "\"stop\":\"" + String(timeStr) + "\",";
    }
    else
    {
        schedulePayload += "\"stop\":null,";
    }

    // Mode
    schedulePayload += "\"mode\":\"" + String(scheduleDailyMode ? "daily" : "onetime") + "\"";

    schedulePayload += "}";

    client.publish(topic_schedule_status, schedulePayload.c_str(), true);

}

// ================= SETUP =================
void setup()
{
    Serial.begin(115200);

    pinMode(RELAY_PIN, OUTPUT);
    pinMode(RED_LED_PIN, OUTPUT);
    pinMode(GREEN_LED_PIN, OUTPUT);
    pinMode(BLUE_LED_PIN, OUTPUT);

    digitalWrite(RELAY_PIN, LOW);
    digitalWrite(RED_LED_PIN, LOW);
    digitalWrite(GREEN_LED_PIN, LOW);
    digitalWrite(BLUE_LED_PIN, LOW);

    // ===== RTC INIT =====
    // RTC harus siap sebelum WiFi connect karena start_wifi() akan sync NTP ke RTC.
    rtc.writeProtect(false);
    rtc.halt(false);

    start_wifi();

    espClient.setCACert(ca_cert);

    client.setServer(mqtt_server, mqtt_port);
    client.setCallback(callback);
    client.setKeepAlive(10);  // 10 detik keepalive

    // ===== PZEM INIT =====
    PZEMSerial.begin(9600, SERIAL_8N1, PZEM_RX_PIN, PZEM_TX_PIN);

    // ===== EEPROM INIT =====
    EEPROM.begin(EEPROM_SIZE);
    loadScheduleFromEEPROM();  // Load schedule yang tersimpan
    restoreManualRelayStateFromEEPROM();
    updateLEDIndicators();
}

// ================= LOOP =================
void loop()
{
    ensureWiFiConnection();
    reconnect();
    if (client.connected())
    {
        client.loop();
    }
    // ================= DEBUG RTC (every 1 sec) =================
    if (millis() - lastDebugPrint > 1000)
    {
        lastDebugPrint = millis();
        Time timeRTC = rtc.time();
        Serial.print("???? RTC: ");
        Serial.print(timeRTC.yr);
        Serial.print("-");
        Serial.print(timeRTC.mon);
        Serial.print("-");
        Serial.print(timeRTC.date);
        Serial.print(" ");
        Serial.print(timeRTC.hr);
        Serial.print(":");
        Serial.print(timeRTC.min);
        Serial.print(":");
        Serial.println(timeRTC.sec);
    }
    // ================= ENERGY PUBLISH (every 2 sec) =================
    if (millis() - lastEnergy > 2000)
    {
        lastEnergy = millis();
        float voltage, current, power, energy, frequency, pf;
        // CEK RELAY STATE
        if (relayState)
        {
            // Relay ON ??? Baca data PZEM asli
            voltage = pzem.voltage();
            current = pzem.current();
            power = pzem.power();
            energy = pzem.energy();
            frequency = pzem.frequency();
            pf = pzem.pf();
            // Kalau PZEM error, kirim 0
            if (isnan(voltage) || isnan(current) || isnan(power) || isnan(energy) || isnan(frequency) || isnan(pf))
            {
                pzemError = true;
                voltage = 0;
                current = 0;
                power = 0;
                energy = 0;
                frequency = 0;
                pf = 0;
                Serial.println("PZEM not responding, sending 0");
            }
            else
            {
                pzemError = false;
            }
        }
        else
        {
            // Relay OFF ??? Kirim semua 0
            pzemError = false;
            voltage = 0;
            current = 0;
            power = 0;
            energy = 0;
            frequency = 0;
            pf = 0;
            Serial.println("Relay OFF, sending 0 data");
        }
        // Kirim payload JSON
        String payload = "{";
        payload += "\"voltage\":" + String(voltage, 2) + ",";
        payload += "\"current\":" + String(current, 3) + ",";
        payload += "\"power\":" + String(power, 2) + ",";
        payload += "\"energy\":" + String(energy, 3) + ",";
        payload += "\"frequency\":" + String(frequency, 1) + ",";
        payload += "\"pf\":" + String(pf, 2);
        payload += "}";
        if (client.connected())
        {
            client.publish(topic_energy, payload.c_str());
        }
        Serial.print("Energy: ");
        Serial.println(payload);
    }
    // ================= STATUS SYNC (every 2 sec for multi-GUI) =================
    if (millis() - lastStatusSync > 2000)
    {
        lastStatusSync = millis();
        if (client.connected())
        {
            publishStatusSync();
        }
    }
    handleTimer();
    handleSchedule();
    updateLEDIndicators();
}
