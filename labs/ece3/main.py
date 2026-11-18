# ECE 3 - Digital filters: moving average (FIR) vs exponential (IIR)
# The potentiometer on GPIO 34 gives a clean signal. We add noise in software,
# then compare two classic filters from your DSP course.
from machine import Pin, ADC
import time, random

adc = ADC(Pin(34))
adc.atten(ADC.ATTN_11DB)

NOISE = 300              # +/- ADC counts of added noise (try 0, 100, 600)
M = 8                    # moving-average length = number of FIR taps
ALPHA = 0.2              # IIR smoothing factor, 0 < ALPHA <= 1

buf = [0] * M
idx = 0
iir = None
while True:
    clean = adc.read_u16() >> 4                          # 0 ... 4095
    x = clean + random.randint(-NOISE, NOISE)            # noisy sample x[n]
    buf[idx] = x
    idx = (idx + 1) % M
    fir = sum(buf) // M                                  # y[n] = (x[n] + ... + x[n-M+1]) / M
    iir = x if iir is None else iir + ALPHA * (x - iir)  # y[n] = y[n-1] + a(x[n] - y[n-1])
    print("clean:%4d noisy:%4d FIR:%4d IIR:%4d" % (clean, x, fir, int(iir)))
    time.sleep_ms(50)                                    # 20 samples per second
