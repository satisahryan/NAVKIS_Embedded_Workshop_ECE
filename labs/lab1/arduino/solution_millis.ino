// Lab 1 - Try-this solution: two LEDs at two different rates WITHOUT delay()
// Red LED on GPIO 26 toggles every 500 ms, green LED on GPIO 27 every 130 ms.

const int RED_PIN = 26;
const int GREEN_PIN = 27;

unsigned long lastRed = 0, lastGreen = 0;   // time of the last toggle
bool redOn = false, greenOn = false;

void setup() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
}

void loop() {
  unsigned long now = millis();             // ms since the board started

  if (now - lastRed >= 500) {               // is it time to toggle red?
    lastRed = now;
    redOn = !redOn;
    digitalWrite(RED_PIN, redOn);
  }
  if (now - lastGreen >= 130) {             // is it time to toggle green?
    lastGreen = now;
    greenOn = !greenOn;
    digitalWrite(GREEN_PIN, greenOn);
  }
  // loop() never blocks, so the CPU is free to do other work here
}
