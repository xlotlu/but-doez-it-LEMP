from time import sleep

import board
import digitalio
from lib.config import LED1_PIN

# -- Lesson 2 --
#
# the LED blinks faster and faster

led = digitalio.DigitalInOut(LED1_PIN)
led.direction = digitalio.Direction.OUTPUT

for x in range(2, 100):
    s = 1 / x
    for _ in range(10):
        led.value = True
        sleep(s)
        led.value = False
        sleep(s)
