#include <ArduinoJson.h>
#include <FastLED.h>

#define LED_PIN A0
#define NUM_LEDS 49  
#define LED_TYPE WS2812B
#define COLOR_ORDER GRB

CRGB leds[NUM_LEDS];

void setup() {
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  Serial.begin(115200);  
  pinMode(8, OUTPUT);   // Set D8 pin as output
  pinMode(9, OUTPUT);   // Set D9 pin as output
  digitalWrite(8, LOW); // Initialize D8 to LOW
  digitalWrite(9, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    String jsonString = Serial.readStringUntil('\n'); // Read until newline

    DynamicJsonDocument doc(1024);
    DeserializationError error = deserializeJson(doc, jsonString);

    if (!error) {
      bool green = doc["green"];
      bool red = doc["red"];
      digitalWrite(8, red);
      digitalWrite(9, green);
      JsonArray dataArray = doc["data"];

      for (int i = 0; i < dataArray.size(); i++) {
        byte row = dataArray[i];
        leds[i] = (row == 1) ? CRGB::White : (row==2)? CRGB::Yellow : CRGB::Black;
      }
      FastLED.show();
    } else {
      Serial.println("Invalid JSON data");
    }
  }
}
