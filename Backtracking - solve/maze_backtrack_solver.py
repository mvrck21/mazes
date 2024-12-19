from PIL import Image
import numpy as np
import random
import time

maze = np.array(Image.open('maze.png'))
current = None
exit_pos = None

start = time.time()

path = []
visited = []

for i in range(len(maze[0])):
    if maze[0, i, 0] == 255:
        path.append([0, i])
        current = [1, i]
    if maze[len(maze)-1, i, 0]:
        path.append([len(maze)-1, i])
        exit_pos = [len(maze)-2, i]

directions = ['up', 'down', 'left', 'right']

row, col = current
path.append(current)
visited.append(current)
deadends = 0

while current != exit_pos:
    row, col = current

    if len(directions) == 0:
        del path[-2:]
        current = path[-1]
        directions = ['up', 'down', 'left', 'right']

    else:
        direction = random.choice(directions)

        if direction == 'up':
            if row - 2 > 0 and maze[row-1, col, 0] != 0 and \
                    maze[row - 2, col, 0] == 255 and [row - 2, col] not in visited:
                current = [row-2, col]
                visited.append([row - 1, col])
                visited.append(current)
                path.append([row - 1, col])
                path.append(current)
                directions = ['up', 'down', 'left', 'right']
            else:
                directions.remove(direction)

        if direction == 'down':
            if row + 2 <= len(maze) - 2 and maze[row+1, col, 0] != 0 and \
                    maze[row + 2, col, 0] == 255 and [row + 2, col] not in visited:
                current = [row+2, col]
                visited.append([row + 1, col])
                visited.append(current)
                path.append([row + 1, col])
                path.append(current)
                directions = ['up', 'down', 'left', 'right']
            else:
                directions.remove(direction)

        if direction == 'left':
            if col - 2 > 0 and maze[row, col-1, 0] != 0 and \
                    maze[row, col - 2, 0] == 255 and [row, col - 2] not in visited:
                current = [row, col - 2]
                visited.append([row, col-1])
                visited.append(current)
                path.append([row, col-1])
                path.append(current)
                directions = ['up', 'down', 'left', 'right']
            else:
                directions.remove(direction)

        if direction == 'right':
            if col + 2 <= len(maze[0]) and maze[row, col+1, 0] != 0 and \
                    maze[row, col + 2, 0] == 255 and [row, col + 2] not in visited:
                current = [row, col + 2]
                visited.append([row, col+1])
                visited.append(current)
                path.append([row, col+1])
                path.append(current)
                directions = ['up', 'down', 'left', 'right']
            else:
                directions.remove(direction)

print("done in %.8f" % abs(start - time.time()), end="")

deadend_blocks = []

for v in visited:
    maze[v[0], v[1], 1] = 200
    maze[v[0], v[1], 2] = 200

    walls = 0
    if maze[v[0]-1, v[1], 2] == 0:
        walls += 1
    if maze[v[0]+1, v[1], 2] == 0:
        walls += 1
    if maze[v[0], v[1]-1, 2] == 0:
        walls += 1
    if maze[v[0], v[1]+1, 2] == 0:
        walls += 1

    if walls > 2:
        deadend_blocks.append([v[0], v[1]])
        deadends += 1


for p in path:
    maze[p[0], p[1], 0] = 60
    maze[p[0], p[1], 1] = 150

print("        been on %s dead_end paths        path length is %s" % (deadends, len(path)))


img = Image.fromarray(maze, "RGB")
img.save('solved_maze.png')
img.show()
