/*
 * EcoLab MCU A - Lamp Control & DHT Sensor
 * Platform: Wemos D1 Mini (ESP8266)
 * Broker: MQTT over TLS
 *
 * Features:
 * - Control relay 1-5 via MQTT
 * - Send status relay via MQTT
 * - DHT11 sensor data (random for testing)
 * - LWT (Last Will Testament) for online status
 */

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>


// ================= WIFI =================
// const char *ssid = "3KSERA";
// const char *password = "04115474";

const char *ssid = "ya gak punya kuota ya? wkwkwk";
const char *password = "debritto21";


// ============================================================
// MQTT BROKER CONFIG (TLS)
// ============================================================
// const char* MQTT_BROKER = "192.168.100.7";
const char* MQTT_BROKER = "10.65.124.151";
const int MQTT_PORT = 8883;

// MQTT Credentials
const char* MQTT_USERNAME = "mcua";
const char* MQTT_PASSWORD = "mcua123";

// CA Certificate (paste your CA certificate here)
const char* ca_cert = R"EOF(
-----BEGIN CERTIFICATE-----
MIIDrTCCApWgAwIBAgIUKjQ9PvlPW8wZDIeg0DCHL2DpIQMwDQYJKoZIhvcNAQEL
BQAwZjELMAkGA1UEBhMCSUQxDDAKBgNVBAgMA0RJWTETMBEGA1UEBwwKWW9neWFr
YXJ0YTEPMA0GA1UECgwGRWNvTGFiMQ8wDQYDVQQLDAZFY29MYWIxEjAQBgNVBAMM
CUVjb0xhYi1DQTAeFw0yNjAzMDYxMjUxMTJaFw0zNjAzMDMxMjUxMTJaMGYxCzAJ
BgNVBAYTAklEMQwwCgYDVQQIDANISVkxEzARBgNVBAcMCllvZ3lha2FydGExDzAN
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

// MQTT Client ID
const char* MQTT_CLIENT_ID = "ecolab_mcua_wemos";

// ============================================================
// MQTT TOPICS
// ============================================================
// Command topics (GUI → ESP8266)
const char* TOPIC_LAMP_CMD_PREFIX = "ecolab/mcuA/lamp";

// Status topics (ESP8266 → GUI)
const char* TOPIC_LAMP_STATUS_PREFIX = "ecolab/mcuA/lamp";
const char* TOPIC_DHT_TEMP = "ecolab/mcuA/dht/temperature";
const char* TOPIC_DHT_HUM = "ecolab/mcuA/dht/humidity";
const char* TOPIC_MCU_STATUS = "ecolab/mcuA/status";

// LWT Topic
const char* TOPIC_LWT = "ecolab/mcuA/status";

// ============================================================
// PIN CONFIGURATION (Wemos D1 Mini)
// ============================================================
// GPIO mapping untuk Wemos D1 Mini
// D1=GPIO5, D2=GPIO4, D3=GPIO0, D4=GPIO2, D5=GPIO14
// D6=GPIO12, D7=GPIO13, D8=GPIO15
const int RELAY_PINS[5] = {5, 4, 0, 2, 14};  // Relay 1-5 (D1, D2, D3, D4, D5)
const int NUM_RELAYS = 5;

// ============================================================
// GLOBAL VARIABLES
// ============================================================
WiFiClientSecure espClient;
PubSubClient mqtt_client(espClient);
BearSSL::X509List cert(ca_cert);

// Relay states
bool relay_states[5] = {false, false, false, false, false};

// Timers
unsigned long last_dht_time = 0;
const long DHT_INTERVAL = 2000;  // Send DHT data every 2 seconds

// ============================================================
// FUNCTION DECLARATIONS
// ============================================================
void setup_wifi();
void setup_mqtt();
void reconnect_mqtt();
void callback(char* topic, byte* payload, unsigned int length);
void control_relay(int relay_index, bool state);
void send_relay_status(int relay_index);
void send_all_relay_status();
void send_dht_data();
void send_mcu_status(const char* status);
float get_random_temperature();
float get_random_humidity();

// ============================================================
// SETUP
// ============================================================
void setup() {
  // Initialize Serial
  Serial.begin(115200);
  Serial.println("\n\n=== EcoLab MCU A - Lamp Control ===\n");

  // Initialize Relay Pins
  for (int i = 0; i < NUM_RELAYS; i++) {
    pinMode(RELAY_PINS[i], OUTPUT);
    digitalWrite(RELAY_PINS[i], LOW);  // Initial OFF
    Serial.printf("Relay %d: GPIO%d initialized\n", i + 1, RELAY_PINS[i]);
  }
  Serial.println("");

  // Setup WiFi
  setup_wifi();

  // Setup MQTT
  setup_mqtt();
}

