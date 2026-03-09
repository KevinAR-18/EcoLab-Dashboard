#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>

#define LED_PIN 8

// ================= WIFI =================

const char* ssid = "ya gak punya kuota ya? wkwkwk";
const char* password = "debritto21";

// ================= MQTT =================

const char* mqtt_server="10.139.6.151";
const int mqtt_port = 8883;

const char* mqtt_user = "smartsocket1";
const char* mqtt_pass = "smart1";

// MQTT topics
const char* topic_control = "ecolab/socket/1/control";
const char* topic_energy  = "ecolab/socket/1/energy";
const char* topic_status  = "ecolab/socket/1/status";

// TLS CA CERT
const char* ca_cert = R"EOF(
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

WiFiClientSecure espClient;
PubSubClient client(espClient);

bool blink_enable = false;
unsigned long lastBlink = 0;
bool ledState = false;

unsigned long lastEnergy = 0;


// ================= LED BLINK =================
void blinkLed(int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(200);
    digitalWrite(LED_PIN, LOW);
    delay(200);
  }
}


// ================= WIFI =================
void start_wifi() {

  WiFi.mode(WIFI_STA);

  WiFi.setSleep(false);
  WiFi.setAutoReconnect(true);
  WiFi.persistent(false);
  WiFi.setTxPower(WIFI_POWER_8_5dBm);

  WiFi.begin(ssid, password);

  Serial.print("WiFi connecting");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  blinkLed(3);
}


// ================= MQTT CALLBACK =================
void callback(char* topic, byte* payload, unsigned int length) {

  String msg;

  for (int i = 0; i < length; i++) {
    msg += (char)payload[i];
  }

  Serial.print("Message: ");
  Serial.println(msg);

  if (msg == "ON") {
    blink_enable = true;
  }

  if (msg == "OFF") {
    blink_enable = false;
    digitalWrite(LED_PIN, LOW);
  }
}


// ================= MQTT CONNECT =================
void connect_mqtt() {

  while (!client.connected()) {

    Serial.print("Connecting MQTT...");

    if (client.connect("smartsocket1", mqtt_user, mqtt_pass)) {

      Serial.println("connected");

      client.subscribe(topic_control);

      client.publish(topic_status, "online");

    } else {

      Serial.print("failed rc=");
      Serial.print(client.state());
      Serial.println(" retrying...");
      delay(2000);

    }
  }
}


// ================= SETUP =================
void setup() {

  Serial.begin(115200);

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  start_wifi();

  espClient.setCACert(ca_cert);
  // espClient.setInsecure();
  // espClient.setTimeout(15000);

  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);

  Serial.print("Resolving host... ");

  IPAddress ip;
  if (WiFi.hostByName(mqtt_server, ip)) {
    Serial.print("OK -> ");
    Serial.println(ip);
  } else {
    Serial.println("FAILED");
  }
}


// ================= LOOP =================
void loop() {

  if (!client.connected()) {
    connect_mqtt();
  }

  client.loop();


  // LED BLINK CONTROL
  if (blink_enable) {

    if (millis() - lastBlink > 500) {

      lastBlink = millis();

      ledState = !ledState;
      digitalWrite(LED_PIN, ledState);

    }
  }


  // SEND RANDOM ENERGY DATA
  if (millis() - lastEnergy > 5000) {

    lastEnergy = millis();

    float volt = random(210, 230);
    float current = random(1, 5) / 10.0;
    float watt = volt * current;

    String payload =
      String(volt) + "," +
      String(current) + "," +
      String(watt);

    client.publish(topic_energy, payload.c_str());

    Serial.print("Energy: ");
    Serial.println(payload);
  }
}