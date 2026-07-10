import asyncio

from keypad import Keys

from button_handler import ButtonHandler, ButtonInput


def double_press(): print("Double press detected!")
def short_press(): print("Short press detected!")
def long_press(): print("Long press detected!")
def hold(): print("The button began being held down!")

class Button:
    def __init__(self, pin):
        actions = {
            ButtonInput(ButtonInput.DOUBLE_PRESS, callback=double_press),
            ButtonInput(ButtonInput.SHORT_PRESS, callback=short_press),
            ButtonInput(ButtonInput.LONG_PRESS, callback=long_press),
            ButtonInput(ButtonInput.HOLD, callback=hold),
        }

        scanner = Keys([pin], value_when_pressed=False)
    
        self._handler = ButtonHandler(scanner.events, actions)

    async def monitor(self):
        while True:
            self._handler.update()

            await asyncio.sleep(0.001)