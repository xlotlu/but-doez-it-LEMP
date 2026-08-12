import asyncio
from collections import deque

from neopixel import NeoPixel
from async_button import Button

from rotenc import (
    RotaryEncoder,
    BoundedRotaryEncoder,
    WraparoundRotaryEncoder,
    AcceleratedRotaryEncoder,
    AcceleratedBoundedRotaryEncoder,
    AcceleratedWraparoundRotaryEncoder,
    AcceleratedBoundedBoostedRotaryEncoder,
)
#from button import Button

import colors
import config


# 1. lampa are mai multe moduri de funcționare.
# 2. fiecare mod face ceva diferit!
#    și poate folosi un alt mod de rotary encoder.
# 3. nice commentating is nice.


# ==== Lamp Mode 1 ==== #
#      "The Lemp"
# 
# 


# lemp brightness:
# 0 -   1: in Neopixel instance
# 0 - 255: in our code
# r, g, b: 0 - 255 fiecare

# AcceleratedBoundedRotaryEncoder

# 1. Avem "submoduri" (ce tunăm în momentul curent)
# - brightness
# - r
# - g
# - b

# 2. By default rotenc tunează brightness

# 3. click pe buton --> schimbă "submodul"

# 4. timeout, when no input, return to default submode
#    (adică după 30 secunde când eram pe un canal, trece pe brightness)


# RGBLemp          #  <-- submod
# ColorWheelLemp   #  <-- submod

# some Lemp attributes are global,
# other are mode-specific.
#
# e.g. globals:
#  - current color
#  - current brightness


class Lemp:
    # this is the RGBLemp
    # mental note: this will be split apart into submodes
    # (when the time comes)

    def __init__(self, color=colors.AMBER, brightness=12):
        self.init_hw()

        self.color = color
        self.brightness = brightness

        # channels are 0 to 3:
        # 0 = brightness
        # 1-3 = r, g, b
        self._current_channel = 0

        # make sure the encoder value is set to the current channel's value
        # (that is, brightness at this point)
        self.reset_encoder()

        # TODO: read values from saved state
        # (as it was saved before power off, and now we load previous values)

    def init_hw(self):
        self.encoder = AcceleratedBoundedBoostedRotaryEncoder(config.ROTENC_PIN1, config.ROTENC_PIN2,
                                                       0, 0xFF,
                                                       callback=self.on_encoder_event)
        self.button = Button(config.BUTTON_PIN,
                             value_when_pressed=False,
                             long_click_min_duration=1.0,
                             long_click_enable=True,
                             double_click_enable=False,
                            )
        self.matrix = NeoPixel(config.MATRIX_PIN, config.MATRIX_PIXELS)

        asyncio.create_task(self.monitor_button())

    @property
    def color(self):
        return self._r, self._g, self._b

    @color.setter
    def color(self, value):
        self._r, self._g, self._b = value
        self.matrix.fill(value)

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._brightness = value
        self.matrix.brightness = value / 255

    def on_encoder_event(self, value):
        # which is the current channel?
        if self._current_channel == 0:
            # this is the brightness
            self.brightness = value
        else:
            # this is one of the color channels
            idx = self._current_channel - 1
            color = list(self.color)
            color[idx] = value
            self.color = color

        print("  --", self.encoder.value, self.color)

    def on_click(self):
        self.next_channel()
        self.reset_encoder()

    def on_timeout(self):
        self._current_channel = 0

    def next_channel(self):
        self._current_channel += 1
        # wraparound:
        if self._current_channel > 3:
            self._current_channel = 0

        print("» channel:", self._current_channel)

    def reset_encoder(self):
        # which is the current channel?
        if self._current_channel == 0:
            # this is the brightness
            self.encoder.value = self.brightness
        else:
            # this is one of the color channels
            idx = self._current_channel - 1
            self.encoder.value = self.color[idx]

    async def monitor_button(self):
        while True:
            event = await self.button.wait(Button.PRESSED)
            # and then, the payload:
            self.on_click()

    async def monitor_rotenc(self):
        while True:
            value = await self.encoder.wait()
            self.on_encoder_event(value)
            #await asyncio.sleep_ms(something)


    async def lemp(self):
        rotenc_ticker = asyncio.create_task(self.encoder.monitor())
        await asyncio.gather(rotenc_ticker)
