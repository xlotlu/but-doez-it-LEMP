import board
import digitalio


# -- Lesson 6 --
#
# button turns off LED

led = digitalio.DigitalInOut(board.GP15)
led.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.GP16)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

while True:
    if button.value == False:
        led.value = True
    else:
        led.value = False
