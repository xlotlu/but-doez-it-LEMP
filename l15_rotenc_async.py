import rotaryio
import asyncio
import time 
from supervisor import ticks_ms

import config

# time-slice-based logic:
# we monitor the delta rotation every time slice
TICK = 40 # the tick used to detect rotenc changes, in ms
SLEEP = TICK // 10 # we async sleep for the 10th part of a tick

_TICKS_PERIOD = const(1<<29)
_TICKS_MAX = const(_TICKS_PERIOD-1)
_TICKS_HALFPERIOD = const(_TICKS_PERIOD//2)

enc = rotaryio.IncrementalEncoder(config.ROTENC_PIN1, config.ROTENC_PIN2)

velocity = 0
def compute(delta):
    global velocity
    velocity = velocity * 0.5 + delta  # decay + input
    return int(velocity * 2)

def ticks_diff(ticks1, ticks2):
    "Compute the signed difference between two ticks values, assuming that they are within 2**28 ticks"
    diff = (ticks1 - ticks2) & _TICKS_MAX
    diff = ((diff + _TICKS_HALFPERIOD) & _TICKS_MAX) - _TICKS_HALFPERIOD
    return diff

async def tick():
    old_time = ticks_ms()
    old_position = enc.position

    system_value = 0

    while True:
        new_time = ticks_ms()
        # if more than TICK time has elapsed,
        # we run a new event (to check for the rotenc value)
        if ticks_diff(new_time, old_time) >= TICK:
            new_position = enc.position

            delta = new_position - old_position
            #print(delta)
            _val = system_value + compute(delta)
            _new_system_value = min(max(0, _val), 255)
            if system_value != _new_system_value:
                system_value = _new_system_value
                print(system_value)

            old_position = new_position
            old_time = new_time
        await asyncio.sleep_ms(SLEEP)


async def main():
    ticker = asyncio.create_task(tick())
    await asyncio.gather(ticker)

asyncio.run(main())
