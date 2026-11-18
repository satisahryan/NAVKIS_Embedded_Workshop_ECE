# Lab 1 - Hello, GPIO!  (MicroPython on ESP32, Wokwi)
# An LED on GPIO 26 (through a 220 ohm resistor) blinks once a second.
from machine import Pin
import time

led = Pin(26, Pin.OUT)          # GPIO 26 as an OUTPUT
print("Lab 1: Hello, GPIO!")

while True:
    led.value(1)                # 3.3 V on the pin -> LED ON
    print("LED ON")
    time.sleep_ms(500)          # wait 500 ms (the CPU does nothing else!)
    led.value(0)                # 0 V on the pin -> LED OFF
    print("LED OFF")
    time.sleep_ms(500)
