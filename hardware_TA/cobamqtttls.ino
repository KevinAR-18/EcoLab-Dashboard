#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>

// ================= CONFIG =================

#define LED_PIN 8

const char* ssid = "ya gak punya kuota ya? wkwkwk";
const char* password = "debritto21q";

const char* mqtt_server = "DESKTOP-CVPE153";
const int mqtt_port = 8883;

// ================= CA CERTIFICATE =================
// Copy isi file ca.crt dari broker kamu

const char* ca_cert = R"EOF(
-----BEGIN CERTIFICATE-----
PASTE_ISI_CA_CRT_DISINI
-----END CERTIFICATE-----
)EOF";

// ================= MQTT OBJECT =================

WiFiClientSecure espClient;
PubSubClient client(espClient);

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
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  blinkLed(3);
  digitalWrite(LED_PIN, LOW);
}

// ================= MQTT CONNECT =================

void connect_mqtt() {

  while (!client.connected()) {

    Serial.print("Connecting MQTT...");

    if (client.connect("ESP32C3_Client")) {

      Serial.println("connected");

      blinkLed(5);   // indikator MQTT connect

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

  espClient.setCACert(ca_cert);   // TLS verification

  client.setServer(mqtt_server, mqtt_port);
}

// ================= LOOP =================

void loop() {

  if (!client.connected()) {
    connect_mqtt();
  }

  client.loop();

  static unsigned long lastMsg = 0;

  if (millis() - lastMsg > 5000) {

    lastMsg = millis();

    String message = "Halo dari ESP32C3";

    client.publish("test/topic", message.c_str());

    Serial.println("Published: " + message);
  }
}