#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <PZEM004Tv30.h>
#include <DS1302.h>

// ================= OUTPUT =================
#define RELAY_PIN 7
#define RED_LED_PIN 8
#define GREEN_LED_PIN 9
#define BLUE_LED_PIN 10

// ================= WIFI =================
const char *ssid = "3KSERA";
const char *password = "04115474";

// ================= MQTT =================
const char *mqtt_server = "192.168.100.7";
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

const char *topic_schedule = "ecolab/socket/1/schedule";
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

// ================= MQTT =================
WiFiClientSecure espClient;
PubSubClient client(espClient);

// ================= GLOBAL =================
unsigned long lastEnergy = 0;
bool relayState = false;

// ================= TIMER =================
bool timerActive = false;
unsigned long timerStartMillis = 0;
unsigned long timerDuration = 0;

// ================= SCHEDULE =================
bool scheduleActive = false;
int schedHour = 0;
int schedMinute = 0;
bool scheduleTriggered = false;


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

// ================= WIFI MODIF =================
void start_wifi()
{
    WiFi.mode(WIFI_STA);
    WiFi.setSleep(false);
    WiFi.setAutoReconnect(true);
    WiFi.persistent(false);
    WiFi.setTxPower(WIFI_POWER_8_5dBm)

    WiFi.begin(ssid, password);

    Serial.print("WiFi connecting");

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    Serial.println("\nWiFi connected");
    Serial.println(WiFi.localIP());

    blinkLED(BLUE_LED_PIN, 3, 200);
    digitalWrite(BLUE_LED_PIN, HIGH);
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
            client.publish(topic_statusrelay, "ON");
        }
        else if (msg == "OFF")
        {
            digitalWrite(RELAY_PIN, LOW);
            relayState = false;
            client.publish(topic_statusrelay, "OFF");
        }
    }

    // ================= TIMER =================
    else if (String(topic) == topic_timer)
    {
        timerDuration = msg.toInt() * 1000; // detik → ms
        timerStartMillis = millis();
        timerActive = true;

        client.publish(topic_timer_status, "TIMER STARTED");
    }

    // ================= SCHEDULE =================
    else if (String(topic) == topic_schedule)
    {
        // format: HH:MM
        int separator = msg.indexOf(':');
        if (separator != -1)
        {
            schedHour = msg.substring(0, separator).toInt();
            schedMinute = msg.substring(separator + 1).toInt();

            scheduleActive = true;

            client.publish(topic_schedule_status, "SCHEDULE SET");
        }
        else
        {
            client.publish(topic_schedule_status, "FORMAT ERROR");
        }
    }
}

// ================= MQTT CONNECT MODIF =================
void reconnect()
{
    while (!client.connected())
    {
        Serial.print("Connecting MQTT...");

        if (client.connect(client_id, mqtt_user, mqtt_pass,
                           topic_device_status, 0, true, "OFFLINE"))
        {
            Serial.println("connected");

            // 🔥 KIRIM STATUS ONLINE
            client.publish(topic_device_status, "ONLINE", true);

            // 🔥 SUBSCRIBE
            client.subscribe(topic_control);
            client.subscribe(topic_timer);
            client.subscribe(topic_schedule);
        }
        else
        {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            delay(2000);
        }
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

            client.publish(topic_timer_status, "TIMER_DONE");
        }
    }
}

void handleSchedule()
{
    if (scheduleActive)
    {
        Time timeRTC = rtc.time();

        if (timeRTC.hr == schedHour && timeRTC.min == schedMinute)
        {
            if (!scheduleTriggered)
            {
                scheduleTriggered = true;

                relayState = !relayState;
                digitalWrite(RELAY_PIN, relayState);

                client.publish(topic_schedule_status, "SCHEDULE_TRIGGER");
            }
        }
        else
        {
            scheduleTriggered = false;
        }
    }
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

    start_wifi();

    espClient.setCACert(ca_cert);

    client.setServer(mqtt_server, mqtt_port);
    client.setCallback(callback);
    client.setKeepAlive(60);
    client.setKeepAlive(60);

    rtc.writeProtect(false);
    rtc.halt(false);

    // ===== SET WAKTU SEKALI SAJA =====
    Time timeRTC(2026, 2, 6, 10, 30, 0, Time::kFriday);
    rtc.time(timeRTC);

    PZEMSerial.begin(9600, SERIAL_8N1, PZEM_RX_PIN, PZEM_TX_PIN);
}

// ================= LOOP =================
void loop()
{
    if (!client.connected())
    {
        reconnect();
    }

    client.loop();

    if (millis() - lastEnergy > 2000)
    {
        lastEnergy = millis();

        float voltage = pzem.voltage();
        float current = pzem.current();
        float power = pzem.power();
        float energy = pzem.energy();
        float frequency = pzem.frequency();
        float pf = pzem.pf();

        if (!isnan(voltage))
        {
            String payload = "{";

            payload += "\"voltage\":" + String(voltage, 2) + ",";
            payload += "\"current\":" + String(current, 3) + ",";
            payload += "\"power\":" + String(power, 2) + ",";
            payload += "\"energy\":" + String(energy, 3) + ",";
            payload += "\"frequency\":" + String(frequency, 1) + ",";
            payload += "\"pf\":" + String(pf, 2);

            payload += "}";

            client.publish(topic_energy, payload.c_str());

            Serial.print("Energy: ");
            Serial.println(payload);
        }
        else
        {
            Serial.println("PZEM not responding");
        }
    }

    handleTimer();
    handleSchedule();
}