// ============================================================
// WIFI SETUP
// ============================================================
void setup_wifi() {
  Serial.print("Connecting to WiFi...");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println(" connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

// ============================================================
// MQTT SETUP
// ============================================================
void setup_mqtt() {
  // Set buffer sizes untuk TLS (ESP8266 butuh lebih besar)
  espClient.setBufferSizes(512, 512);

  // Set CA certificate for TLS using BearSSL
  espClient.setTrustAnchors(&cert);

  // Configure MQTT client
  mqtt_client.setServer(MQTT_BROKER, MQTT_PORT);
  mqtt_client.setCallback(callback);
  mqtt_client.setKeepAlive(60);
  mqtt_client.setSocketTimeout(30);

  // Connect to MQTT broker
  reconnect_mqtt();
}

// ============================================================
// MQTT RECONNECT
// ============================================================
void reconnect_mqtt() {
  while (!mqtt_client.connected()) {
    Serial.print("Attempting MQTT connection...");

    // Attempt to connect with username/password dan LWT
    // connect(clientId, username, password, willTopic, willQoS, willRetain, willMessage)
    if (mqtt_client.connect(MQTT_CLIENT_ID, MQTT_USERNAME, MQTT_PASSWORD, TOPIC_LWT, 0, true, "OFFLINE")) {
      Serial.println(" connected!");

      // Send online status
      send_mcu_status("ONLINE");

      // Subscribe to lamp command topics
      for (int i = 1; i <= NUM_RELAYS; i++) {
        char topic[50];
        sprintf(topic, "%s%d/control", TOPIC_LAMP_CMD_PREFIX, i);
        mqtt_client.subscribe(topic);
        Serial.printf("Subscribed to: %s\n", topic);
      }

      // Send initial relay status
      send_all_relay_status();

    } else {
      Serial.print(" failed, rc=");
      Serial.print(mqtt_client.state());
      Serial.println(" retrying in 5 seconds");
      delay(5000);
    }
  }
}

// ============================================================
// MQTT CALLBACK (Receive Commands)
// ============================================================
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.printf("\n[MQTT] Message received\n");
  Serial.printf("Topic: %s\n", topic);

  // Convert payload to string
  char message[length + 1];
  memcpy(message, payload, length);
  message[length] = '\0';
  Serial.printf("Payload: %s\n", message);

  // Parse lamp index from topic
  // Topic format: ecolab/mcuA/lamp1/control
  String topicStr = String(topic);

  if (topicStr.indexOf(TOPIC_LAMP_CMD_PREFIX) == 0) {
    // Extract lamp number: ecolab/mcuA/lamp1/control → 1
    int lamp_index = topicStr.substring(
      topicStr.lastIndexOf("lamp") + 4,
      topicStr.lastIndexOf("/")
    ).toInt();

    if (lamp_index >= 1 && lamp_index <= NUM_RELAYS) {
      // Control relay
      if (String(message) == "ON") {
        control_relay(lamp_index, true);
      } else if (String(message) == "OFF") {
        control_relay(lamp_index, false);
      }
    }
  }
}

// ============================================================
// CONTROL RELAY
// ============================================================
void control_relay(int relay_index, bool state) {
  if (relay_index < 1 || relay_index > NUM_RELAYS) return;

  int pin_index = relay_index - 1;

  // Set relay state
  digitalWrite(RELAY_PINS[pin_index], state ? HIGH : LOW);
  relay_states[pin_index] = state;

  Serial.printf("Relay %d: %s\n", relay_index, state ? "ON" : "OFF");

  // Send status
  send_relay_status(relay_index);
}

// ============================================================
// SEND RELAY STATUS
// ============================================================
void send_relay_status(int relay_index) {
  if (relay_index < 1 || relay_index > NUM_RELAYS) return;

  int pin_index = relay_index - 1;
  bool state = relay_states[pin_index];

  char topic[50];
  sprintf(topic, "%s%d/status", TOPIC_LAMP_STATUS_PREFIX, relay_index);

  const char* payload = state ? "ON" : "OFF";

  // Publish dengan retain=True agar status tersimpan di broker
  if (mqtt_client.publish(topic, payload, true)) {
    Serial.printf("[MQTT] Published: %s → %s (retain)\n", topic, payload);
  } else {
    Serial.printf("[MQTT] Failed to publish: %s\n", topic);
  }
}

// ============================================================
// SEND ALL RELAY STATUS
// ============================================================
void send_all_relay_status() {
  for (int i = 1; i <= NUM_RELAYS; i++) {
    send_relay_status(i);
    delay(100);  // Small delay between messages
  }
}

// ============================================================
// SEND DHT DATA (Random for Testing)
// ============================================================
void send_dht_data() {
  // Generate random temperature (20-30°C)
  float temperature = get_random_temperature();

  // Generate random humidity (40-80%)
  float humidity = get_random_humidity();

  // Send temperature
  char temp_str[10];
  dtostrf(temperature, 2, 1, temp_str);
  if (mqtt_client.publish(TOPIC_DHT_TEMP, temp_str)) {
    Serial.printf("[MQTT] Published: %s → %s°C\n", TOPIC_DHT_TEMP, temp_str);
  }

  // Send humidity
  char hum_str[10];
  dtostrf(humidity, 2, 1, hum_str);
  if (mqtt_client.publish(TOPIC_DHT_HUM, hum_str)) {
    Serial.printf("[MQTT] Published: %s → %s%%\n", TOPIC_DHT_HUM, hum_str);
  }
}

// ============================================================
// SEND MCU STATUS
// ============================================================
void send_mcu_status(const char* status) {
  if (mqtt_client.publish(TOPIC_MCU_STATUS, status, true)) {
    Serial.printf("[MQTT] Published: %s → %s (retain)\n", TOPIC_MCU_STATUS, status);
  }
}

// ============================================================
// RANDOM DATA GENERATORS (For Testing)
// ============================================================
float get_random_temperature() {
  // Random temperature between 20-30°C
  return random(200, 301) / 10.0;
}

float get_random_humidity() {
  // Random humidity between 40-80%
  return random(40, 81);
}

// ============================================================
// MAIN LOOP
// ============================================================
void loop() {
  // Check MQTT connection
  if (!mqtt_client.connected()) {
    reconnect_mqtt();
  }
  mqtt_client.loop();

  // Send DHT data every 2 seconds
  unsigned long current_time = millis();
  if (current_time - last_dht_time >= DHT_INTERVAL) {
    last_dht_time = current_time;
    send_dht_data();
  }

  delay(100);  // Small delay
}
