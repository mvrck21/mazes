from PIL import Image
import numpy as np
import time

key_points = [] # здесь будут храниться ключевые точки (будущие узлы)
nodes = []
path = []
exit_point = []


class Node:
    def __init__(self, row, col, parent):
        self.row = row
        self.col = col
        self.parent = parent
        self.children = []


# если точка находится не в туннеле, то добавить точку в ключевые
def if_node(row, col):
    if (maze[row-1][col-1][0], maze[row-1][col][0], maze[row-1][col+1][0],
        maze[row][col - 1][0], maze[row][col][0], maze[row][col + 1][0],
        maze[row + 1][col-1][0], maze[row+1][col][0], maze[row+1][col+1][0]) == (0, 0, 0, 255, 255, 255, 0, 0, 0):
        pass
    elif (maze[row-1][col-1][0], maze[row][col-1][0], maze[row+1][col-1][0],
        maze[row-1][col][0], maze[row][col][0], maze[row + 1][col][0],
        maze[row - 1][col + 1][0], maze[row][col+1][0], maze[row + 1][col + 1][0]) == (0, 0, 0, 255, 255, 255, 0, 0, 0):
        pass
    else:
        key_points.append([row, col])


def connect_nodes(node1, node2):
    y_distance = node2[0] - node1[0]
    x_distance = node2[1] - node1[1]

    if y_distance == 0:
        if x_distance > 0:
            for i in range(node1[1] + 1, node1[1] + x_distance, 1):
                path.append([node1[0], i])
        if x_distance < 0:
            for i in range(node1[1] + x_distance + 1, node1[1], 1):
                path.append([node1[0], i])

    if x_distance == 0:
        if y_distance > 0:
            for i in range(node1[0] + 1, node1[0] + y_distance, 1):
                path.append([i, node1[1]])
        if y_distance < 0:
            for i in range(node1[0] + y_distance + 1, node1[0], 1):
                path.append([i, node1[1]])


maze = np.array(Image.open('maze.png'))

start = time.time()

# а эти две строки для чего? считает количество линий по вертикали и по горизонтали (не стены)
vertical = (len(maze[0]) - 1) // 2
horizontal = (len(maze) - 1) // 2

for i in range(1, len(maze), 2):
    for j in range(1, len(maze[0]), 2):
        if_node(i, j)

for i in key_points:
    print(i)

nodes_count = len(key_points)
print("всего узлов: %d \n\n\n" % nodes_count)

for i in range(len(maze[0])):
    if maze[0, i, 0] == 255:
        nodes.append(Node(1, i, None))
        if [1, i] not in key_points:
            key_points.append([1, i])
        key_points.remove([1, i])
        path.append([0, i])
        path.append([1, i])
        print("start at:", 1, i, "\n\n\n")

    if maze[len(maze) - 1, i, 0] == 255:
        path.append([len(maze) - 1, i])
        exit_point = [len(maze) - 2, i]
        print("end at:", len(maze) - 2, i)

current_node = 0
while current_node < nodes_count:
    print("current node:", current_node, "nodes count:", nodes_count)

    row = nodes[current_node].row
    col = nodes[current_node].col

    if [row, col] == exit_point:
        break

    c_row = row
    c_col = col

    while [c_row, c_col] not in key_points and maze[c_row, c_col][0] != 0 and c_row > 0:
        c_row -= 1
        if [c_row, c_col] in key_points:
            nodes.append(Node(c_row, c_col, nodes[current_node]))
            key_points.remove([c_row, c_col])
            nodes[current_node].children.append(nodes[len(nodes) - 1])
            break

    print("posle UP: ", end="")
    for i in nodes:
        print(i.row, i.col, end="    ")

    c_row = row

    while [c_row, c_col] not in key_points and maze[c_row, c_col][0] != 0 and c_col < len(maze[0]) - 1:
        c_col += 1
        if [c_row, c_col] in key_points:
            nodes.append(Node(c_row, c_col, nodes[current_node]))
            key_points.remove([c_row, c_col])
            nodes[current_node].children.append(nodes[len(nodes) - 1])
            break

    print("posle RIGHT: ", end="")
    for i in nodes:
        print(i.row, i.col, end="    ")


    c_col = col

    while [c_row, c_col] not in key_points and maze[c_row, c_col][0] != 0 and c_row < len(maze) - 1:
        c_row += 1
        if [c_row, c_col] in key_points:
            nodes.append(Node(c_row, c_col, nodes[current_node]))
            key_points.remove([c_row, c_col])
            nodes[current_node].children.append(nodes[len(nodes) - 1])
            break

    print("posle DOWN: ", end="")
    for i in nodes:
        print(i.row, i.col, end="    ")

    c_row = row

    while [c_row, c_col] not in key_points and maze[c_row, c_col][0] != 0 and c_col > 0:
        c_col -= 1
        if [c_row, c_col] in key_points:
            nodes.append(Node(c_row, c_col, nodes[current_node]))
            key_points.remove([c_row, c_col])
            nodes[current_node].children.append(nodes[len(nodes) - 1])
            break

    print("posle LEFT: ", end="")
    for i in nodes:
        print(i.row, i.col, end="    ")

    print("\n\n")

    current_node += 1


prev_node_coord = [nodes[current_node].row, nodes[current_node].col]
current_node_coord = [nodes[current_node].row, nodes[current_node].col]
current_node = nodes[current_node]

while current_node.parent != None:
    current_node_coord = [current_node.row, current_node.col]
    path.append(current_node_coord)

    if len(current_node.children) > 0:
        connect_nodes(prev_node_coord, current_node_coord)
        prev_node_coord = current_node_coord

    current_node = current_node.parent

connect_nodes(current_node_coord, [nodes[0].row, nodes[0].col])

print("\ndone in %.8f" % (time.time() - start), end="")

for p in path:
    maze[p[0], p[1], 0] = 60
    maze[p[0], p[1], 1] = 150
    maze[p[0], p[1], 2] = 200

# for n in key_points:
#     maze[n[0], n[1], 0] = 255
#     maze[n[0], n[1], 1] = 109
#     maze[n[0], n[1], 2] = 16

# for n in nodes:
#     maze[n[0], n[1], 0] = 0
#     maze[n[0], n[1], 1] = 255
#     maze[n[0], n[1], 2] = 0

print("path length:", len(path))

img = Image.fromarray(maze, "RGB")
img.save('solved_maze.png')
img.show()

# ИНОГДА ПОКАЗЫВАЕТ ПАРУ ТУПИКОВЫХ КЛЕТОК