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


# TODO: should the compute function work on system_value or on delta?
#       it must do different things depending on bounded / accelerated / wraparound


class RotaryEncoder:
    def __init__(self, pin1, pin2, callback, accelerated=False, limits=(None, None), wraparound=False):
        min, max = limits

        if (min is None and max is not None) or (max is None and min is not None):
            # this is an error, both bounds are necessary
            raise ValueError("A bounded rotary encoder must specify both bounds!")

        self.bounded = min is not None and max is not None

        self.min = min
        self.max = max

        if wraparound and not self.bounded:
            raise ValueError("An unbounded rotary encoder cannot wrap around!")

        self.wraparound = wraparound

        self.accelerated = accelerated

        self._encoder = IncrementalEncoder(pin1, pin2)
        self.velocity = 0
        self.callback = callback

    def compute(self, delta):
        self.velocity = self.velocity * 0.5 + delta  # decay + input
        return round(self.velocity * 2)


    # sună logic să punem accelerated în altă funcție?
    # D A


    def mk_the_value(self, new_value):
        if self.wraparound:
            # wraparound mode means we're bounded to min and max
            if new_value < self.min:
                overflow = self.min - new_value
                new_value = self.max - overflow 

            elif new_value > self.max:
                overflow = new_value - self.max
                new_value = self.min + overflow

        elif self.bounded:
            if new_value < self.min:
                # TODO: emit event: lower bound was hit
                new_value = self.min

            elif new_value > self.max:
                # TODO: emit event: upper bound was hit
                new_value = self.max

        # else: this is unbounded. nothing to do.

        return new_value



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

            system_value = self.mk_the_value(_new_system_value)

            self.callback(system_value)


# new and different approach:

class RotaryEncoder:
    def __init__(self, pin1, pin2, divisor=4, value=0, callback=None):
        self._encoder = IncrementalEncoder(pin1, pin2, divisor=divisor)

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


# class BoundedRotaryEncoder(RotaryEncoder):
#     def __init__(self, pin1, pin2, callback, min, max):
#         pass

# class WraparoundRotaryEncoder(BoundedRotaryEncoder):
#     def __init__(self, pin1, pin2, callback, min, max):
#         pass

# class AcceleratedRotaryEncoder(RotaryEncoder):
#     pass

# AcceleratedBoundedRotaryEncoder

# AcceleratedWraparoundRotaryEncoder


# 

import board
import neopixel
import config
px = neopixel.NeoPixel(board.NEOPIXEL, 1)

def payload(value):
    #px.fill(rgb_color_wheel(value))
    print(f"\r{value:>4}", end="")

enc = RotaryEncoder(config.ROTENC_PIN1, config.ROTENC_PIN2, callback=payload)

async def main():
    ticker = asyncio.create_task(enc.monitor())
    await asyncio.gather(ticker)

asyncio.run(main())
