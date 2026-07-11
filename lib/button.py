import asyncio

from keypad import Keys

from button_handler import (
    ButtonHandler,
    ButtonInput,
    ButtonInitConfig,
)


class Button:
    def __init__(self, pin,
                 on_click_callback=None,
                ):
        _actions = set()
        if on_click_callback is not None:
            _actions.add(ButtonInput(
                ButtonInput.SHORT_PRESS, callback=on_click_callback
            ))

        # TODO:
        # ButtonInput(ButtonInput.LONG_PRESS, callback=long_press)
        # ButtonInput(ButtonInput.HOLD, callback=hold)

        _config = ButtonInitConfig(
            # we don't need double click
            enable_multi_press=False,
            # speedy response to long press.
            # TODO: un-hardcode it
            long_press_threshold=400,
        )

        _keypad = Keys([pin], value_when_pressed=False)
        self._handler = ButtonHandler(
            _keypad.events, _actions, config={0: _config}
        )

    async def monitor(self):
        while True:
            self._handler.update()

            # TODO: un-hardcode this too
            await asyncio.sleep(0.001)