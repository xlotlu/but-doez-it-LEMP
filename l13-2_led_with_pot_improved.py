import asyncio

import analogio
import board
import pwmio

# -- Lesson 13 --
#  - Version 2 -
#
# pot controls LED's pwm
# with async - improved version
#
# This version uses EMA (Exponential Moving Average) for smoothing.
# It's faster and uses less memory than the previous "window" approach.

potentiometer = analogio.AnalogIn(board.GP26)
led = pwmio.PWMOut(board.GP15, frequency=1000)


def create_smoothing_func(shift=2, initial=0):
    """
    Creates a 'smart' smoothing function that remembers past values.

    This uses EMA (Exponential Moving Average).
    It just keeps one 'average' that updates over time.

    initial: Starting value of the sensor
    shift: How much 'smoothing' to apply (higher = smoother but slower)
    """
    # 'state' is our memory. We scale it up (<< shift) to keep
    # precision without using floating point numbers (which are slow).
    state = initial << shift

    def smoothen(raw_value):
        """
        The actual math to clean up the signal:
        - Removes 'jitter' (shaking numbers)
        - Damps down sudden spikes
        """
        nonlocal state

        # We update the average:
        # 1. Take away a small part of the old average (state >> 2)
        # 2. Add the new raw value
        # This is basically: average = (average * 0.75) + new_value
        state = state - (state >> 2) + raw_value

        # Scale it back down to the normal range before returning
        return state >> shift

    return smoothen


def print_progress(value):
    """Draws a progress bar in the console."""
    percentage = value * 100 / 65535
    bar_count = round(percentage)

    print(f"\r{percentage:.1f}% [{'#' * bar_count:-<100}]", end=" ")


async def monitor_pot(callback):
    """Asynchronously watches the potentiometer for changes."""
    # We work with 12-bit precision (>> 4) to reduce initial noise
    initial_val = potentiometer.value >> 4

    # Initialize our smoothing 'memory'
    smoothen = create_smoothing_func(initial=initial_val)

    callback(initial_val)

    old_pot = smoothen(initial_val)
    while True:
        raw_pot = potentiometer.value >> 4
        clean_pot = smoothen(raw_pot)

        # Only trigger the callback if the change is significant (~2%)
        if (abs(clean_pot - old_pot)) > 82:
            # Reconstruct the 16-bit value for the PWM duty_cycle
            callback((clean_pot << 4) | (clean_pot >> 8))
            old_pot = clean_pot

        await asyncio.sleep(0)


def handle_pot_changes(value):
    """This runs whenever the pot moves enough."""
    led.duty_cycle = value
    print_progress(value)


async def main():
    pot_monitor = asyncio.create_task(monitor_pot(handle_pot_changes))

    await asyncio.gather(pot_monitor)


asyncio.run(main())
