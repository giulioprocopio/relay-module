#include <Arduino.h>
#include <Preferences.h>

#include "config.h"
#include "hardware.h"

Preferences preferences;

void setup() {
  Serial.begin(SERIAL_BAUD_RATE);

  pinMode(LED_BUILTIN_PIN, OUTPUT);

  if (!preferences.begin("factory", true)) {
    Serial.println("Failed to initialize preferences");
    return;
  }

  String pop = preferences.getString("pop", "def_pop");
  String name = preferences.getString("name", "def_name");

  Serial.println("POP: " + pop);
  Serial.println("Name: " + name);

  preferences.end();
}

void loop() {
  digitalWrite(LED_BUILTIN_PIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN_PIN, LOW);
  delay(1000);
}
