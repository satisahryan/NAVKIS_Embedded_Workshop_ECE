# Mini-challenge - Smart Street Light (starter)
# Parts already wired: LDR module AO -> GPIO 35, PIR motion sensor OUT -> GPIO 27,
# street-light LED -> GPIO 26.
#
# Rules for your street light:
#   1. Daytime (bright)                -> lamp OFF
#   2. Night, nobody around            -> lamp DIM (about 20 % brightness)
#   3. Night AND motion detected       -> lamp FULL brightness for 5 s after the last motion
# Bonus: print the state ("DAY", "NIGHT-DIM", "NIGHT-FULL") only when it changes.
# Super-bonus: publish the state to MQTT (reuse your Lab 5 code).
from machine import Pin, ADC, PWM
import time

ldr = ADC(Pin(35))
ldr.atten(ADC.ATTN_11DB)
pir = Pin(27, Pin.IN)
lamp = PWM(Pin(26), freq=1000)
print("Smart Street Light - starter")

while True:
    light = ldr.read_u16() >> 4       # higher value = darker (in Wokwi)
    motion = pir.value()              # 1 when motion is detected
    print("ldr:%d motion:%d" % (light, motion))

    # TODO: decide DAY / NIGHT using a threshold you calibrate
    # TODO: use time.ticks_ms() to keep the lamp at full brightness for 5 s after motion
    # TODO: lamp.duty_u16(0 / 13000 / 65535) for OFF / DIM / FULL

    time.sleep_ms(200)
