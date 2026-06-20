import rotaryio
import asyncio
import time 
from supervisor import ticks_ms
import neopixel
import board
import pwmio

import config

# time-slice-based logic:
# we monitor the delta rotation every time slice
TICK = 40 # the tick used to detect rotenc changes, in ms
SLEEP = TICK // 10 # we async sleep for the 10th part of a tick

_TICKS_PERIOD = const(1 << 29)
_TICKS_MAX = const(_TICKS_PERIOD - 1)
_TICKS_HALFPERIOD = const(_TICKS_PERIOD // 2)

VISUALIZER_WIDTH= 10
VISUALIZER_SYMBOL = "="

enc = rotaryio.IncrementalEncoder(config.ROTENC_PIN1, config.ROTENC_PIN2)
px = neopixel.NeoPixel(board.NEOPIXEL, 1)
led = pwmio.PWMOut(board.IO42, frequency=1000)


velocity = 0
def compute(delta):
    global velocity
    velocity = velocity * 0.5 + delta  # decay + input
    return round(velocity)

def get_current_multiplier(value):
    return round(value * 19 / 255) + 1

def visualize(delta, length=VISUALIZER_WIDTH, symbol=VISUALIZER_SYMBOL):
    """ 
    Offers a nice way to VISUALIZE the current delta
    Example: ==|
               |=
    'width' is half of the total to avoid an extra division
    it adds 1 to the 'width' for the | (pipe)
    """
    first_half = second_half = " " * VISUALIZER_WIDTH
    gap = VISUALIZER_WIDTH - abs(delta)

    if delta < 0:
        first_half = " " * gap + VISUALIZER_SYMBOL * -delta
    elif delta > 0:
        second_half = VISUALIZER_SYMBOL * delta + " " * gap 

    line = f"| {first_half}|{second_half} | "
    return line

def ticks_diff(ticks1, ticks2):
    "Compute the signed difference between two ticks values, assuming that they are within 2**28 ticks"
    diff = (ticks1 - ticks2) & _TICKS_MAX
    diff = ((diff + _TICKS_HALFPERIOD) & _TICKS_MAX) - _TICKS_HALFPERIOD
    return diff

async def tick():
    old_time = ticks_ms()
    old_position = enc.position

    system_value = 0
    # TODO: here we initialise system / print / whatever with current values
    print(visualize(0))

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
        
        new_position = enc.position

        delta = new_position - old_position
        # don't forget to remember the old_position!
        old_position = new_position

        _val = system_value + compute(delta) * get_current_multiplier(system_value)
        _new_system_value = min(max(0, _val), 255)
        if delta == 0 and system_value == _new_system_value:
            continue

        system_value = _new_system_value

        print(visualize(delta), system_value)
        px.fill((system_value, system_value // 4, system_value // 2))
        #led.duty_cycle = 2 ** (system_value // 16)
        

async def main():
    ticker = asyncio.create_task(tick())
    await asyncio.gather(ticker) 

asyncio.run(main())
