import asyncio

from neopixel import NeoPixel

import config


class LempModeBase:
    "this is The Base for all Lemps"

    def __init__(self):
        self.init_hw()

    def init_hw(self):
        # TODO: receive specific brightness on init?
        self.matrix = NeoPixel(config.MATRIX_PIN, config.MATRIX_PIXELS, brightness=.2)

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._brightness = value
        self.matrix.brightness = value / 255

    #####################################################
    #### this has been put aside
    #### because it is trigger material.
    #
    # 1. brightness este ceva comun tututor lămpilor.
    # 2. este "canalul" default. (cu el începem, la el ne întoarcem după timeout)
    # 3. vrem să fie accesibil ușor.
    #    adică, se comporte seemless ca un "canal" / "mod" al tututor lămpilor
    #    (adică, clicking the (only!..?) button also cycles through it,
    #     regardless of how many other "modes" / "channels" the Lemp has)
    #
    #####################################################


    # d.p.d.v. tehnic!!
    # 1. brightness-ul este schimbabil în orice Lemp
    # 2. it is stable across Lemps

    # implicații:
    # a) brightness-ul are nevoie de setări personalizate
    #    de rotary encoder.
    # b) când suntem într-un Lemp care are alt rotary encoder,
    #    trebuie să putem face cumva switch între aceste rotenc-uri.


    # altă implicație:
    # cineva top-level face switch între moduri.


class BrightnessMode(LempModeBase):
    def __init__(self, initial=0):
        super().__init__()

        # TODO: maybe make the initial color
        # a tuple, not a number
        self.on_encoder_event(initial)

    def init_hw(self):
        super().init_hw()

        self.encoder = AcceleratedBoundedBoostedRotaryEncoder(
            config.ROTENC_PIN1, config.ROTENC_PIN2,
            0, 0xFF,
            callback=self.on_encoder_event
        )
