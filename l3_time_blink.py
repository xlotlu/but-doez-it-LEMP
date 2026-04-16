from time import sleep

import board
import digitalio

# -- Lesson 3 --
#
# 1. stable time unit
#    (where time unit = time on + time off)
# 2. we vary the on / off ratio

TIME_UNIT = 1/250 # 25 fps

led = digitalio.DigitalInOut(board.GP15)
led.direction = digitalio.Direction.OUTPUT

for pct in range(1, 100):
    time_on = pct / 100 * TIME_UNIT
    time_off = TIME_UNIT - time_on

    led.value = True
    sleep(time_on)
    led.value = False
    sleep(time_off)
