from PIL import Image
import numpy as np
import time
import random


def dig(r, c):
    pixels[r, c] = 255


maze_width = int(input("Ширина: "))
maze_height = int(input("Высота: "))

width = maze_width * 2 + 1
height = maze_height * 2 + 1

pixels = np.zeros((height, width), dtype=np.uint8)

paths = []
# paths = set()

all_positions = maze_width * maze_height

start = time.time()

row = random.randrange(1, height-1, 2)
col = random.randrange(1, width-1, 2)

dig(row, col)
paths.append([row, col])
# paths.add((row, col))

iterations = 0
in_deadend = 0

UP = (0, -2)
DOWN = (0, 2)
LEFT = (-2, 0)
RIGHT = (2, 0)

directions = [UP, DOWN, LEFT, RIGHT]


visited = 1

while visited < all_positions:
    iterations += 1

    if len(directions) == 0:
        in_deadend += 1


        # paths.discard((row, col))

        row, col = random.choice(paths)
        # row, col = random.choice(list(paths))

        directions = [UP, DOWN, LEFT, RIGHT]

    else:
        direction = random.choice(directions)

        d_col, d_row = direction

        if 0 < row + d_row < height and 0 < col + d_col < width and pixels[row + d_row, col + d_col] != 255:
            row += d_row
            col += d_col
            dig(row, col)

            dig(row - d_row // 2, col - d_col // 2)

            directions = [UP, DOWN, LEFT, RIGHT]

            visited += 1
            paths.append([row, col])
            # paths.add((row, col))
        else:
            directions.remove(direction)


print('iterations: ', iterations)
print('been in deadend: ', in_deadend)

pixels[0, random.randrange(1, width-1, 2)] = 255
pixels[height-1, random.randrange(1, width-1, 2)] = 255

print("\ncreated in %.5f" % (time.time() - start))

size = int(width * 10), int(height * 10)

img = Image.fromarray(pixels)
img = img.resize(size, Image.NEAREST)
img.save('maze.png')
img.show()
