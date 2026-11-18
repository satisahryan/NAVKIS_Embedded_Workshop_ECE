// Lab 2 - Polling version (for comparison). Same wiring as the interrupt version.
const int BUTTON_PIN = 4;
const int LED_PIN = 26;

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  int state = digitalRead(BUTTON_PIN);     // ask the pin, again and again...
  digitalWrite(LED_PIN, state == LOW);     // LED on while the button is held
  delay(10);
}
