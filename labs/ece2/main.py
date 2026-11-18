# ECE 2 - Sampling and aliasing
# The PWM hardware makes a square wave on GPIO 26 (the LED shows it).
# A wire carries it to GPIO 35, which the CPU samples at a fixed rate FS.
from machine import Pin, PWM
import time

F_SIGNAL = 50            # Hz, square wave from the PWM hardware
FS = 1000                # samples per second
N = 1000                 # samples to take (1 s at 1 kHz)

src = PWM(Pin(26), freq=F_SIGNAL, duty_u16=32768)    # 50 % duty
inp = Pin(35, Pin.IN)

samples = bytearray(N)
period_us = 1_000_000 // FS
t = time.ticks_us()
for i in range(N):
    while time.ticks_diff(time.ticks_us(), t) < 0:   # wait for the next sample instant
        pass
    samples[i] = inp.value()
    t = time.ticks_add(t, period_us)

rises = sum(1 for i in range(1, N) if samples[i] and not samples[i - 1])
print("Signal %d Hz, sampled at %d Hz for %.2f s" % (F_SIGNAL, FS, N / FS))
print("Rising edges seen: %d -> apparent frequency about %.0f Hz" % (rises, rises * FS / N))
print("First 80 samples:", "".join("#" if s else "_" for s in samples[:80]))
