import asyncio

from rotaryio import IncrementalEncoder
from supervisor import ticks_ms

from utils import ticks_diff


# time-slice-based logic:
# we monitor the delta rotation every time slice
TICK = 40 # the tick used to detect rotenc changes, in ms
SLEEP = TICK // 10 # we async sleep for the 10th part of a tick


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

    async def wait(self):
        self.old_time = ticks_ms()
        self._old_encoder_position = self._encoder.position

        while True:
            if False: # value changed
                return value

            await asyncio.sleep_ms(SLEEP)

    async def monitor(self):
        old_time = ticks_ms()
        _old_encoder_position = self._encoder.position

        # TODO: here we initialise system / print / whatever with current values
        #
        self.callback(self.value)

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

            _encoder_position = self._encoder.position

            delta = _encoder_position - _old_encoder_position
            # don't forget to remember the encoder's old position!
            _old_encoder_position = _encoder_position

            _new_system_value = self.value + self.process_delta(delta)
            if delta == 0 and self.value == _new_system_value:
                continue

            self.value = self.process_value(_new_system_value)

            self.callback(self.value)


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
