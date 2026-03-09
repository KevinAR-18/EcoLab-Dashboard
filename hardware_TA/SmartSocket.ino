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
const char *ssid = "ya gak punya kuota ya? wkwkwk";
const char *password = "debritto21";

// ================= MQTT =================
const char *mqtt_server = "10.139.6.151";
const int mqtt_port = 8883;

const char *mqtt_user = "smartsocket1";
const char *mqtt_pass = "smart1";

// MQTT topics
const char *topic_control = "ecolab/socket/1/control";
const char *topic_energy = "ecolab/socket/1/energy";
const char *topic_status = "ecolab/socket/1/status";

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

unsigned long lastEnergy = 0;

bool relayState = false;

// ================= WIFI =================
void start_wifi()
{

    WiFi.mode(WIFI_STA);

    WiFi.setSleep(false);
    WiFi.setAutoReconnect(true);
    WiFi.persistent(false);
    WiFi.setTxPower(WIFI_POWER_8_5dBm);  

    WiFi.begin(ssid, password);

    Serial.print("WiFi connecting");

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    Serial.println("\nWiFi connected");
    Serial.println(WiFi.localIP());
}

// ================= MQTT CALLBACK =================
void callback(char *topic, byte *payload, unsigned int length)
{

    String msg;

    for (int i = 0; i < length; i++)
    {
        msg += (char)payload[i];
    }

    Serial.print("Control Message: ");
    Serial.println(msg);

    if (msg == "ON")
    {

        digitalWrite(RELAY_PIN, HIGH);
        relayState = true;

        client.publish(topic_status, "ON");
    }

    if (msg == "OFF")
    {

        digitalWrite(RELAY_PIN, LOW);
        relayState = false;

        client.publish(topic_status, "OFF");
    }
}

// ================= MQTT CONNECT =================
void connect_mqtt()
{

    while (!client.connected())
    {

        Serial.print("Connecting MQTT...");

        if (client.connect("smartsocket1", mqtt_user, mqtt_pass))
        {

            Serial.println("connected");

            client.subscribe(topic_control);

            client.publish(topic_status, "online");
        }
        else
        {

            Serial.print("failed rc=");
            Serial.println(client.state());

            delay(2000);
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

    // RTC init
    rtc.writeProtect(false);
    rtc.halt(false);

    // PZEM start
    PZEMSerial.begin(9600, SERIAL_8N1, PZEM_RX_PIN, PZEM_TX_PIN);
}

// ================= LOOP =================
void loop()
{

    if (!client.connected())
    {
        connect_mqtt();
    }

    client.loop();

    // ================= ENERGY DATA =================
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
}