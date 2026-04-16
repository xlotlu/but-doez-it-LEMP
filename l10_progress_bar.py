import time
from collections import deque

import analogio
import board
import pwmio

# -- Lesson 10 --
#
# make a progress bar
# for the pot

WINDOW_SAMPLES = 30
NOISE_THRESHOLD_PERCENTAGE = 2.5
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


initial_val = potentiometer.value
values = deque([initial_val] * WINDOW_SAMPLES, WINDOW_SAMPLES)

# we need to maintain these variables manually,
# to verify if the current value has "really" changed
last_sum = current_sum = sum(values)
maximum_variability = WINDOW_SAMPLES * initial_val * NOISE_THRESHOLD_PERCENTAGE / 100

# initialize the display with the current value
print_progress(initial_val)

while True:
    value = potentiometer.value
    # we maintain the deque manually because micro-optimisations
    oldest_val = values.popleft()
    values.append(value)

    current_sum = current_sum - oldest_val + value

    if abs(last_sum - current_sum) > maximum_variability:
        the_value = current_sum / WINDOW_SAMPLES

        # payload(s)
        print_progress(the_value)
        led.duty_cycle = round(the_value)

        # the maximum variability depends on the current value
        maximum_variability = WINDOW_SAMPLES * (
            value * NOISE_THRESHOLD_PERCENTAGE / 100
        )
        last_sum = current_sum
rrent_sum
