import board
from neopixel import NeoPixel
from time import sleep

matrix = NeoPixel(board.IO1, 256, brightness=0.2)

BLACK = (0, 0, 0)


# we want a 256-value color wheel,
# because 256 pixels
def rgb_color_wheel(x):
    if 0 <= x < 85:
        return (255 - x * 3, x * 3, 0)
    elif 85 <= x < 85 * 2:
        x -= 85
        return (0, 255 - x * 3, x * 3)
    else:
        x -= 85 * 2
        return (x * 3, 0, 255 - x * 3)


for x in range(matrix.n):
    matrix[x] = rgb_color_wheel(x)

    sleep(.002)


sleep(5)

# we clean up
matrix.fill(BLACK)
matrix.write()
