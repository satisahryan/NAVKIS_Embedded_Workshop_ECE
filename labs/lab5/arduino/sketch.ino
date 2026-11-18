// Lab 5 - Your ESP32 on the Internet (MQTT)
// DHT22 -> GPIO 15, LED -> GPIO 26. Joins Wokwi's virtual Wi-Fi, publishes
// readings every 5 s, and listens for ON/OFF commands from the class dashboard.
#include <WiFi.h>
#include <PubSubClient.h>
#include "DHTesp.h"

// ======= CHANGE THIS: your name or USN (letters/numbers only, no spaces) =======
const char* STUDENT = "your-name";
// ===============================================================================

const char* MQTT_BROKER = "broker.hivemq.com";   // free public broker
const int   MQTT_PORT   = 1883;
const char* TOPIC_ROOT  = "navkis/ews2026";      // must match the dashboard

const int DHT_PIN = 15;
const int LED_PIN = 26;

WiFiClient net;
PubSubClient mqtt(net);
DHTesp dht;
String dataTopic, ledTopic;
unsigned long lastSend = 0;

// Called whenever a message arrives on a topic we subscribed to
void onMessage(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (unsigned int i = 0; i < length; i++) msg += (char)payload[i];
  Serial.printf("Message on %s: %s\n", topic, msg.c_str());
  if (msg == "ON")  digitalWrite(LED_PIN, HIGH);
  if (msg == "OFF") digitalWrite(LED_PIN, LOW);
}

void connectWiFi() {
  Serial.print("Connecting to Wi-Fi");
  WiFi.begin("Wokwi-GUEST", "", 6);       // open network, channel 6
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }
  Serial.print(" connected! IP = ");
  Serial.println(WiFi.localIP());
}

void connectMQTT() {
  while (!mqtt.connected()) {
    String clientId = "navkis-" + String(STUDENT) + "-" + String(random(0xffff), HEX);
    Serial.print("Connecting to MQTT broker... ");
    if (mqtt.connect(clientId.c_str())) {
      Serial.println("connected!");
      mqtt.subscribe(ledTopic.c_str());
      Serial.println("Listening on " + ledTopic);
    } else {
      Serial.printf("failed (state %d), retrying in 2 s\n", mqtt.state());
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  dht.setup(DHT_PIN, DHTesp::DHT22);
  randomSeed(micros());

  dataTopic = String(TOPIC_ROOT) + "/" + STUDENT + "/data";
  ledTopic  = String(TOPIC_ROOT) + "/" + STUDENT + "/led";

  connectWiFi();
  mqtt.setServer(MQTT_BROKER, MQTT_PORT);
  mqtt.setCallback(onMessage);
}

void loop() {
  if (!mqtt.connected()) connectMQTT();
  mqtt.loop();                            // handle incoming messages

  if (millis() - lastSend > 5000) {       // publish every 5 seconds
    lastSend = millis();
    TempAndHumidity d = dht.getTempAndHumidity();
    char json[96];
    snprintf(json, sizeof(json), "{\"t\":%.1f,\"h\":%.1f,\"led\":%d}",
             d.temperature, d.humidity, digitalRead(LED_PIN));
    mqtt.publish(dataTopic.c_str(), json);
    Serial.printf("Published to %s: %s\n", dataTopic.c_str(), json);
  }
}
