import board
from neopixel import NeoPixel
from time import sleep


matrix = NeoPixel(board.IO1, 64) # 256


while True:
    matrix.fill((127, 12, 0))
    sleep(6)
    matrix.fill((0, 0, 0))
    sleep(2)
