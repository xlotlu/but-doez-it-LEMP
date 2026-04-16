import asyncio

import board
import digitalio

# -- Lesson 12 --
#
# pulse the LEDs with async

LEDS = [
    (board.GP13, 1),
    (board.GP15, 2),
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
