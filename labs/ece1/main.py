# ECE 1 - See the bits: UART frames on a logic analyzer
# UART1 transmits on GPIO 17. A wire loops it back to UART2's receiver on GPIO 16.
# Logic analyzer channel D0 watches the TX line.
from machine import UART
import time

BAUD_TX = 9600
BAUD_RX = 9600           # try 4800 or 19200: what arrives when the two ends disagree?

tx = UART(1, baudrate=BAUD_TX, tx=17, rx=18)
rx = UART(2, baudrate=BAUD_RX, tx=19, rx=16)

msg = b"UA"              # 'U' = 0x55 = 0101 0101, a clean clock pattern; 'A' = 0x41
for i in range(5):
    tx.write(msg)
    time.sleep_ms(50)    # give the bytes time to arrive
    print("sent", msg, "received", rx.read())
    time.sleep_ms(500)
print("Done. Stop the simulation to download the waveform (wokwi-logic.vcd).")
