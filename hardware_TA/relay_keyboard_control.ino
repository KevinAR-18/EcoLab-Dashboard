/**
 * Relay Control via Keyboard (Serial Monitor)
 * Wemos D1 Mini - ESP8266
 *
 * Pin Relay: D1, D2, D5, D6, D7
 * Trigger: Keyboard 1-5
 *
 * OUTPUT MODE: OUTPUT_OPEN_DRAIN
 * - LOW  = Relay ON (sink ke GND)
 * - HIGH = Relay OFF (floating)
 */

// ----------- PIN RELAY -----------
const int relayPins[5] = {D1, D2, D5, D6, D7};

// State relay (true = ON, false = OFF)
bool relayState[5] = {false, false, false, false, false};

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Setup semua relay pin sebagai OUTPUT_OPEN_DRAIN
  for (int i = 0; i < 5; i++) {
    pinMode(relayPins[i], OUTPUT_OPEN_DRAIN);
    digitalWrite(relayPins[i], HIGH);  // Default OFF (floating)
  }

  Serial.println("=== RELAY CONTROL ===");
  Serial.println("Pin Relay: D1, D2, D5, D6, D7");
  Serial.println();
  Serial.println("KONTROL VIA KEYBOARD:");
  Serial.println("  1 = Toggle Relay 1 (D1)");
  Serial.println("  2 = Toggle Relay 2 (D2)");
  Serial.println("  3 = Toggle Relay 3 (D5)");
  Serial.println("  4 = Toggle Relay 4 (D6)");
  Serial.println("  5 = Toggle Relay 5 (D7)");
  Serial.println();
  Serial.println("  a = All ON");
  Serial.println("  s = All OFF");
  Serial.println("  ? = Status");
  Serial.println();
  Serial.println("Siap menerima input...\n");
}

void loop() {
  if (Serial.available() > 0) {
    char input = Serial.read();

    // Toggle relay 1-5
    if (input >= '1' && input <= '5') {
      int relayIndex = input - '1';  // '1' -> 0, '2' -> 1, dst.

      relayState[relayIndex] = !relayState[relayIndex];

      // OUTPUT_OPEN_DRAIN: LOW = ON, HIGH = OFF (floating)
      digitalWrite(relayPins[relayIndex], relayState[relayIndex] ? LOW : HIGH);

      Serial.print("Relay ");
      Serial.print(relayIndex + 1);
      Serial.print(" (D");
      Serial.print((String[]){"1", "2", "5", "6", "7"}[relayIndex]);
      Serial.print("): ");
      Serial.println(relayState[relayIndex] ? "ON" : "OFF");
    }

    // All ON
    else if (input == 'a' || input == 'A') {
      for (int i = 0; i < 5; i++) {
        relayState[i] = true;
        digitalWrite(relayPins[i], LOW);  // LOW = ON (sink to GND)
      }
      Serial.println(">>> All RELAY ON <<<");
    }

    // All OFF
    else if (input == 's' || input == 'S') {
      for (int i = 0; i < 5; i++) {
        relayState[i] = false;
        digitalWrite(relayPins[i], HIGH);  // HIGH = OFF (floating)
      }
      Serial.println(">>> All RELAY OFF <<<");
    }

    // Status
    else if (input == '?') {
      printStatus();
    }

    // Unknown
    else if (input != '\n' && input != '\r') {
      Serial.print("Unknown: ");
      Serial.println(input);
    }
  }
}

void printStatus() {
  Serial.println("\n=== RELAY STATUS ===");
  for (int i = 0; i < 5; i++) {
    Serial.print("Relay ");
    Serial.print(i + 1);
    Serial.print(" (D");
    Serial.print((String[]){"1", "2", "5", "6", "7"}[i]);
    Serial.print("): ");
    Serial.println(relayState[i] ? "ON" : "OFF");
  }
  Serial.println("===================\n");
}
