# Lab 3 - Try-this solution: automatic night lamp
# LDR module AO -> GPIO 35. In Wokwi the AO value RISES when it gets darker.
from machine import Pin, ADC
import time

ldr = ADC(Pin(35))
ldr.atten(ADC.ATTN_11DB)
lamp = Pin(26, Pin.OUT)
DARK_THRESHOLD = 2000        # calibrate: watch the printed values, then choose

while True:
    light = ldr.read_u16() >> 4
    dark = light > DARK_THRESHOLD
    lamp.value(dark)
    print("ldr:%d lamp:%s" % (light, "ON" if dark else "OFF"))
    time.sleep_ms(200)
