"""
the task ahead:

animate a single pixel linearly across the matrix
(it's gonna be a 1-pixel snek)

"""

import board
from neopixel import NeoPixel
from time import sleep



# we init without auto-write,
# because now we create actual animations
# (we need to redraw more pixels at once)
matrix = NeoPixel(board.IO1, 256, auto_write=False)


COLOR = (127, 16, 0)
BLACK = (0, 0, 0)


for px in range(matrix.n):
    # we turn on the current pixel
    matrix[px] = COLOR
    # and turn off the previous pixel
    matrix[px - 1] = BLACK

    # we "commit" manually, so all the changes are atomic
    matrix.write()

    sleep(.002)


# și să treacă dintr-o parte în alta?
# while True:
#    for:
#        ...



# we clean up
matrix.fill(BLACK)
matrix.write()
