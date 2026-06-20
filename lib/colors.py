from adafruit_led_animation.color import *

# TODO: make this generic, universal, nice, and not hardcoded.
#       and maybe a class, because Darius like class
def rgb_color_wheel(x):
    """Color wheel to allow for cycling through the rainbow of RGB colors."""
    x = x % (255 * 3)

    if 0 <= x < 255:
        return (255 - x, x, 0)
    elif 255 <= x < 255 * 2:
        x -= 255
        return (0, 255 - x, x)
    else:
        x -= 255 * 2
        return (x, 0, 255 - x)
