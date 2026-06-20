from collections import deque

import analogio
import board
from lib.config import ADC_PIN

potentiometer = analogio.AnalogIn(ADC_PIN)

# -- Lesson 8 --
#
# Task:
# output the potentiometer's value only when it changes
# (outside a reasonable limit)
#
# How do we do that?
# 1. how do we detect the change?
# 2. what does 'reasonable' mean?

# Version 1
# we change the value when its outside
# the variability
#
# we use the window variability
# to avoid multiple divisions

VARIABILITY = 20

# SAMPLING_RATE
WINDOW_SAMPLES = 20
WINDOW_VARIABILITY = VARIABILITY * WINDOW_SAMPLES

# we instantiate the deque fully filled with the current value
values = deque([potentiometer.value] * WINDOW_SAMPLES, WINDOW_SAMPLES)

old_sum = sum(values)
while True:
    value = potentiometer.value
    values.append(value)
    new_sum = sum(values)
    # do we have enough variance?
    if abs(new_sum - old_sum) > WINDOW_VARIABILITY:
        print(sum(values) / len(values))
        old_sum = new_sum


# Version 2
# we calculate the variability dynamically

old_sum = sum(values)
while True:
    value = potentiometer.value
    values.append(value)

    new_sum = sum(values)
    maximum_variability = WINDOW_VARIABILITY + (value // 40)

    # do we have enough variance?
    if abs(new_sum - old_sum) > maximum_variability:
        print(sum(values) // len(values))
        old_sum = new_sum
