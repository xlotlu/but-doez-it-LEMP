from time import sleep

import board
import digitalio

# -- Lesson 2 --
#
# the LED blinks faster and faster

led = digitalio.DigitalInOut(board.GP15)
led.direction = digitalio.Direction.OUTPUT

for x in range(2, 100):
    s = 1 / x
    for _ in range(10):
        led.value = True
        sleep(s)
        led.value = False
        sleep(s)
