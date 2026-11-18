# Lab 3 - The Analog World: ADC in, PWM out
# Potentiometer wiper -> GPIO 34 (ADC), LED on GPIO 26 dimmed with PWM.
from machine import Pin, ADC, PWM
import time

pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)             # full 0 ... 3.3 V input range
led = PWM(Pin(26), freq=1000)        # 1 kHz PWM on the LED

while True:
    raw = pot.read_u16() >> 4        # 16-bit reading -> 12-bit: 0 ... 4095
    volts = raw * 3.3 / 4095
    duty = raw * 255 // 4095         # scale to 8-bit duty: 0 ... 255
    led.duty_u16(duty * 257)         # 0..255 -> 0..65535
    print("raw:%d volts:%.2f duty:%d" % (raw, volts, duty))
    time.sleep_ms(100)
