from time import sleep

import board
import pwmio

# -- Lesson 5 --
#
# PWM!
# (= pulse-width modulation)
# with lib

# Example 1
led1 = pwmio.PWMOut(board.LED, frequency=1000)

# duty cycle == how much out of 2 ** 16
led1.duty_cycle = 2**15
sleep(3)
led1.duty_cycle = 2**12
sleep(3)
led1.duty_cycle = 2**4
sleep(3)
led1.duty_cycle = 2
sleep(3)


# Example 2
# LED 0-100% power cycle

led2 = pwmio.PWMOut(board.GP15, frequency=1000)

DUTY = 1
TIMES = 5
for _ in range(TIMES):
    for _ in range(15):
        led2.duty_cycle = 2**DUTY - 1
        sleep(0.05)
        DUTY = DUTY + 1
    for _ in range(15):
        led2.duty_cycle = 2**DUTY - 1
        sleep(0.05)
        DUTY = DUTY - 1


# Example 3
# with 2 leds

white_led = pwmio.PWMOut(board.GP15, frequency=1000)
green_led = pwmio.PWMOut(board.GP13, frequency=1000)

Max_Duty = 2**16 - 1

for _ in range(20):
    white_led.duty_cycle = Max_Duty
    sleep(0.1)
    white_led.duty_cycle = 0
    green_led.duty_cycle = Max_Duty
    sleep(0.1)
    green_led.duty_cycle = 0


# Example 5
# led becomes brighter
# than dimmer

for _ in range(3):
    for x in range(2**16):
        led2.duty_cycle = x
    for x in range(2**16, 0, -1):
        led2.duty_cycle = x - 1
