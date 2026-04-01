/**
 * MQTT TLS Test Program
 * Wemos D1 Mini - ESP8266
 *
 * Simple test untuk MQTT connection dengan TLS + CA verification
 *
 * - Connect WiFi
 * - Connect MQTT dengan TLS (port 8883)
 * - Subscribe test topic
 * - Publish test message
 * - LWT (Last Will Testament)
 */

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>

// ============================================================
// WIFI CONFIG
// ============================================================
const char* WIFI_SSID = "EcoLab";
const char* WIFI_PASSWORD = "ecolab321";

// ============================================================
// MQTT CONFIG
// ============================================================
const char* MQTT_BROKER = "10.33.11.148";
const int MQTT_PORT = 8883;  // TLS
const char* MQTT_USERNAME = "mcub";
const char* MQTT_PASSWORD = "mcub123";
const char* MQTT_CLIENT_ID = "wemos_mqtt_test";

// Topics
const char* TOPIC_TEST_SUB = "ecolab/test/subscribe";
const char* TOPIC_TEST_PUB = "ecolab/test/publish";
const char* TOPIC_LWT = "ecolab/test/status";

// ============================================================
// CA CERTIFICATE
// =========

const char* CA_CERT= R"EOF(
-----BEGIN CERTIFICATE-----
MIIDrTCCApWgAwIBAgIUKFYwJQFQ7JDUKBtRlbyz+MkxL1wwDQYJKoZIhvcNAQEL
BQAwZjELMAkGA1UEBhMCSUQxDDAKBgNVBAgMA0RJWTETMBEGA1UEBwwKWW9neWFr
YXJ0YTEPMA0GA1UECgwGRWNvTGFiMQ8wDQYDVQQLDAZFY29MYWIxEjAQBgNVBAMM
CUVjb2xhYi1DQTAeFw0yNjAzMzEwODM0NTlaFw0zNjAzMjgwODM0NTlaMGYxCzAJ
BgNVBAYTAklEMQwwCgYDVQQIDANESVkxEzARBgNVBAcMCllvZ3lha2FydGExDzAN
BgNVBAoMBkVjb0xhYjEPMA0GA1UECwwGRWNvTGFiMRIwEAYDVQQDDAlFY29sYWIt
Q0EwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDJMVvFYOUG7zs4w/sC
dvblP5v0MmumansCh3wWEAjFcLXFDC4kS0hERHw661asm4TNYl1K8XUj8uCvqN8G
Rpgqh3qnld9JEUY8tVrmLZxh0sd/B3bJ+2sQTLZTznk/N1mJS4UIatu+KYAusv/Q
QHRgtQM42rpMZpFaq3+qsTWx/cTZV3WwQWMEY6Ypr3lMI+naSB18jg7Ac321escd
K+GW20/5ScJQhrSd5g0iUETOvRzoKrqhHq4sZ1xBa0W4CGLF4UV8IGP7C118skIQ
nJajJ79obXTyAqzqzKrLIM0zc5Xxt/mbaapghsk7+/IvZUEAizwPQmU1Uj9Pr5er
4SbnAgMBAAGjUzBRMB0GA1UdDgQWBBQlQOdG4wFtYT3+0hXWfTaSnS6I5DAfBgNV
HSMEGDAWgBQlQOdG4wFtYT3+0hXWfTaSnS6I5DAPBgNVHRMBAf8EBTADAQH/MA0G
CSqGSIb3DQEBCwUAA4IBAQAk2RsxuzFzWT3WbVghHtcczDjR1u28TWFYY7jGTvgy
ZvyYWxi0PnFl8Ht/6liNvWoxVdXc0MOauIQTfq29RKLz99U9xMIqT4Vz0V/7n+Mb
sk1KwWIPbQrGe0aQaZUNtq1+0DA2BDyOpbaAxJKCqu02df5LXcHE+ZxMlIHjboHt
a+xJtxrLkMcqU0oislf/IGrs6155Sb9yszaXt9Rk1Dugrzz/QQmhXHBLyQTjxy9Q
5BwkMG4ysoqz6SrySg+s7USvNuOa4f3u2mglLwRPWNLljkf55EN22OvRN6yDL2qa
MlQOy/la90QK6a7W969cM6ZpdVh3OwthHG1/5VpwonBO
-----END CERTIFICATE-----
)EOF";

// ============================================================
// GLOBAL OBJECTS
// ============================================================
WiFiClientSecure espClient;
PubSubClient mqttClient(espClient);

unsigned long lastPublishTime = 0;
const unsigned long PUBLISH_INTERVAL = 5000;  // 5 detik

int messageCount = 0;

// ============================================================
// SETUP
// ============================================================
void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("\n====================================");
  Serial.println("MQTT TLS Test Program");
  Serial.println("====================================\n");

  // Connect WiFi
  connectWiFi();

  // Setup MQTT
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  mqttClient.setCallback(mqttCallback);

  Serial.println("\n[INFO] Setup complete. Starting loop...\n");
}

