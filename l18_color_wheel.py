# p e r f e c t ! ! !

# oile placide
# s-au așternut la iernat
# privesc nutrețul cu multă poftă
# din care vor consuma
# iarna întreagă

import neopixel
import board
import time

px = neopixel.NeoPixel(board.NEOPIXEL, 1)

# avem nevoie de o funcție ce primește input
# o valoare între 0-255
# și returnează o tuplă de la
# (255, 0, 0) la (128, 127, 0) la (0, 255, 0)
# la (0, 128, 127) la (0, 0, 255) la (127, 0, 128)
# la (255, 0, 0) la...

_ALL_DISTINCT_VALUES = (
    [(x, 255 - x, 0) for x in range(255, 0, -1)] +
    [(0, x, 255 - x) for x in range(255, 0, -1)] +
    [(255 - x, 0, x) for x in range(255, 0, -1)]
)

def get_colorwheel_value(v):
    # future me, solve this problem.
    # make no mistakes.

    # v must be between range(0, 255 * 3) !!!

    return _ALL_DISTINCT_VALUES[v]

get_colorwheel_value(0) == (255, 0, 0)
get_colorwheel_value(255) == (0, 255, 0)
get_colorwheel_value(510) == (0, 0, 255)
get_colorwheel_value(764) == (254, 0, 1)


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


while True:
    for x in range(0, 255 * 3):
        color = get_colorwheel_value(x)
        px.fill(color)
        time.sleep(.01)

# 255   0   0
# 128 127   0
#   0 255   0
#   0 128 127
#   0   0 255 
# 127   0 128
# 254   0   0
