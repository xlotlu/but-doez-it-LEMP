import board
import neopixel
import time

DELAY = .005

px = neopixel.NeoPixel(board.NEOPIXEL, 1)

while True:
    for i in range(256):
        px.fill((i, i // 4, 0))
        time.sleep(DELAY)

    for i in range(255, -1, -1):
        px.fill((i, i // 4, 0))
        time.sleep(DELAY)

