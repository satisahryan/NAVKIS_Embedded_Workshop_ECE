# Lab 1 - Try-this solution: two LEDs at two rates WITHOUT sleep()
# Red LED on GPIO 26 toggles every 500 ms, green LED on GPIO 27 every 130 ms.
from machine import Pin
import time

red = Pin(26, Pin.OUT)
green = Pin(27, Pin.OUT)
last_red = last_green = time.ticks_ms()     # time of the last toggle

while True:
    now = time.ticks_ms()                    # ms since the board started
    if time.ticks_diff(now, last_red) >= 500:
        last_red = now
        red.value(not red.value())
    if time.ticks_diff(now, last_green) >= 130:
        last_green = now
        green.value(not green.value())
    # the loop never blocks, so the CPU is free for other work here
