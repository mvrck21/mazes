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


def add_frontiers(current_coord):
    if current_coord[0] > 0 and maze[current_coord[0] - 1][current_coord[1]] == 0:
        frontiers.append([current_coord[0] - 1, current_coord[1]])
        maze[current_coord[0] - 1][current_coord[1]] = 1

    if current_coord[0] < height - 1 and maze[current_coord[0] + 1][current_coord[1]] == 0:
        frontiers.append([current_coord[0] + 1, current_coord[1]])
        maze[current_coord[0] + 1][current_coord[1]] = 1

    if current_coord[1] > 0 and maze[current_coord[0]][current_coord[1] - 1] == 0:
        frontiers.append([current_coord[0], current_coord[1] - 1])
        maze[current_coord[0]][current_coord[1] - 1] = 1

    if current_coord[1] < width - 1 and maze[current_coord[0]][current_coord[1] + 1] == 0:
        frontiers.append([current_coord[0], current_coord[1] + 1])
        maze[current_coord[0]][current_coord[1] + 1] = 1


width = int(input("ширина: "))
height = int(input("высота: "))

img_width = width * 6 + 1
img_height = height * 6 + 1

maze = [[0 for i in range(width)] for j in range(height)]

pixels = np.full((img_height, img_width), 255, dtype=np.uint8)

start = time.time()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - рисуем сетку
for x in range(0, img_width, 6):
    for y in range(img_height):
        pixels[y][x] = 0

for x in range(0, img_height, 6):
    for y in range(img_width):
        pixels[x][y] = 0

frontiers = []  # массив под клетки на рубеже

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = начинаем со случано выбранной клетки
current_coord = [random.randrange(height), random.randrange(width)]     # координаты начальной точки

maze[current_coord[0]][current_coord[1]] = 2    # отмечаем точку как посещенную

add_frontiers(current_coord)

# = = = = = = = = = = = = = = = = = = = = = = = продолжаем, пока есть клетки на рубеже (пока есть непосещенные клетки)
directions = ['up', 'down', 'left', 'right']    # направления, в которых можно присоединиться

while len(frontiers) > 0:
    current_coord = random.choice(frontiers)    # выбираем случайную точку на рубеже

    while maze[current_coord[0]][current_coord[1]] != 2:    # пока текущая клетка не будет отмечена как посещенная
        direction = random.choice(directions)    # случайным образом выбирается направление для присоединения

        if direction == 'up':
            if current_coord[0] > 0 and maze[current_coord[0] - 1][current_coord[1]] == 2:  # если уже посещена
                maze[current_coord[0]][current_coord[1]] = 2
                add_frontiers(current_coord)
                frontiers.remove(current_coord)
                delete_bottom_wall([6 + 6 * (current_coord[0] - 1), 3 + 6 * current_coord[1]])
            else:
                pass

        if direction == 'down':
            if current_coord[0] < height - 1 and maze[current_coord[0] + 1][current_coord[1]] == 2:
                maze[current_coord[0]][current_coord[1]] = 2
                add_frontiers(current_coord)
                frontiers.remove(current_coord)
                delete_bottom_wall([6 + 6 * current_coord[0], 3 + 6 * current_coord[1]])
            else:
                pass

        if direction == 'left':
            if current_coord[1] > 0 and maze[current_coord[0]][current_coord[1] - 1] == 2:  # если уже посещена
                maze[current_coord[0]][current_coord[1]] = 2
                add_frontiers(current_coord)
                frontiers.remove(current_coord)
                delete_right_wall([3 + 6 * current_coord[0], 6 + 6 * (current_coord[1] - 1)])
            else:
                pass

        if direction == 'right':
            if current_coord[1] < width - 1 and maze[current_coord[0]][current_coord[1] + 1] == 2:  # если уже посещена
                maze[current_coord[0]][current_coord[1]] = 2
                add_frontiers(current_coord)
                frontiers.remove(current_coord)
                delete_right_wall([3 + 6 * (current_coord[0]), 6 + 6 * current_coord[1]])
            else:
                pass

print("\ncreated in %.5f" % (time.time() - start))

img = Image.fromarray(pixels)
img.save("maze.png")
img.show()