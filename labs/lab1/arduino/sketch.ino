// Lab 1 - Hello, GPIO!  (ESP32 DevKitC V4 in Wokwi)
// An LED on GPIO 26 (through a 220 ohm resistor) blinks once a second.

const int LED_PIN = 26;        // the GPIO pin our LED is wired to

void setup() {
  Serial.begin(115200);        // open the serial monitor (115200 baud)
  pinMode(LED_PIN, OUTPUT);    // configure GPIO 26 as an OUTPUT
  Serial.println("Lab 1: Hello, GPIO!");
}

void loop() {
  digitalWrite(LED_PIN, HIGH); // 3.3 V on the pin -> LED ON
  Serial.println("LED ON");
  delay(500);                  // wait 500 ms (the CPU does nothing else!)

  digitalWrite(LED_PIN, LOW);  // 0 V on the pin -> LED OFF
  Serial.println("LED OFF");
  delay(500);
}
