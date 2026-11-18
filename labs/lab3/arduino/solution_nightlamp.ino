// Lab 3 - Try-this solution: automatic night lamp
// LDR module AO -> GPIO 35. In Wokwi the AO value RISES when it gets darker.
const int LDR_PIN = 35;
const int LED_PIN = 26;
int DARK_THRESHOLD = 2000;   // calibrate: watch the printed values, then choose

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int light = analogRead(LDR_PIN);
  bool dark = light > DARK_THRESHOLD;
  digitalWrite(LED_PIN, dark);
  Serial.printf("ldr:%d lamp:%s\n", light, dark ? "ON" : "OFF");
  delay(200);
}
