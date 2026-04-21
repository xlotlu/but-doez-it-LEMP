from time import sleep

import board
import digitalio
from lib.config import LED1_PIN

# -- Lesson 1 --
#
# make an LED blink

# these are "constants"
TIME_ON = 0.04
TIME_OFF = 0.01

TIMES = 50

led = digitalio.DigitalInOut(LED1_PIN)
led.direction = digitalio.Direction.OUTPUT

# we make the led blink 'TIMES'
for _ in range(TIMES):
    led.value = True
    sleep(TIME_ON)
    led.value = False
    sleep(TIME_OFF)
