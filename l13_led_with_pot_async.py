import asyncio
from collections import deque

import analogio
import board
import pwmio

# -- Lesson 13 --
#
# pot controlls led's pwm
# with async

WINDOW_SAMPLES = 30
NOISE_THRESHOLD_MULTIPLIER = 2.5 / 100
MIN_THRESHOLD = 65  # ~0.1% of 65535
PROGRESSBAR_WIDTH = 100


potentiometer = analogio.AnalogIn(board.GP26)
led = pwmio.PWMOut(board.GP15, frequency=1000)


def print_progress(value):
    percentage = value * 100 / 65535
    display_percentage = round(percentage / 100 * PROGRESSBAR_WIDTH)
    leftover_percentage = 100 - display_percentage
    print(
        f"\rProgress: {percentage:>6.2f}% [{'#' * display_percentage}{'-' * leftover_percentage}]",
        end="",
    )


def compute_variability(value):
    """
    this computes the allowed maximum variability for a given value.
    """
    # it should normally be value * NOISE_THRESHOLD_MULTIPLIER,
    # but 1) we account for a minimum
    # and 2) we multiply by WINDOW_SAMPLES
    #        because we compare with the full deque sum
    return WINDOW_SAMPLES * max(MIN_THRESHOLD, value * NOISE_THRESHOLD_MULTIPLIER)


async def monitor_pot(callback):
    ### start init

    # we use the current potentiometer value to initialize:
    # - the deque
    values = deque([potentiometer.value] * WINDOW_SAMPLES, WINDOW_SAMPLES)
    # - the last and current sum
    #   (which we will maintain manually for optimization)
    last_sum = current_sum = sum(values)
    # - and the current variability
    variability = compute_variability(potentiometer.value)

    ### end init

    # run the callback once so the entire system gets initialized
    callback(potentiometer.value)

    while True:
        value = potentiometer.value
        # we maintain the deque manually because micro-optimisations
        oldest_val = values.popleft()
        values.append(value)

        current_sum = current_sum - oldest_val + value

        if abs(last_sum - current_sum) > variability:
            callback(round(current_sum / WINDOW_SAMPLES))

            # the maximum variability depends on the current value
            variability = compute_variability(value)
            last_sum = current_sum

        await asyncio.sleep(
            0.05
        )  # (≈50Hz) value chosen by much debate and random dice throw.


def handle_pot_changes(value):
    led.duty_cycle = value
    print_progress(value)


async def main():
    pot_monitor = asyncio.create_task(monitor_pot(handle_pot_changes))
    await asyncio.gather(pot_monitor)


asyncio.run(main())

)

