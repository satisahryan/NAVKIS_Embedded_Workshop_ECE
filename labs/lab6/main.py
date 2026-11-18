# Lab 6 (Deep dive) - Cooperative multitasking with asyncio
# Three independent tasks share one CPU, like tasks in a real-time OS:
#   blink_task  - toggles the LED on GPIO 26 every 250 ms
#   sensor_task - reads the potentiometer (GPIO 34) and puts values in a FIFO
#   print_task  - waits until data arrives, then prints it
# Potentiometer wiper -> GPIO 34, LED -> GPIO 26 (same wiring as Lab 3).
import asyncio
from machine import Pin, ADC

led = Pin(26, Pin.OUT)
pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)

fifo = []                      # a simple queue between producer and consumer
data_ready = asyncio.Event()   # lets print_task sleep until there is data

async def blink_task():
    while True:
        led.value(not led.value())
        await asyncio.sleep_ms(250)    # give the CPU to the other tasks

async def sensor_task():               # producer
    while True:
        if len(fifo) < 10:             # drop the sample if the queue is full
            fifo.append(pot.read_u16() >> 4)
            data_ready.set()
        await asyncio.sleep_ms(500)

async def print_task():                # consumer
    while True:
        await data_ready.wait()        # block until the producer signals
        data_ready.clear()
        while fifo:
            print("pot =", fifo.pop(0))

async def main():
    asyncio.create_task(blink_task())
    asyncio.create_task(sensor_task())
    asyncio.create_task(print_task())
    while True:                        # main() is just another task
        await asyncio.sleep(1)

asyncio.run(main())
