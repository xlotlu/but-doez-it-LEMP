import asyncio
from rotaryio import IncrementalEncoder
from supervisor import ticks_ms

from utils import ticks_diff
from colors import rgb_color_wheel


# time-slice-based logic:
# we monitor the delta rotation every time slice
TICK = 40 # the tick used to detect rotenc changes, in ms
SLEEP = TICK // 10 # we async sleep for the 10th part of a tick


# important note:
# different lamp modes have different "compute" functions.
# examples:
#   Tetris is linear, and bounded (has min and max)
#   change color brightness: accelerated, bounded
#   change color wheel: accelerated (maybe different algorithm?),
#                       but bounded + wraparound

# Terms dictionary
# ================
#
# linear:
#       rotation speed is not taken into consideration
#
# accelerated:
#       faster rotation speed causes greater transition
#
# bounded:
#       it has a maximum and minimum value which it cannot surpass
#
# unbounded:
#       it has no minimum / maximum values. goes on forever.
#
# wraparound:
#       makes sense only in bounded mode:
#       when reaching the maximum value, the next value will be the minimum
#       and the other way around (passing minimum leads to maximum)
#


class RotaryEncoder:
    def __init__(self, pin_a, pin_b, divisor=4, value=0, callback=None):
        self._encoder = IncrementalEncoder(pin_a, pin_b, divisor=divisor)

        self.value = value # the initial value
        if callback is None:
            # we set the callback to a no-op function to simplify the code
            self.callback = lambda v: None
        else:
            self.callback = callback

    def process_delta(self, delta):
        return delta

    def process_value(self, value):
        return value

    async def monitor(self):
        old_time = ticks_ms()
        old_position = self._encoder.position

        system_value = self.value
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

            _new_system_value = system_value + self.process_delta(delta)
            if delta == 0 and system_value == _new_system_value:
                continue

            system_value = self.process_value(_new_system_value)

            self.value = system_value

            self.callback(system_value)


class BoundedRotaryEncoder(RotaryEncoder):
    def __init__(self, pin_a, pin_b, min, max, **kwargs):
        super().__init__(pin_a, pin_b, **kwargs)

        self.min = min
        self.max = max

    def process_value(self, value):
        if value < self.min:
            # TODO: emit event: lower bound was hit
            value = self.min

        elif value > self.max:
            # TODO: emit event: upper bound was hit
            value = self.max

        return value


class WraparoundRotaryEncoder(BoundedRotaryEncoder):
    def process_value(self, value):
        if value < self.min:
            overflow = self.min - value
            value = self.max - overflow 

        elif value > self.max:
            overflow = value - self.max
            value = self.min + overflow

        return value


class _AcceleratedRotaryMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocity = 0

    def process_delta(self, delta):
        self.velocity = self.velocity * 0.5 + delta  # decay + input
        return round(self.velocity * 2)


class AcceleratedRotaryEncoder(RotaryEncoder, _AcceleratedRotaryMixin):
    pass

class AcceleratedBoundedRotaryEncoder(BoundedRotaryEncoder, _AcceleratedRotaryMixin):
    pass

class AcceleratedWraparoundRotaryEncoder(WraparoundRotaryEncoder, _AcceleratedRotaryMixin):
    pass


# 

import board
import neopixel
import config
px = neopixel.NeoPixel(board.NEOPIXEL, 1)

def payload(value):
    #px.fill(rgb_color_wheel(value))
    print(f"\r{value:>4}", end="")

#enc = RotaryEncoder(config.ROTENC_PIN1, config.ROTENC_PIN2, callback=payload)
#enc = AcceleratedRotaryEncoder(config.ROTENC_PIN1, config.ROTENC_PIN2, callback=payload)
#enc = BoundedRotaryEncoder(config.ROTENC_PIN1, config.ROTENC_PIN2, 0, 42, callback=payload)
#enc = WraparoundRotaryEncoder(config.ROTENC_PIN1, config.ROTENC_PIN2, 0, 42, callback=payload)
#enc = AcceleratedBoundedRotaryEncoder(config.ROTENC_PIN1, config.ROTENC_PIN2, 0, 255, callback=payload)
enc = AcceleratedWraparoundRotaryEncoder(config.ROTENC_PIN1, config.ROTENC_PIN2, 0, 255, callback=payload)


async def main():
    ticker = asyncio.create_task(enc.monitor())
    await asyncio.gather(ticker)

if __name__ == "__main__":
    asyncio.run(main())
