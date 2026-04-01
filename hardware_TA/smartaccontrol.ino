/**
 * EcoLab Smart AC Control (mcuB)
 * Wemos D1 Mini - ESP8266
 *
 * Features:
 * - DHT11 Temperature & Humidity Sensor (Pin D4)
 * - Daikin AC IR Control (Pin D1)
 * - MQTT Communication (TLS Insecure - No CA verification)
 *
 * MQTT Topics:
 * - Subscribe: ecolab/mcuB/ac/control
 * - Publish: ecolab/mcuB/ac/status (retain)
 * - Publish: ecolab/mcuB/dht/temperature
 * - Publish: ecolab/mcuB/dht/humidity
 * - LWT: ecolab/mcuB/status
 *
 * WARNING: TLS Insecure mode skips certificate verification!
 *          Not recommended for production use.
 */

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <IRremoteESP8266.h>
#include <IRsend.h>
#include <ir_Daikin.h>
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
const char* MQTT_USERNAME = "mcub";
const char* MQTT_PASSWORD = "mcub123";
const char* MQTT_CLIENT_ID = "ecolab_mcub";

// TLS INSECURE MODE - No CA certificate verification
// Peringatan: Mode ini tidak aman untuk production!

// Topics
const char* TOPIC_AC_CONTROL = "ecolab/mcuB/ac/control";
const char* TOPIC_AC_STATUS = "ecolab/mcuB/ac/status";
const char* TOPIC_DHT_TEMP = "ecolab/mcuB/dht/temperature";
const char* TOPIC_DHT_HUM = "ecolab/mcuB/dht/humidity";
const char* TOPIC_MCU_STATUS = "ecolab/mcuB/status";

// ============================================================
// HARDWARE CONFIG
// ============================================================
// IR LED
const uint16_t IR_LED_PIN = D1;
IRDaikinESP ac(IR_LED_PIN);

// DHT11
#define DHTPIN D4      // Pin DHT11
#define DHTTYPE DHT11     // Tipe sensor DHT11
DHT dht(DHTPIN, DHTTYPE);

// ============================================================
// AC STATE
// ============================================================
bool acState = false;           // true = ON, false = OFF
uint8_t acTemperature = 24;     // Default 24°C
uint8_t acMode = kDaikinCool;   // Default COOL mode

// Min/Max temperature
const uint8_t TEMP_MIN = 16;    // 16°C
const uint8_t TEMP_MAX = 30;    // 30°C

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
  Serial.println("EcoLab Smart AC Control (mcuB)");
  Serial.println("====================================\n");

  // Setup IR AC
  ac.begin();
  Serial.println("[AC] Daikin IR initialized (Pin D1)");

  // Setup DHT
  dht.begin();
  Serial.println("[DHT] DHT11 initialized (Pin D2)");

  // Set initial AC state (but don't send IR yet)
  ac.on();
  ac.setMode(kDaikinCool);
  ac.setTemp(acTemperature);
  ac.setFan(kDaikinFanAuto);
  ac.setSwingVertical(false);

  Serial.println("[AC] Default settings: Cool, 24°C, Fan Auto, Swing Off\n");

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
  espClient.setInsecure();

  Serial.println("[TLS] Insecure mode enabled (no certificate verification)");

  if (mqttClient.connect(MQTT_CLIENT_ID, MQTT_USERNAME, MQTT_PASSWORD, TOPIC_MCU_STATUS, 0, true, "OFFLINE")) {
    Serial.println(" connected!");

    // Subscribe to AC control topic
    mqttClient.subscribe(TOPIC_AC_CONTROL);
    Serial.print("[MQTT] Subscribed: ");
    Serial.println(TOPIC_AC_CONTROL);

    // Send MCU status
    mqttClient.publish(TOPIC_MCU_STATUS, "ONLINE", true);
    Serial.print("[MQTT] Published: ");
    Serial.print(TOPIC_MCU_STATUS);
    Serial.println(" -> ONLINE (retain)");

    // Send initial AC status
    sendACStatus();

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

  // Parse AC command
  if (strcmp(topic, TOPIC_AC_CONTROL) == 0) {
    handleACCommand(message);
  }
}

// ============================================================
// AC CONTROL FUNCTIONS
// ============================================================
void handleACCommand(char* command) {
  if (strcmp(command, "ON") == 0) {
    // Turn ON AC
    acState = true;
    ac.on();
    sendIR();
    Serial.println("[AC] Power: ON");
    sendACStatus();
  }
  else if (strcmp(command, "OFF") == 0) {
    // Turn OFF AC
    acState = false;
    ac.off();
    sendIR();
    Serial.println("[AC] Power: OFF");
    sendACStatus();
  }
  else if (strcmp(command, "TEMP_UP") == 0) {
    // Increase temperature
    if (acState) {
      if (acTemperature < TEMP_MAX) {
        acTemperature++;
        ac.setTemp(acTemperature);
        sendIR();
        Serial.print("[AC] Temperature: ");
        Serial.print(acTemperature);
        Serial.println("°C");
        sendACStatus();
      } else {
        Serial.println("[AC] Already at max temperature");
      }
    } else {
      Serial.println("[AC] Cannot change temp: AC is OFF");
    }
  }
  else if (strcmp(command, "TEMP_DOWN") == 0) {
    // Decrease temperature
    if (acState) {
      if (acTemperature > TEMP_MIN) {
        acTemperature--;
        ac.setTemp(acTemperature);
        sendIR();
        Serial.print("[AC] Temperature: ");
        Serial.print(acTemperature);
        Serial.println("°C");
        sendACStatus();
      } else {
        Serial.println("[AC] Already at min temperature");
      }
    } else {
      Serial.println("[AC] Cannot change temp: AC is OFF");
    }
  }
  else if (strcmp(command, "MODE_COOL") == 0) {
    // Set mode to COOL
    if (acState) {
      acMode = kDaikinCool;
      ac.setMode(kDaikinCool);
      sendIR();
      Serial.println("[AC] Mode: COOL");
      sendACStatus();
    } else {
      Serial.println("[AC] Cannot change mode: AC is OFF");
    }
  }
  else if (strcmp(command, "MODE_FAN") == 0) {
    // Set mode to FAN
    if (acState) {
      acMode = kDaikinFan;
      ac.setMode(kDaikinFan);
      sendIR();
      Serial.println("[AC] Mode: FAN");
      sendACStatus();
    } else {
      Serial.println("[AC] Cannot change mode: AC is OFF");
    }
  }
}

void sendIR() {
  // Apply settings before sending
  ac.setFan(kDaikinFanAuto);
  ac.setSwingVertical(false);
  ac.send();
  Serial.println("[IR] Command sent!");
}

void sendACStatus() {
  // Publish AC state (ON/OFF)
  const char* payload = acState ? "ON" : "OFF";
  mqttClient.publish(TOPIC_AC_STATUS, payload, true);  // retain = true

  Serial.print("[MQTT] Published: ");
  Serial.print(TOPIC_AC_STATUS);
  Serial.print(" -> ");
  Serial.print(payload);
  Serial.println(" (retain)");
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
