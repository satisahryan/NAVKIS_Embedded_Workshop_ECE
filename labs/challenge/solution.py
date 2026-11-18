# Mini-challenge - Smart Street Light (reference solution)
from machine import Pin, ADC, PWM
import time

ldr = ADC(Pin(35))
ldr.atten(ADC.ATTN_11DB)
pir = Pin(27, Pin.IN)
lamp = PWM(Pin(26), freq=1000)
DARK_THRESHOLD = 2000        # calibrate from the printed ldr values
HOLD_MS = 5000

last_motion = None
last_state = ""

while True:
    dark = (ldr.read_u16() >> 4) > DARK_THRESHOLD
    if pir.value():
        last_motion = time.ticks_ms()
    recent = last_motion is not None and time.ticks_diff(time.ticks_ms(), last_motion) < HOLD_MS

    if not dark:
        lamp.duty_u16(0); state = "DAY"
    elif recent:
        lamp.duty_u16(65535); state = "NIGHT-FULL"
    else:
        lamp.duty_u16(13000); state = "NIGHT-DIM"

    if state != last_state:          # print only on change
        print(state)
        last_state = state
    time.sleep_ms(50)
