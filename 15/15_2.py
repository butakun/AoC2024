import os
import logging
import re
import numpy as np
from canvas import Canvas

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def read(inputfile):
    f = open(inputfile)
    grid = []
    while True:
        line = f.readline().strip()
        if not line:
            break
        line = line.replace("#", "##")
        line = line.replace("O", "[]")
        line = line.replace(".", "..")
        line = line.replace("@", "@.")
        grid.append(list(line))
    grid = np.array(grid)

    movements = []
    for line in f:
        movements.extend(list(line.strip()))

    return grid, movements


def dump(grid):
    for l in grid:
        print("".join(l))


def can_move_to(i, j, movement, grid):
    if grid[i, j] == ".":
        return True, []
    elif grid[i, j] == "#":
        return False, []

    if grid[i, j] == "]":
        j -= 1
    assert grid[i, j] == "[" and grid[i, j+1] == "]"

    Q = [(i, j)]
    B = []
    while Q:
        i, j = Q.pop()
        B.append((i, j))

        if movement == ">":
            if grid[i, j+2] == "#":
                return False, []
            if grid[i, j+2] == "[":
                Q.append((i, j+2))
        elif movement == "<":
            if grid[i, j-1] == "#":
                return False, []
            if grid[i, j-1] == "]":
                Q.append((i, j-2))
        elif movement == "v":
            if grid[i+1, j] == "#" or grid[i+1, j+1] == "#":
                return False, []
            if grid[i+1, j] == "[":
                Q.append((i+1, j))
            elif grid[i+1, j] == "]":
                Q.append((i+1, j-1))
            if grid[i+1, j+1] == "[":
                Q.append((i+1, j+1))
        elif movement == "^":
            if grid[i-1, j] == "#" or grid[i-1, j+1] == "#":
                return False, []
            if grid[i-1, j] == "[":
                Q.append((i-1, j))
            elif grid[i-1, j] == "]":
                Q.append((i-1, j-1))
            if grid[i-1, j+1] == "[":
                Q.append((i-1, j+1))

    return True, B


def step(robot, grid, movement):
    idim, jdim = grid.shape[:2]
    i, j = robot
    i1, j1 = i, j

    if movement == "<":
        di, dj = 0, -1
    elif movement == ">":
        di, dj = 0, 1
    elif movement == "^":
        di, dj = -1, 0
    elif movement == "v":
        di, dj = 1, 0
    else:
        raise ValueError(movement)

    i2, j2 = i1 + di, j1 + dj
    logger.debug(f"moving attempt {movement}, {i2}, {j2}")

    move, boxes = can_move_to(i2, j2, movement, grid)
    if not move:
        return i1, j1

    to = [(i_+di, j_+dj) for i_, j_ in boxes]
    logger.debug(f"  {boxes} can move to {to}")
    for i, j in boxes:
        grid[i, j] = "."
        grid[i, j+1] = "."
    for i, j in to:
        grid[i, j] = "["
        grid[i, j+1] = "]"
    grid[i1, j1] = "."
    grid[i2, j2] = "@"
    return i2, j2


def main(inputfile, vis):
    grid, movements = read(inputfile)

    i, j = np.where(grid == "@")
    i, j = int(i[0]), int(j[0])
    assert grid[i, j] == "@"
    robot = [i, j]

    dump(grid)
    if vis:
        canvas = Canvas()
        canvas.draw_frame(grid)
    for i, movement in enumerate(movements):
        logger.debug(f"move {movement}, {robot=}")
        robot = step(robot, grid, movement)
        if vis and i % 100 == 0:
            canvas.draw_frame(grid)

    dump(grid)
    total = 0
    boxes = np.stack(np.where(grid == "["), axis=-1)
    for i, j in boxes:
        total += 100 * i + j
    print(total)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    parser.add_argument("--vis", action="store_true")
    args = parser.parse_args()
    main(args.input, args.vis)
