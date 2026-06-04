import asyncio
from rotaryio import IncrementalEncoder
from supervisor import ticks_ms




# time-slice-based logic:
# we monitor the delta rotation every time slice
TICK = 40 # the tick used to detect rotenc changes, in ms
SLEEP = TICK // 10 # we async sleep for the 10th part of a tick

_TICKS_PERIOD = const(1 << 29)
_TICKS_MAX = const(_TICKS_PERIOD - 1)
_TICKS_HALFPERIOD = const(_TICKS_PERIOD // 2)


def ticks_diff(ticks1, ticks2):
    "Compute the signed difference between two ticks values, assuming that they are within 2**28 ticks"
    diff = (ticks1 - ticks2) & _TICKS_MAX
    diff = ((diff + _TICKS_HALFPERIOD) & _TICKS_MAX) - _TICKS_HALFPERIOD
    return diff


def rgb_color_wheel(x):
    """Color wheel to allow for cycling through the rainbow of RGB colors."""
    x = x % (255 * 3)

    if 0 <= x < 255:
        return (255 - x, x, 0)
    elif 255 <= x < 255 * 2:
        x -= 255
        return (0, 255 - x, x)
    else:
        x -= 255 * 2
        return (x, 0, 255 - x)


class RotaryEncoder:
    def __init__(self, pin1, pin2, callback):
        self._encoder = IncrementalEncoder(pin1, pin2)
        self.velocity = 0
        self.callback = callback

    def compute(self, delta):
        self.velocity = self.velocity * 0.5 + delta  # decay + input
        return round(self.velocity * 2)

    async def monitor(self):
        old_time = ticks_ms()
        old_position = self._encoder.position

        system_value = 0
        # TODO: here we initialise system / print / whatever with current values
        # 
        self.callback(system_value)

        while True:
            # we need to always await, so we do it from the start.
            # this is desirable because it adds the proper pause after system init.
            await asyncio.sleep_ms(SLEEP)

            new_time = ticks_ms()
            # we run a new event only if more than TICK time has elapsed
            if ticks_diff(new_time, old_time) < TICK:
                continue

            # this is a new tick. remember to reset the time!
            old_time = new_time

            new_position = self._encoder.position

            delta = new_position - old_position
            # don't forget to remember the old_position!
            old_position = new_position

            _new_system_value = system_value + self.compute(delta)
            if delta == 0 and system_value == _new_system_value:
                continue

            system_value = _new_system_value

            self.callback(system_value)

# 

import board
import neopixel
import config
px = neopixel.NeoPixel(board.NEOPIXEL, 1)

def payload(value):
    px.fill(rgb_color_wheel(value))

enc = RotaryEncoder(config.ROTENC_PIN1, config.ROTENC_PIN2, payload)

async def main():
    ticker = asyncio.create_task(enc.monitor())
    await asyncio.gather(ticker)

asyncio.run(main())


# v. A:


# v. B:


# important note:
# different lamp modes have different "compute" functions.
# examples:
#   Tetris is linear, and bounded
#   change color brightness: accelerated, bounded
#   change color wheel: accelerated (maybe different algorithm?),
#                       but bounded + wraparound