// ============================================================
// LOOP
// ============================================================
void loop() {
  // MQTT Connection handling
  if (!mqttClient.connected()) {
    Serial.println("[MQTT] Not connected. Attempting to reconnect...");
    delay(2000);

    if (reconnectMQTT()) {
      Serial.println("[MQTT] Reconnected successfully!");
    } else {
      Serial.println("[MQTT] Reconnect failed. Will try again...");
    }
  } else {
    mqttClient.loop();
  }

  // Publish test message periodically
  unsigned long now = millis();
  if (mqttClient.connected() && (now - lastPublishTime >= PUBLISH_INTERVAL)) {
    lastPublishTime = now;
    publishTestMessage();
  }
}

// ============================================================
// WIFI FUNCTIONS
// ============================================================
void connectWiFi() {
  Serial.print("[WIFI] Connecting to ");
  Serial.println(WIFI_SSID);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    attempts++;
    if (attempts > 40) {  // 20 seconds timeout
      Serial.println("\n[WIFI] Failed to connect! Restarting...");
      ESP.restart();
    }
  }

  Serial.println("\n[WIFI] Connected!");
  Serial.println("====================");
  Serial.print("[WIFI] SSID: ");
  Serial.println(WiFi.SSID());
  Serial.print("[WIFI] IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.print("[WIFI] Gateway: ");
  Serial.println(WiFi.gatewayIP());
  Serial.print("[WIFI] Signal Strength (RSSI): ");
  Serial.print(WiFi.RSSI());
  Serial.println(" dBm");
  Serial.println("====================");
  Serial.println();
  Serial.println("====================================");
  Serial.println("PING TEST FROM RASPBERRY PI:");
  Serial.print("ping ");
  Serial.println(WiFi.localIP());
  Serial.println("====================================");
  Serial.println();
}

// ============================================================
// MQTT FUNCTIONS
// ============================================================
bool reconnectMQTT() {
  Serial.print("[MQTT] Connecting to ");
  Serial.print(MQTT_BROKER);
  Serial.print(":");
  Serial.print(MQTT_PORT);
  Serial.println("...");

  // Set CA certificate untuk TLS verification
  Serial.println("[TLS] Setting CA certificate...");
  BearSSL::X509List cert(CA_CERT);
  espClient.setTrustAnchors(&cert);
  Serial.println("[TLS] CA certificate loaded successfully");

  // Connect dengan LWT
  Serial.println("[MQTT] Attempting connection with credentials...");
  if (mqttClient.connect(MQTT_CLIENT_ID, MQTT_USERNAME, MQTT_PASSWORD,
                         TOPIC_LWT, 0, true, "OFFLINE")) {
    Serial.println("[MQTT] Connected successfully!");
    Serial.println("====================");

    // Subscribe test topic
    mqttClient.subscribe(TOPIC_TEST_SUB);
    Serial.print("[MQTT] Subscribed to: ");
    Serial.println(TOPIC_TEST_SUB);

    // Send LWT online status
    mqttClient.publish(TOPIC_LWT, "ONLINE", true);
    Serial.print("[MQTT] Published to: ");
    Serial.print(TOPIC_LWT);
    Serial.println(" -> ONLINE (retain)");

    Serial.println("====================\n");
    return true;

  } else {
    Serial.print("[MQTT] Connection failed! RC = ");
    Serial.println(mqttClient.state());
    Serial.println();

    // Error codes:
    // -4 : MQTT_CONNECTION_TIMEOUT - the server didn't respond within the keepalive time
    // -3 : MQTT_CONNECTION_LOST - the network connection was broken
    // -2 : MQTT_CONNECT_FAILED - the network connection failed
    // -1 : MQTT_DISCONNECTED - the client is disconnected cleanly
    //  0 : MQTT_CONNECTED - the client is connected
    //  1 : CONNECT_BAD_PROTOCOL - the server doesn't support the requested version of MQTT
    //  2 : CONNECT_BAD_CLIENT_ID - the server rejected the client identifier
    //  3 : CONNECT_UNAVAILABLE - the server was unable to accept the connection
    //  4 : CONNECT_BAD_CREDENTIALS - the username/password were rejected
    //  5 : CONNECT_UNAUTHORIZED - the client was not authorized to connect

    return false;
  }
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  Serial.print("\n[MQTT] Message received [");
  Serial.print(topic);
  Serial.print("]: ");

  for (unsigned int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println("\n");
}

void publishTestMessage() {
  messageCount++;

  char message[100];
  sprintf(message, "Test message #%d from Wemos D1 Mini", messageCount);

  mqttClient.publish(TOPIC_TEST_PUB, message);

  Serial.print("[MQTT] Published: ");
  Serial.print(TOPIC_TEST_PUB);
  Serial.print(" -> ");
  Serial.println(message);
}
