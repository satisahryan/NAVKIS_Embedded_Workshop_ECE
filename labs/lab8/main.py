# Lab 8 (take-home): live Hassan weather from the web, next to your own sensor
# The ESP32 makes an HTTP request, parses the JSON reply, and shows it on the OLED.
import network, time, dht
from machine import Pin, SoftI2C
import ssd1306
try:
    import requests                  # newer MicroPython
except ImportError:
    import urequests as requests     # older MicroPython

LAT, LON = 13.01, 76.10              # Hassan. Try your home town's coordinates!
URL = ("http://api.open-meteo.com/v1/forecast?latitude={}&longitude={}"
       "&current=temperature_2m,relative_humidity_2m,wind_speed_10m").format(LAT, LON)

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
sensor = dht.DHT22(Pin(15))

def show(lines):
    oled.fill(0)
    for i, text in enumerate(lines):
        oled.text(text, 0, i * 10)
    oled.show()

show(["Connecting Wi-Fi"])
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Wokwi-GUEST", "")
while not wlan.isconnected():
    time.sleep_ms(200)
print("Wi-Fi connected, IP", wlan.ifconfig()[0])

def fetch():
    r = requests.get(URL)
    try:
        if r.status_code != 200:
            raise OSError("HTTP " + str(r.status_code))
        now = r.json()["current"]
    finally:
        r.close()                     # always free the socket: RAM is precious
    return now["temperature_2m"], now["relative_humidity_2m"], now["wind_speed_10m"]

while True:
    sensor.measure()
    room = "{:.1f} C {:.0f}%".format(sensor.temperature(), sensor.humidity())
    try:
        t, h, wind = fetch()
        print("Hassan now: {} C, {} %, wind {} km/h | room: {}".format(t, h, wind, room))
        show(["Hassan (web)", "{:.1f} C {:.0f}%".format(t, h), "wind {:.0f} km/h".format(wind), "",
              "Room (DHT22)", room])
    except Exception as e:
        print("Fetch failed:", e)
        show(["Web fetch failed", str(e)[:16], "", "", "Room (DHT22)", room])
    time.sleep(60)                    # be polite to a free service: one request a minute
