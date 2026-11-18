// Mini-challenge - Smart Street Light (reference solution)
const int LDR_PIN = 35;
const int PIR_PIN = 27;
const int LAMP_PIN = 26;
const int DARK_THRESHOLD = 2000;      // calibrate from the printed ldr values
const unsigned long HOLD_MS = 5000;

unsigned long lastMotion = 0;
String lastState = "";

void setup() {
  Serial.begin(115200);
  pinMode(PIR_PIN, INPUT);
  pinMode(LAMP_PIN, OUTPUT);
}

void loop() {
  bool dark = analogRead(LDR_PIN) > DARK_THRESHOLD;
  if (digitalRead(PIR_PIN) == HIGH) lastMotion = millis();
  bool recentMotion = (lastMotion != 0) && (millis() - lastMotion < HOLD_MS);

  String state;
  if (!dark)             { analogWrite(LAMP_PIN, 0);   state = "DAY"; }
  else if (recentMotion) { analogWrite(LAMP_PIN, 255); state = "NIGHT-FULL"; }
  else                   { analogWrite(LAMP_PIN, 50);  state = "NIGHT-DIM"; }

  if (state != lastState) {           // print only on change
    Serial.println(state);
    lastState = state;
  }
  delay(50);
}
