# Lab 5 - Your ESP32 on the Internet (MQTT)
# DHT22 -> GPIO 15, LED -> GPIO 26. Joins Wokwi's virtual Wi-Fi, publishes
# readings every 5 s, and listens for ON/OFF commands from the class dashboard.
import network
import time
import dht
import machine
from machine import Pin
from umqtt.simple import MQTTClient

# ======= CHANGE THIS: your name or USN (letters/numbers only, no spaces) =======
STUDENT = "your-name"
# ===============================================================================

# Free public brokers, tried in order (the class dashboard listens to all of them)
BROKERS = ["broker.hivemq.com", "broker.emqx.io", "test.mosquitto.org"]
TOPIC_ROOT = "navkis/ews2026"          # must match the dashboard

sensor = dht.DHT22(Pin(15))
led = Pin(26, Pin.OUT)
data_topic = "%s/%s/data" % (TOPIC_ROOT, STUDENT)
led_topic = "%s/%s/led" % (TOPIC_ROOT, STUDENT)

print("Connecting to Wi-Fi", end="")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Wokwi-GUEST", "")        # open network
while not wlan.isconnected():
    print(".", end="")
    time.sleep(0.1)
print(" connected! IP =", wlan.ifconfig()[0])

def on_message(topic, msg):            # runs when a subscribed message arrives
    print("Message on", topic.decode(), ":", msg.decode())
    if msg == b"ON":
        led.value(1)
    elif msg == b"OFF":
        led.value(0)

client_id = "navkis-%s-%d" % (STUDENT, machine.unique_id()[-1])
client = None
for broker in BROKERS:                 # use the first broker that answers
    try:
        print("Connecting to MQTT broker", broker, "...", end="")
        c = MQTTClient(client_id, broker, keepalive=60)
        c.set_callback(on_message)
        c.connect()
        client = c
        break
    except Exception as e:
        print(" failed:", e)
if client is None:
    raise SystemExit("No MQTT broker reachable - tell the instructor")
client.subscribe(led_topic)
print(" connected! Listening on", led_topic)

last_send = time.ticks_ms() - 5000
while True:
    client.check_msg()                 # handle incoming messages (non-blocking)
    if time.ticks_diff(time.ticks_ms(), last_send) >= 5000:   # every 5 seconds
        last_send = time.ticks_ms()
        try:
            sensor.measure()
            msg = '{"t":%.1f,"h":%.1f,"led":%d}' % (sensor.temperature(), sensor.humidity(), led.value())
            client.publish(data_topic, msg)
            print("Published to", data_topic, ":", msg)
        except OSError as e:
            print("Sensor error:", e)
    time.sleep_ms(50)
