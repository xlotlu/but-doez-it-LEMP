from rotenc import AcceleratedWraparoundRotaryEncoder

from lemp_mode_base import LempModeBase
from colors import rgb_color_wheel

import config


class RGBColorWheelMode(LempModeBase):
    def __init__(self, initial=0):
        super().__init__()

        # TODO: maybe make the initial color
        # a tuple, not a number
        self.on_encoder_event(initial)

    def init_hw(self):
        super().init_hw()

        self.encoder = AcceleratedWraparoundRotaryEncoder(
            config.ROTENC_PIN1, config.ROTENC_PIN2,
            0, 0xFF * 3 - 1,
            callback=self.on_encoder_event
        )

    def on_encoder_event(self, value):
        color = rgb_color_wheel(value)
        print(color)
        self.matrix.fill(color)

    async def lemp(self):
        rotenc_ticker = asyncio.create_task(self.encoder.monitor())
        await asyncio.gather(rotenc_ticker)
