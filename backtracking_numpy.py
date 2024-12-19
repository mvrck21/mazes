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

all_positions = maze_width * maze_height

start = time.time() # засекает время

row = random.randrange(1, height-1, 2)
col = random.randrange(1, width-1, 2)

dig(row, col)
paths = np.array([[row, col, 0]])

directions = ['up', 'down', 'left', 'right']

iterations = 0

visited = 1

while visited < all_positions:
    iterations += 1

    if len(directions) == 0:
        row, col, deadend = list(paths[np.random.choice(paths.shape[0], 1, replace=False)])[0]

        directions = ['up', 'down', 'left', 'right']

    else:
        direction = random.choice(directions)

        if direction == 'up':
            if row-2 > 0 and pixels[row-2, col] != 255:
                row -= 2
                dig(row+1, col)
                dig(row, col)
                directions = ['up', 'down', 'left', 'right']
                visited += 1
                paths = np.append(paths, [[row, col, 0]], axis=0)

            else:
                directions.remove(direction)

        if direction == 'down':
            if row+2 <= height - 2 and pixels[row+2, col] != 255:
                row += 2
                dig(row-1, col)
                dig(row, col)
                directions = ['up', 'down', 'left', 'right']
                visited += 1
                paths = np.append(paths, [[row, col, 0]], axis=0)
            else:
                directions.remove(direction)

        if direction == 'left':
            if col-2 > 0 and pixels[row, col-2] != 255:
                col -= 2
                dig(row, col+1)
                dig(row, col)
                directions = ['up', 'down', 'left', 'right']
                visited += 1
                paths = np.append(paths, [[row, col, 0]], axis=0)
            else:
                directions.remove(direction)

        if direction == 'right':
            if col+2 <= width - 2 and pixels[row, col+2] != 255:
                col += 2
                dig(row, col-1)
                dig(row, col)
                directions = ['up', 'down', 'left', 'right']
                visited += 1
                paths = np.append(paths, [[row, col, 0]], axis=0)
            else:
                directions.remove(direction)

print(iterations)

pixels[0, random.randrange(1, width-1, 2)] = 255
pixels[height-1, random.randrange(1, width-1, 2)] = 255

print("\n created in %.5f" % (time.time() - start))

size = int(width * 10.5), int(height * 10.5)

img = Image.fromarray(pixels)
img = img.resize(size, Image.NEAREST)
img.save('maze.png')
img.show()

# очень плохо - при 300х300 неизвестно, сколько времени