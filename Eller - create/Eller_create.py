import numpy as np
import random
from PIL import Image
import time


def delete_right_wall(center):
    for p in range(center[0] - 2, center[0] + 3):
        pixels[p][center[1] + 3] = 255


def delete_bottom_wall(center):
    for p in range(center[1] - 2, center[1] + 3):
        pixels[center[0] + 3][p] = 255


width = int(input("ширина: "))
height = int(input("высота: "))

img_width = width * 6 + 1
img_height = height * 6 + 1

pixels = np.full((img_height, img_width), 255, dtype=np.uint8)

# рисуем сетку
for x in range(0, img_width, 6):
    for y in range(img_height):
        pixels[y][x] = 0

for x in range(0, img_height, 6):
    for y in range(img_width):
        pixels[x][y] = 0

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 1. СОЗДАЕТСЯ ПЕРВАЯ СТРОКА
set_number = 1

line = [[0, True] for i in range(width)]

this_cell_center = [3, 3]
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

start = time.time() # начинаем отсчет времени

for row in range(height):
    # = = = = = = = = = = = = = = = = = 2. ЯЧЕЙКАМ, НЕ ВХОДЯЩИМ ВО МНОЖЕСТВО, ПРИСВАИВАЕТСЯ СВОЕ УНИКАЛЬНОЕ МНОЖЕСТВО
    for c in line:
        if c[0] == 0:
            c[0], c[1] = set_number, True
            set_number += 1
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    # = = = = = = = = = = = = = = = = находим, какие множества представлены в строке = = = = = = = = = = = = = = = =
    line_sets = []

    for i in line:
        line_sets.append(i[0])
        line_sets = sorted(set(line_sets), key=lambda x: line_sets.index(x))
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    # = = = = = = = = = = = = = = = = = = = создаем словарь из списка множеств = = = = = = = = = = = = = = = = = = =
    sets = {s:[] for s in line_sets}

    for s in sets:
        for l in range(width):
            if line[l][0] == s:
                sets[s].append(l)
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

    if row == height - 1:   # если последняя строка
        for i in range(width - 1):
            if line[i][0] != line[i + 1][0]:
                temp = line[i + 1][0]

                sets[line[i][0]].extend(sets[line[i + 1][0]])

                for c in sets[line[i + 1][0]]:
                    line[c][0] = line[i][0]

                sets[temp] = []

                delete_right_wall(this_cell_center)

            else:
                pass

            this_cell_center[1] += 6

    else:
        # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 3. ДВИГАЯСЬ СЛЕВА НАПРАВО, СОЗДАЮТСЯ ПРАВЫЕ СТЕНЫ
        for i in range(width - 1):
            if line[i][0] != line[i + 1][0] and random.randint(0, 1) == 1:
                temp = line[i + 1][0]

                sets[line[i][0]].extend(sets[line[i + 1][0]])

                for c in sets[line[i + 1][0]]:
                    line[c][0] = line[i][0]

                sets[temp] = []

                delete_right_wall(this_cell_center)

            else:
                pass

            this_cell_center[1] += 6

        this_cell_center[1] = 3
        # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

        # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 4. ДВИГАЯСЬ СЛЕВА НАПРАВО, СОЗДАЮТСЯ НИЖНИЕ СТЕНЫ
        for s in sets:
            set_length = len(sets[s])

            if set_length == 0:
                pass

            elif set_length == 1:
                line[sets[s][0]][1] = False

            else:
                how_much_passages = random.randrange(1, set_length)
                walls_with_passages = random.sample(sets[s], how_much_passages)

                for w in walls_with_passages:   # присваиваем логическое значение стены
                    line[w][1] = False

        for c in line:
            if not c[1]:    # если значение стены False, то ломаем стену снизу
                delete_bottom_wall(this_cell_center)
                c[1] = True

            else:
                if row != height - 1:
                    c[0] = 0
                    c[1] = True

            this_cell_center[1] += 6

        this_cell_center[0] += 6
        this_cell_center[1] = 3

print("\ncreated in %.5f" % (time.time() - start))

img = Image.fromarray(pixels)
img.save("eller_maze.png")
img.show()
