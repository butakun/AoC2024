import os
import logging
import re
import numpy as np

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def read(inputfile):
    f = open(inputfile)
    grid = []
    while True:
        line = f.readline().strip()
        if not line:
            break
        grid.append(list(line))
    grid = np.array(grid)

    movements = []
    for line in f:
        movements.extend(list(line.strip()))

    return grid, movements


def push(i, j, movement, grid):
    idim, jdim = grid.shape[:2]
    if movement == "<":
        try:
            j1 = next(j1 for j1 in range(j, 0, -1) if grid[i, j1] != "O")
        except StopIteration:
            return False
        if grid[i, j1] == "#":
            return False
        grid[i, j1:j] = "O"
    elif movement == ">":
        try:
            j2 = next(j2 for j2 in range(j, jdim) if grid[i, j2] != "O")
        except StopIteration:
            return False
        if grid[i, j2] == "#":
            return False
        grid[i, j+1:j2+1] = "O"
    elif movement == "^":
        try:
            i1 = next(i1 for i1 in range(i, 0, -1) if grid[i1, j] != "O")
        except StopIteration:
            return False
        if grid[i1, j] == "#":
            return False
        grid[i1:i, j] = "O"
    elif movement == "v":
        try:
            i2 = next(i2 for i2 in range(i, idim) if grid[i2, j] != "O")
        except StopIteration:
            return False
        if grid[i2, j] == "#":
            return False
        grid[i+1:i2+1, j] = "O"
    return True


def step(robot, grid, movement):
    idim, jdim = grid.shape[:2]
    i, j = robot
    i0, j0 = i, j

    if movement == "<":
        j -= 1
    elif movement == ">":
        j += 1
    elif movement == "^":
        i -= 1
    elif movement == "v":
        i += 1
    else:
        raise ValueError(movement)

    if grid[i, j] == "#":
        return i0, j0

    if grid[i, j] == ".":
        grid[i0, j0] = "."
        grid[i, j] = "@"
        return i, j

    assert grid[i, j] == "O"

    print("moving attempt ", movement, i, j)
    if push(i, j, movement, grid):
        grid[i0, j0] = "."
        grid[i, j] = "@"
        return i, j
    return i0, j0



def main(inputfile):
    grid, movements = read(inputfile)

    i, j = np.where(grid == "@")
    i, j = i[0], j[0]
    assert grid[i, j] == "@"
    robot = [i, j]

    print(grid)
    for movement in movements:
        print(f"move {movement}, {robot=}")
        robot = step(robot, grid, movement)
        print(grid)

    total = 0
    boxes = np.stack(np.where(grid == "O"), axis=-1)
    for i, j in boxes:
        total += 100 * i + j
    print(total)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
