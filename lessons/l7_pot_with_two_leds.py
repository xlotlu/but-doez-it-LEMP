import analogio
import board
import pwmio
from lib.config import ADC_PIN, LED1_PIN, LED2_PIN

# -- Lesson 7 --
#
# potentiometer makes one brighter
# and the other one dimmer

potentiometer = analogio.AnalogIn(ADC_PIN)
led1 = pwmio.PWMOut(LED1_PIN, frequency=1000)
led2 = pwmio.PWMOut(LED2_PIN, frequency=1000)

while True:
    led2.duty_cycle = 2**16 - 1 - potentiometer.value
    led1.duty_cycle = 0 + potentiometer.value
