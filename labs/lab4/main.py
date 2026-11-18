# Lab 4 - Sensor + Display over I2C
# DHT22 data -> GPIO 15, SSD1306 OLED on I2C (SDA = GPIO 21, SCL = GPIO 22),
# alarm LED on GPIO 26 switches on above TEMP_ALARM.
# Needs a second file in the project: ssd1306.py (the OLED driver).
from machine import Pin, SoftI2C
import dht
import ssd1306
import time

TEMP_ALARM = 35.0                       # degrees C
sensor = dht.DHT22(Pin(15))
alarm_led = Pin(26, Pin.OUT)
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
print("I2C devices found:", [hex(a) for a in i2c.scan()])   # expect ['0x3c']
oled = ssd1306.SSD1306_I2C(128, 64, i2c)                    # address 0x3C

while True:
    try:
        sensor.measure()
    except OSError as e:
        print("DHT error:", e)
        time.sleep(2)
        continue
    t = sensor.temperature()
    h = sensor.humidity()
    alarm = t > TEMP_ALARM
    alarm_led.value(alarm)
    print("temp:%.1f hum:%.1f alarm:%d" % (t, h, alarm))

    oled.fill(0)
    oled.text("NAVKIS Weather", 0, 0)
    oled.text("Temp: %.1f C" % t, 0, 20)
    oled.text("Hum : %.0f %%" % h, 0, 34)
    if alarm:
        oled.text("!! HIGH TEMP !!", 0, 54)
    oled.show()
    time.sleep(2)                       # DHT22 can be read at most every 2 s
