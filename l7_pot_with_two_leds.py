import analogio
import board
import pwmio

# -- Lesson 7 --
#
# potentiometer makes one brighter
# and the other one dimmer

potentiometer = analogio.AnalogIn(board.GP26)
led1 = pwmio.PWMOut(board.GP15, frequency=1000)
led2 = pwmio.PWMOut(board.GP13, frequency=1000)

while True:
    led2.duty_cycle = 2**16 - 1 - potentiometer.value
    led1.duty_cycle = 0 + potentiometer.value
