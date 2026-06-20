import board
import digitalio
from lib.config import LED1_PIN


# -- Lesson 6 --
#
# button turns off LED

led = digitalio.DigitalInOut(LED1_PIN)
led.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.GP16)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

while True:
    if button.value == False:
        led.value = True
    else:
        led.value = False
