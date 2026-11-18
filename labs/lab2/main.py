# Lab 2 - Buttons & Interrupts
# Push-button on GPIO 4 (other leg to GND), LED on GPIO 26.
# Every press toggles the LED and increments a counter - handled by an INTERRUPT.
from machine import Pin
import time

led = Pin(26, Pin.OUT)
button = Pin(4, Pin.IN, Pin.PULL_UP)   # internal pull-up: idle = 1, pressed = 0

pressed = False        # set inside the handler, read in the main loop
last_irq = 0           # for debouncing

def on_button(pin):
    # Interrupt handler: keep it SHORT. No print(), no sleep() here.
    global pressed, last_irq
    now = time.ticks_ms()
    if time.ticks_diff(now, last_irq) > 200:   # ignore contact bounce
        pressed = True
        last_irq = now

button.irq(trigger=Pin.IRQ_FALLING, handler=on_button)
print("Lab 2: press the button!")

count = 0
while True:
    if pressed:                 # the handler raised the flag
        pressed = False
        count += 1
        led.value(not led.value())
        print("Press #%d -> LED %s" % (count, "ON" if led.value() else "OFF"))
    time.sleep_ms(10)           # the CPU is free here for other work
