# Lab 7 (take-home): deep sleep and battery life
# The ESP32 wakes up, does a little work, then sleeps for 10 s.
# Press the button to wake it early.
import machine, esp32, time
from machine import Pin

led = Pin(26, Pin.OUT)
btn = Pin(4, Pin.IN, Pin.PULL_UP)
rtc = machine.RTC()

# Normal variables live in RAM, which is switched off in deep sleep.
# RTC memory stays powered, so the boot counter survives.
mem = rtc.memory()
boots = int(mem) + 1 if mem else 1
rtc.memory(str(boots))

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    why = {machine.EXT0_WAKE: "button", machine.TIMER_WAKE: "timer"}.get(machine.wake_reason(), "other")
    print("Woke up from deep sleep (", why, ") - boot number", boots)
else:
    print("Power-on boot - boot number", boots)

# The 'work': pretend to read a sensor and send the value (about 0.6 s awake)
for _ in range(3):
    led.on(); time.sleep_ms(100)
    led.off(); time.sleep_ms(100)
print("Work done. Deep sleep for 10 s (or press the button)...")

esp32.wake_on_ext0(pin=btn, level=esp32.WAKEUP_ALL_LOW)   # wake when GPIO 4 goes low
time.sleep_ms(50)                                         # let the message finish printing
machine.deepsleep(10000)                                  # never returns: the chip restarts on wake
