import board
from neopixel import NeoPixel
from time import sleep


matrix = NeoPixel(board.IO1, 64) # 256


COLOR = (127, 16, 0)
BLACK = (0, 0, 0)

for px in range(matrix.n):
    matrix[px] = COLOR
    sleep(.02)

#matrix.fill(COLOR)

for _ in range(3):
    for b in range(100, -1, -1):
        matrix.brightness = b / 100
        sleep(.01)
    for b in range(0, 101, 1):
        matrix.brightness = b / 100
        sleep(.01)

matrix.fill(BLACK)


# întrebare:
#
# dat fiind că eu am acces unidimensional la pixeli
#    matrix[ț]
#
# cum am putea avea acces bidimensional?
#    matrix[x][y]
#    matrix[x, y]

# răspuns:
# făcând un calcul matematic, din care obținum o funcție
# f(x, y) ==> ț
#
# și făcând o structură de date accesibilă după tupla (x, y)
#
# și atunci,
# my_bidi_matrix[x, y] = COLOR
# va rezulta în
# underlying_neopixel_instance[ț] = COLOR


"""

f(0, 0) => 0
f(0, 2) => 2
f(0, 7) => 7
f(1, 7) => 8 
f(1, 6) => 9
f(1, 1) => 14
f(3, 0) => 16


....


matrix[f(5, 2)] = COLOR
"""

