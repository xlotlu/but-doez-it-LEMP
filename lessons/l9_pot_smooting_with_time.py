import time
from collections import deque

import analogio
import board
from lib.config import ADC_PIN


# -- Lesson 9 --
#
# obtain the median value of the potentiometer
# over a period of time
# Quippy genius stuff

potentiometer = analogio.AnalogIn(ADC_PIN)

WINDOW_DURATION = 0.2 # seconds
THRESHOLD = 10


def avg(list: list):
    return int(sum(list) / len(list))

potentiometer = analogio.AnalogIn(ADC_PIN)

old_avg = 0
values = []
while True:
    values.clear()

    # 1. collect value in an interval
    start_time = time.monotonic()
    while time.monotonic() - start_time < WINDOW_DURATION:
        # f*cking blocking like hell
        pot = potentiometer.value
        values.append(pot)
    
    # 2. calculate the average
    current_avg = avg(values)
    if abs(current_avg - old_avg) > THRESHOLD:
        print(len(values), ': ', current_avg)
        old_avg = current_avg
