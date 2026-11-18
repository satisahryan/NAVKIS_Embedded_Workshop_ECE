// Lab 3 - The Analog World: ADC in, PWM out
// Potentiometer wiper -> GPIO 34 (ADC1), LED on GPIO 26 dimmed with PWM.
// Open the Serial Plotter style output: each line prints "raw volts duty".

const int POT_PIN = 34;   // ADC1 channel (input-only pin)
const int LED_PIN = 26;

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  analogReadResolution(12);           // 12-bit ADC: 0 ... 4095
}

void loop() {
  int raw = analogRead(POT_PIN);              // 0 ... 4095
  float volts = raw * 3.3 / 4095.0;           // convert to voltage
  int duty = map(raw, 0, 4095, 0, 255);       // scale to 8-bit PWM duty
  analogWrite(LED_PIN, duty);                 // PWM: brightness follows the knob

  Serial.printf("raw:%d volts:%.2f duty:%d\n", raw, volts, duty);
  delay(100);
}
