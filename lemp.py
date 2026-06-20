import asyncio
from collections import deque

from neopixel import NeoPixel
from rotenc import (
    RotaryEncoder,
    BoundedRotaryEncoder,
    WraparoundRotaryEncoder,
    AcceleratedRotaryEncoder,
    AcceleratedBoundedRotaryEncoder,
    AcceleratedWraparoundRotaryEncoder,
)


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

    def __init__(self, color=colors.AMBER, brightness=1):
        self.color = color
        self.brightness = brightness
 
        self.channels = {
            'brightness': self._brightness,
            'r': self._r,
            'g': self._g,
            'b': self._b,
        }

        self._chans = deque(self.channels.keys())

        self.init_hw()

    @property
    def color(self):
        return (self._r, self._g, self._b)

    @color.setter
    def color(self, value):
        (self._r, self._g, self._b) = value

    @property
    def brightness(self):
        return self._brightness
    
    @brightness.setter
    def brightness(self, value):
        self._brightness = value

    def init_hw(self):
        self.encoder = AcceleratedBoundedRotaryEncoder(config.ROTENC_PIN1, config.ROTENC_PIN2,
                                                       callback=self.on_encoder_event)
        self.matrix = NeoPixel(config.MATRIX_PIN, 256, brightness=self.brightness)

    def on_encoder_event(self, value):
        # tune the value for the current channel
        self.channels[self.current_channel] = value

    def on_click(self):
        self.next_channel()
        self.encoder.value = self.channels[self.current_channel]

    @property
    def current_channel(self):
        return self._chans[0]
    
    def next_channel(self):   # TODO: on click
        self._chans.rotate(-1)

    def reset_channels(self): # TODO: on timeout
        self._chans.clear()
        self._chans.extend(self.channels.keys())

    async def lemp(self):
        ticker = asyncio.create_task(self.encoder.monitor())
        await asyncio.gather(ticker)
