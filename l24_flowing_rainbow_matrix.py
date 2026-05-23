import board
from neopixel import NeoPixel
from time import sleep

matrix = NeoPixel(board.IO1, 256, brightness=0.2, auto_write=False)

# we want a 256-value color wheel,
# because 256 pixels
def rgb_256_color_wheel(x):
    if 0 <= x < 85:
        return (255 - x * 3, x * 3, 0)
    elif 85 <= x < 85 * 2:
        x -= 85
        return (0, 255 - x * 3, x * 3)
    else:
        x -= 85 * 2
        return (x * 3, 0, 255 - x * 3)

# we cache all values, because no need to make cpu crazy
ALL_COLORS = [
    rgb_256_color_wheel(x)
    for x in range(256)
]

offset = 0
while True:
    for x in range(matrix.n):
        matrix[x] = ALL_COLORS[(x + offset) % 256]
    matrix.write()
    sleep(.0001)

    offset += 1
    # let's be easy on the memory and wrap the offset
    if offset == 256:
        offset = 0
