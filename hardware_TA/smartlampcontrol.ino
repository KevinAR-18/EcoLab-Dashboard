/**
 * EcoLab Smart Lamp Control (mcuA)
 * Wemos D1 Mini - ESP8266
 *
 * Features:
 * - DHT22 Temperature & Humidity Sensor (Pin D4)
 * - 5x Relay Control (Pin D1, D2, D5, D6, D7)
 * - MQTT Communication (TLS Insecure - No CA verification)
 *
 * MQTT Topics:
 * - Subscribe: ecolab/mcuA/lamp1-5/control
 * - Publish: ecolab/mcuA/lamp1-5/status (retain)
 * - Publish: ecolab/mcuA/dht/temperature
 * - Publish: ecolab/mcuA/dht/humidity
 * - LWT: ecolab/mcuA/status
 *
 * WARNING: TLS Insecure mode skips certificate verification!
 *          Not recommended for production use.
 */

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <WiFiClientSecure.h>

// ============================================================
// WIFI CONFIG
// ============================================================
const char* WIFI_SSID = "EcoLab";        // Ganti dengan WiFi SSID
const char* WIFI_PASSWORD = "ecolab321"; // Ganti dengan WiFi Password

// ============================================================
// MQTT CONFIG
// ============================================================
const char* MQTT_BROKER = "10.33.11.148";  // Ganti dengan IP broker
const int MQTT_PORT = 8883;                   // TLS
const char* MQTT_USERNAME = "mcua";
const char* MQTT_PASSWORD = "mcua123";
const char* MQTT_CLIENT_ID = "ecolab_mcua";

// Topics
const char* TOPIC_LAMP_CMD_PREFIX = "ecolab/mcuA/lamp";
const char* TOPIC_LAMP_STATUS_PREFIX = "ecolab/mcuA/lamp";
const char* TOPIC_DHT_TEMP = "ecolab/mcuA/dht/temperature";
const char* TOPIC_DHT_HUM = "ecolab/mcuA/dht/humidity";
const char* TOPIC_MCU_STATUS = "ecolab/mcuA/status";

// ============================================================
// HARDWARE CONFIG
// ============================================================
// DHT22
#define DHTPIN D4         // Pin DHT22 (GPIO2)
#define DHTTYPE DHT22     // Tipe sensor
DHT dht(DHTPIN, DHTTYPE);

// Relay
const int relayPins[5] = {D1, D2, D5, D6, D7};
bool relayStates[5] = {false, false, false, false, false};

// ============================================================
// GLOBAL VARIABLES
// ============================================================
WiFiClientSecure espClient;
PubSubClient mqttClient(espClient);

unsigned long lastDHTTime = 0;
const unsigned long DHT_INTERVAL = 2000;  // 2 detik

unsigned long lastReconnectAttempt = 0;
const unsigned long RECONNECT_INTERVAL = 5000;  // 5 detik

// ============================================================
// SETUP
// ============================================================
void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("\n====================================");
  Serial.println("EcoLab Smart Lamp Control (mcuA)");
  Serial.println("====================================\n");

  // Setup DHT
  dht.begin();
  Serial.println("[DHT] DHT22 initialized (Pin D4)");

  // Setup Relay pins
  for (int i = 0; i < 5; i++) {
    pinMode(relayPins[i], OUTPUT_OPEN_DRAIN);
    digitalWrite(relayPins[i], HIGH);  // Default OFF
  }
  Serial.println("[RELAY] 5 relays initialized (D1, D2, D5, D6, D7)");
  Serial.println("[RELAY] Mode: OUTPUT_OPEN_DRAIN (LOW=ON, HIGH=OFF)\n");

  // Connect WiFi
  connectWiFi();

  // Setup MQTT - TLS Insecure Mode (tanpa CA certificate)
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  mqttClient.setCallback(mqttCallback);

  // ESP8266: Set insecure mode (skip certificate verification)
  espClient.setInsecure();

  // ESP8266: Increase buffer size untuk TLS
  espClient.setBufferSizes(2048, 2048);

  Serial.println("\n[INFO] Setup complete. Starting loop...\n");
}

