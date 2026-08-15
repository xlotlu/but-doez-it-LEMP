from neopixel import NeoPixel

from rotenc import AcceleratedWraparoundRotaryEncoder

from colors import rgb_color_wheel


class ColorWheelLemp:
    def __init__(self, initial=0):
        self.init_hw()

        # TODO: maybe make the initial color
        # a tuple, not a number
        self.on_encoder_event(initial)

    def init_hw(self):
        self.encoder = AcceleratedWraparoundRotaryEncoder(
            config.ROTENC_PIN1, config.ROTENC_PIN2,
            0, 0xFF * 3 - 1,
            callback=self.on_encoder_event
        )

        # TODO: this is common to all modes
        self.matrix = NeoPixel(config.MATRIX_PIN, config.MATRIX_PIXELS)

    def on_encoder_event(self, value):
        color = rgb_color_wheel(value)
        self.matrix.fill(color)

    async def lemp(self):
        rotenc_ticker = asyncio.create_task(self.encoder.monitor())
        await asyncio.gather(rotenc_ticker)
