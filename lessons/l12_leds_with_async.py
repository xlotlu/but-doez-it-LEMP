import asyncio

import board
import digitalio
from lib.config import LED1_PIN, LED2_PIN

# -- Lesson 12 --
#
# pulse the LEDs with async

LEDS = [
    (LED2_PIN, 1),
    (LED1_PIN, 2),
    # ...
]


async def pulse_the_led(pin, interval):
    led = digitalio.DigitalInOut(pin)
    led.switch_to_output()

    while True:
        led.value = not led.value
        await asyncio.sleep(interval)


async def main():
    await asyncio.gather(
        *[asyncio.create_task(pulse_the_led(pin, interval)) for pin, interval in LEDS]
    )


asyncio.run(main())
