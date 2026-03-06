#include <WiFi.h>
#include <PubSubClient.h>

#define LED_PIN 8

// ================= WIFI =================

const char* ssid = "ya gak punya kuota ya? wkwkwk";
const char* password = "debritto21q";

// ================= MQTT =================

const char* mqtt_server = "10.139.6.151";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

// ================= LED =================

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

// ================= MQTT =================

void connect_mqtt() {

  while (!client.connected()) {

    Serial.print("Connecting MQTT...");

    if (client.connect("ESP32C3_Client")) {

      Serial.println("connected");

      blinkLed(5);

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

  start_wifi();

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

    client.publish("test/topic", "Halo dari ESP32C3");

    Serial.println("Message sent");
  }
}