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
all_positions = maze_width * maze_height

start = time.time()     # засекает время

row = random.randrange(1, height-1, 2)
col = random.randrange(1, width-1, 2)

dig(row, col)
paths.append([row, col, 0])

directions = ['up', 'down', 'left', 'right']

iterations = 0
in_deadend = 0


direction_to_coords = {'up': {'y':-2, 'half': 1}, 'down': {'y': 2, 'half': -1}, 'left': { 'x': -2, 'half': 1}, 'right': { 'x': 2, 'half': -1}}


visited = 1

while visited < all_positions:
    iterations += 1

    if len(directions) == 0:
        in_deadend += 1

        row, col, deadend = random.choice(paths)

        directions = ['up', 'down', 'left', 'right']

    else:
        direction = random.choice(directions)

        direction_action = direction_to_coords[direction]

        if 'y' in direction_action:
            if 0 < row + direction_action['y'] <= height - 2 and pixels[row + direction_action['y'], col] != 255:
                row += direction_action['y']
                dig(row + direction_action['half'], col)
                dig(row, col)
                directions = ['up', 'down', 'left', 'right']
                visited += 1
                paths.append([row, col, 0])
            else:
                directions.remove(direction)
        else:
            if 0 < col + direction_action['x'] <= width - 2 and pixels[row, col + direction_action['x']] != 255:
                col += direction_action['x']
                dig(row, col + direction_action['half'])
                dig(row, col)
                directions = ['up', 'down', 'left', 'right']
                visited += 1
                paths.append([row, col, 0])
            else:
                directions.remove(direction)


print('iterations: ', iterations)
print('been in deadend: ', in_deadend )

pixels[0, random.randrange(1, width-1, 2)] = 255
pixels[height-1, random.randrange(1, width-1, 2)] = 255

print("\ncreated in %.5f" % (time.time() - start))

size = int(width * 10), int(height * 10)

img = Image.fromarray(pixels)
img = img.resize(size, Image.NEAREST)
img.save('maze.png')
img.show()
