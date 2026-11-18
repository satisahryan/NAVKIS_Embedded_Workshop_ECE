// Lab 2 - Buttons & Interrupts
// Push-button on GPIO 4 (other leg to GND), LED on GPIO 26.
// Every press toggles the LED and increments a counter - handled by an INTERRUPT.

const int BUTTON_PIN = 4;
const int LED_PIN = 26;

volatile bool pressed = false;        // set inside the ISR, read in loop()
volatile unsigned long lastIsrMs = 0; // for debouncing

// Interrupt Service Routine: keep it SHORT. No Serial.print, no delay here.
void IRAM_ATTR onButton() {
  unsigned long now = millis();
  if (now - lastIsrMs > 200) {        // ignore contact bounce (< 200 ms)
    pressed = true;
    lastIsrMs = now;
  }
}

int count = 0;
bool ledOn = false;

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);  // internal pull-up: idle = HIGH, pressed = LOW
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), onButton, FALLING);
  Serial.println("Lab 2: press the button!");
}

void loop() {
  if (pressed) {                      // the ISR raised the flag
    pressed = false;
    count++;
    ledOn = !ledOn;
    digitalWrite(LED_PIN, ledOn);
    Serial.printf("Press #%d -> LED %s\n", count, ledOn ? "ON" : "OFF");
  }
  // The CPU is free here - e.g. blink something else, read sensors...
}