// ============================================================
// MAIN LOOP
// ============================================================
void loop() {
  // MQTT Connection handling
  if (!mqttClient.connected()) {
    unsigned long now = millis();
    if (now - lastReconnectAttempt >= RECONNECT_INTERVAL) {
      lastReconnectAttempt = now;
      if (reconnectMQTT()) {
        lastReconnectAttempt = 0;
      }
    }
  } else {
    mqttClient.loop();
  }

  // Send DHT data periodically
  unsigned long now = millis();
  if (now - lastDHTTime >= DHT_INTERVAL) {
    lastDHTTime = now;
    sendDHTData();
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
  Serial.print("[WIFI] Subnet Mask: ");
  Serial.println(WiFi.subnetMask());
  Serial.print("[WIFI] Signal Strength (RSSI): ");
  Serial.print(WiFi.RSSI());
  Serial.println(" dBm");
  Serial.print("[WIFI] MAC Address: ");
  Serial.println(WiFi.macAddress());
  Serial.println("====================");
}

// ============================================================
// MQTT FUNCTIONS
// ============================================================
bool reconnectMQTT() {
  Serial.print("[MQTT] Connecting to ");
  Serial.print(MQTT_BROKER);
  Serial.print("...");

  // ESP8266: Insecure mode (skip certificate verification)
  // Note: setInsecure() sudah dipanggil di setup()

  if (mqttClient.connect(MQTT_CLIENT_ID, MQTT_USERNAME, MQTT_PASSWORD, TOPIC_MCU_STATUS, 0, true, "OFFLINE")) {
    Serial.println(" connected!");

    // Subscribe to lamp control topics
    for (int i = 1; i <= 5; i++) {
      char topic[50];
      sprintf(topic, "%s%d/control", TOPIC_LAMP_CMD_PREFIX, i);
      mqttClient.subscribe(topic);
      Serial.print("[MQTT] Subscribed: ");
      Serial.println(topic);
    }

    // Send MCU status
    mqttClient.publish(TOPIC_MCU_STATUS, "ONLINE", true);
    Serial.print("[MQTT] Published: ");
    Serial.print(TOPIC_MCU_STATUS);
    Serial.println(" -> ONLINE (retain)");

    // Send initial relay status
    sendAllRelayStatus();

    return true;
  } else {
    Serial.print(" failed (rc=");
    Serial.print(mqttClient.state());
    Serial.println(")");
    return false;
  }
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  // Convert payload to string
  char message[length + 1];
  for (unsigned int i = 0; i < length; i++) {
    message[i] = (char)payload[i];
  }
  message[length] = '\0';

  Serial.print("\n[MQTT] Received: ");
  Serial.print(topic);
  Serial.print(" -> ");
  Serial.println(message);

  // Parse lamp index from topic
  // Topic format: ecolab/mcuA/lamp1/control
  if (strstr(topic, TOPIC_LAMP_CMD_PREFIX) != NULL) {
    // Extract lamp number
    char* lampPart = strstr(topic, "lamp");
    if (lampPart != NULL) {
      int lampIndex = atoi(lampPart + 4);  // Skip "lamp"

      if (lampIndex >= 1 && lampIndex <= 5) {
        if (strcmp(message, "ON") == 0) {
          controlRelay(lampIndex, true);
        } else if (strcmp(message, "OFF") == 0) {
          controlRelay(lampIndex, false);
        }
      }
    }
  }
}

// ============================================================
// RELAY CONTROL FUNCTIONS
// ============================================================
void controlRelay(int relayIndex, bool state) {
  relayStates[relayIndex - 1] = state;

  // OUTPUT_OPEN_DRAIN: LOW = ON, HIGH = OFF
  digitalWrite(relayPins[relayIndex - 1], state ? LOW : HIGH);

  Serial.print("[RELAY] Lamp ");
  Serial.print(relayIndex);
  Serial.print(": ");
  Serial.println(state ? "ON" : "OFF");

  // Publish status
  sendRelayStatus(relayIndex);
}

void sendRelayStatus(int relayIndex) {
  char topic[50];
  sprintf(topic, "%s%d/status", TOPIC_LAMP_STATUS_PREFIX, relayIndex);

  const char* payload = relayStates[relayIndex - 1] ? "ON" : "OFF";

  mqttClient.publish(topic, payload, true);  // retain = true
  Serial.print("[MQTT] Published: ");
  Serial.print(topic);
  Serial.print(" -> ");
  Serial.print(payload);
  Serial.println(" (retain)");
}

void sendAllRelayStatus() {
  Serial.println("[MQTT] Publishing all relay statuses...");
  for (int i = 1; i <= 5; i++) {
    sendRelayStatus(i);
    delay(100);
  }
}

// ============================================================
// DHT SENSOR FUNCTIONS
// ============================================================
void sendDHTData() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();

  // Check error
  if (isnan(h) || isnan(t)) {
    Serial.println("[DHT] Failed to read sensor!");
    return;
  }

  // Publish temperature
  char tempStr[10];
  dtostrf(t, 1, 1, tempStr);
  mqttClient.publish(TOPIC_DHT_TEMP, tempStr);

  // Publish humidity
  char humStr[10];
  dtostrf(h, 1, 1, humStr);
  mqttClient.publish(TOPIC_DHT_HUM, humStr);

  Serial.print("[DHT] Temp: ");
  Serial.print(tempStr);
  Serial.print("°C, Hum: ");
  Serial.print(humStr);
  Serial.println("%");
}
