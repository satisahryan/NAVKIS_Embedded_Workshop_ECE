// Mini-challenge - Smart Street Light (starter)
// Parts already wired: LDR module AO -> GPIO 35, PIR motion sensor OUT -> GPIO 27,
// street-light LED -> GPIO 26.
//
// Rules for your street light:
//   1. Daytime (bright)                -> lamp OFF
//   2. Night, nobody around            -> lamp DIM (about 20 % brightness)
//   3. Night AND motion detected       -> lamp FULL brightness for 5 s after the last motion
// Bonus: print the state changes ("DAY", "NIGHT-DIM", "NIGHT-FULL") only when they change.
// Super-bonus: publish the state to MQTT (reuse your Lab 5 code).

const int LDR_PIN = 35;
const int PIR_PIN = 27;
const int LAMP_PIN = 26;

void setup() {
  Serial.begin(115200);
  pinMode(PIR_PIN, INPUT);
  pinMode(LAMP_PIN, OUTPUT);
  Serial.println("Smart Street Light - starter");
}

void loop() {
  int light = analogRead(LDR_PIN);     // higher value = darker (in Wokwi)
  int motion = digitalRead(PIR_PIN);   // HIGH when motion is detected

  Serial.printf("ldr:%d motion:%d\n", light, motion);

  // TODO: decide DAY / NIGHT using a threshold you calibrate
  // TODO: use millis() to keep the lamp at full brightness for 5 s after motion
  // TODO: analogWrite(LAMP_PIN, 0 / 50 / 255) for OFF / DIM / FULL

  delay(200);
}
