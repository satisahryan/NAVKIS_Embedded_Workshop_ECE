# Lab 8 extra - REAL ESP32 BOARD ONLY (not the free Wokwi plan):
# serve a web page from the ESP32 and switch the LED from your phone.
# Put your phone and the board on the same Wi-Fi, then open http://<board IP>/
import network, socket, time
from machine import Pin

SSID, PASSWORD = "your-wifi", "your-password"
led = Pin(26, Pin.OUT)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep_ms(200)
ip = wlan.ifconfig()[0]
print("Open http://%s/ on your phone" % ip)

PAGE = """HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE html><html><head>
<meta name="viewport" content="width=device-width,initial-scale=1"><title>ESP32</title></head>
<body style="font-family:sans-serif;text-align:center"><h1>My ESP32</h1><p>LED is <b>{}</b></p>
<p><a href="/on"><button style="font-size:2em">ON</button></a> <a href="/off"><button style="font-size:2em">OFF</button></a></p></body></html>"""

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 80))
s.listen(2)
while True:
    conn, addr = s.accept()
    request = conn.recv(512).decode()
    path = request.split(" ")[1] if " " in request else "/"
    if path == "/on": led.on()
    elif path == "/off": led.off()
    print(addr[0], "asked for", path)
    conn.send(PAGE.format("ON" if led.value() else "OFF"))
    conn.close()
