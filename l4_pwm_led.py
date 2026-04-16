from time import sleep

import board
import digitalio

# -- Lesson 4 --
#
# we play with pulse-width modulation
# we move sequentially through multiple values
# but we wait a bit to see what happens
#
# the animation takes 5 seconds
# each position is 5 / 100

led = digitalio.DigitalInOut(board.GP15)
led.direction = digitalio.Direction.OUTPUT

steps = 500

duration = 5 / steps
frequency = 400  # Hz

cycle_time = 1 / frequency

for pct in range(1, steps):
    time_on = pct / steps * cycle_time
    time_off = cycle_time - time_on

    # we repeat the on-off
    # for the given duration
    for _ in range(duration / cycle_time):
        led.value = True
        sleep(time_on)
        led.value = False
        sleep(time_off)
