// Lab 4 - Sensor + Display over I2C
// DHT22 data -> GPIO 15, SSD1306 OLED on I2C (SDA = GPIO 21, SCL = GPIO 22),
// alarm LED on GPIO 26 switches on above TEMP_ALARM.
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "DHTesp.h"

const int DHT_PIN = 15;
const int LED_PIN = 26;
const float TEMP_ALARM = 35.0;      // degrees C

Adafruit_SSD1306 oled(128, 64, &Wire, -1);
DHTesp dht;

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  dht.setup(DHT_PIN, DHTesp::DHT22);

  if (!oled.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {   // 0x3C = OLED I2C address
    Serial.println("OLED not found - check SDA/SCL wiring");
    while (true) delay(10);
  }
  oled.clearDisplay();
  oled.setTextColor(SSD1306_WHITE);
}

void loop() {
  TempAndHumidity d = dht.getTempAndHumidity();
  if (dht.getStatus() != 0) {
    Serial.println("DHT error: " + String(dht.getStatusString()));
    delay(2000);
    return;
  }
  bool alarm = d.temperature > TEMP_ALARM;
  digitalWrite(LED_PIN, alarm);

  Serial.printf("temp:%.1f hum:%.1f alarm:%d\n", d.temperature, d.humidity, alarm);

  oled.clearDisplay();
  oled.setTextSize(1);
  oled.setCursor(0, 0);
  oled.println("NAVKIS Weather Node");
  oled.setTextSize(2);
  oled.setCursor(0, 18);
  oled.printf("%.1f C\n", d.temperature);
  oled.printf("%.0f %%RH", d.humidity);
  if (alarm) {
    oled.setTextSize(1);
    oled.setCursor(0, 56);
    oled.print("!! HIGH TEMPERATURE !!");
  }
  oled.display();
  delay(2000);                        // DHT22 can be read at most every 2 s
}
