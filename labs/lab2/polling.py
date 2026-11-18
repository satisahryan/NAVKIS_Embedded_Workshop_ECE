# Lab 2 - Polling version (for comparison). Same wiring as the interrupt version.
from machine import Pin
import time

led = Pin(26, Pin.OUT)
button = Pin(4, Pin.IN, Pin.PULL_UP)

while True:
    led.value(button.value() == 0)   # ask the pin again and again: LED on while held
    time.sleep_ms(10)
