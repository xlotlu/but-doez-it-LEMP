from time import sleep

import board
import digitalio
from lib.config import LED1_PIN, LED2_PIN

# -- Lesson 11 --
#
# 2 leds that blink
# at different intervals
#
# we have count downs for the leds
# when they reach 0, the led toggles

TICK = 1

# stores the pin and interval (seconds) for each LED
LEDS = [
    (LED2_PIN, 1),
    (LED1_PIN, 2),
    # ...
]

# holds the initialized LEDs
leds = [
    # LED 1
    # LED 2
    # LED 3
    # ...
]

count_downs = [
    # countdown for LED 1
    # countdown for LED 2
    # ...
]

# create the LED
for pin, cd in LEDS:
    led = digitalio.DigitalInOut(pin)
    led.switch_to_output()
    leds.append(led)

    count_downs.append(cd)

while True:
    for i, led in enumerate(leds):
        count_downs[i] -= TICK

        if count_downs[i] <= 0:
            # toggle the LED
            led.value = not led.value
            # reset the countdown
            count_downs[i] = LEDS[i][1]

    sleep(TICK)
