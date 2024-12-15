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


def pushv(i, j, movement, grid):
    idim, jdim = grid.shape[:2]
    assert grid[i, j] == "[" or grid[i, j] == "]"
    if grid[i, j] == "]":
        j -= 1

    if movement == "^":
        di = -1
    elif movement == "v":
        di = 1
    else:
        raise ValueError(movement)

    Q = [(int(i), int(j))]
    B = []
    while Q:
        i, j = Q.pop()
        B.append((i, j))
        i2 = i + di
        if grid[i2, j] == "." and grid[i2, j+1] == ".":
            continue
        if grid[i2, j] == "[":
            Q.append((i2, j))
        elif grid[i2, j] == "#" or grid[i2, j+1] == "#":
            return None
        else:
            if grid[i2, j] == "]":
                Q.append((i2, j-1))
            if grid[i2, j+1] == "[":
                Q.append((i2, j+1))

    logger.debug(f"  these can be pushed: {B}")
    for box in B:
        i, j = box
        grid[i, j:j+2] = "."
    for box in B:
        i, j = box
        grid[i+di, j] = "["
        grid[i+di, j+1] = "]"
    return True


def push(i, j, movement, grid):
    idim, jdim = grid.shape[:2]
    if movement == "<":
        try:
            j1 = next(j1 for j1 in range(j, 0, -1) if grid[i, j1] != "[" and grid[i, j1] != "]")
        except StopIteration:
            return False
        if grid[i, j1] == "#":
            return False
        assert grid[i, j1] == "."
        grid[i, j1:j] = grid[i, j1+1:j+1]
    elif movement == ">":
        try:
            j2 = next(j2 for j2 in range(j, jdim) if grid[i, j2] != "[" and grid[i, j2] != "]")
        except StopIteration:
            return False
        if grid[i, j2] == "#":
            return False
        assert grid[i, j2] == "."
        grid[i, j:j2+1] = grid[i, j-1:j2]
    elif movement == "^":
        return pushv(i, j, movement, grid)
    elif movement == "v":
        return pushv(i, j, movement, grid)

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

    assert grid[i, j] == "[" or grid[i, j] == "]"

    logger.debug(f"moving attempt {movement}, {i}, {j}")
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

    for movement in movements:
        logger.debug(f"move {movement}, {robot=}")
        robot = step(robot, grid, movement)
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
    args = parser.parse_args()
    main(args.input)
