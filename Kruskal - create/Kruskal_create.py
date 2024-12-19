import numpy as np
import random
from PIL import Image
import time


def delete_right_wall(center):
    for p in range(center[0] - 2, center[0] + 3):
        pixels[p][center[1]] = 255


def delete_bottom_wall(center):
    for p in range(center[1] - 2, center[1] + 3):
        pixels[center[0]][p] = 255


width = int(input("ширина: "))
height = int(input("высота: "))

img_width = width * 6 + 1
img_height = height * 6 + 1

# заполняем матрицу числами по возрастанию, начиная с 1. Слева-направо, сверху-вниз
maze = [[i + width * j for i in range(1, width + 1)] for j in range(height)]

pixels = np.full((img_height, img_width), 255, dtype=np.uint8)

start = time.time()     # засекает время выполнения алгоритма

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  рисуем сетку
for x in range(0, img_width, 6):
    for y in range(img_height):
        pixels[y][x] = 0

for x in range(0, img_height, 6):
    for y in range(img_width):
        pixels[x][y] = 0

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - создаем список всех стен между клетками
walls = []

for h in range(height):
    for i in range(width - 1):
        walls.append([[h, i], [h, i + 1]])

for w in range(width):
    for i in range(height - 1):
        walls.append([[i, w], [i + 1, w]])

finish = False

while not finish:
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - находим, какие именно сеты представлены в матрице
    matrix_sets = []

    for row in maze:
        for c in row:
            matrix_sets.append(c)

        matrix_sets = sorted(set(matrix_sets), key=lambda s: matrix_sets.index(s))

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - создаем словарь из списка сетов
    sets = {s: [] for s in matrix_sets}

    for s in sets:
        for h in range(height):
            for w in range(width):
                if maze[h][w] == s:
                    sets[s].append([h, w])

    wall = random.choice(walls)     # выбираем случайную стену из списка всех стен

    if maze[wall[0][0]][wall[0][1]] != maze[wall[1][0]][wall[1][1]]:

        sets[maze[wall[0][0]][wall[0][1]]].extend(sets[maze[wall[1][0]][wall[1][1]]])

        for c in sets[maze[wall[1][0]][wall[1][1]]]:
            maze[c[0]][c[1]] = maze[wall[0][0]][wall[0][1]]

        if wall[0][0] == wall[1][0]:    # горизонтальное соединение
            wall_center = [3 + 6 * wall[0][0], 6 * wall[1][1]]
            delete_right_wall(wall_center)

        else:   # вертикальное соединение
            wall_center = [6 * wall[1][0], 3 + 6 * wall[0][1]]
            delete_bottom_wall(wall_center)

    walls.remove(wall)

    if len(matrix_sets) == 1:
        finish = True

print("\ncreated in %.5f" % (time.time() - start))

img = Image.fromarray(pixels)
img.save("maze.png")
img.show()
