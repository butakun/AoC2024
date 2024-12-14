import os
import logging
import numpy as np
from collections import defaultdict
from itertools import combinations
from math import prod

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def read(inputfile):
    robots = [ l.strip().split() for l in open(inputfile) ]
    robots = [ [p[2:].split(","), v[2:].split(",")] for p, v in robots ]
    robots = [ [[int(p[0]), int(p[1])], [int(v[0]), int(v[1])]] for p, v in robots ]
    return np.array(robots)


def dump(robots, shape):
    grid = np.zeros(shape, dtype=np.uint64)
    for p, _ in robots:
        grid[p[0], p[1]] += 1
    grid = grid[:-1:2,:-1:2] + grid[1::2,1::2]

    grid = grid.astype(np.str_)
    grid[grid == "0"] = "."
    grid = grid.T
    for l in grid:
        print("".join(l))


def count(robots, shape):
    idim, jdim = shape
    oi, oj = idim // 2, jdim // 2

    q = [0] * 4
    for (x, y), _ in robots:
        if x > oi and y > oj:
            q[0] += 1
        elif x < oi and y > oj:
            q[1] += 1
        elif x < oi and y < oj:
            q[2] += 1
        elif x > oi and y < oj:
            q[3] += 1
            i = 3
    return q


def step(robots, shape, t=1):
    robots2 = []
    for robot in robots:
        p, v = robot
        p2 = p + v * t
        p2 = p2 % shape
        robots2.append([p2, v])
    return robots2


def main(inputfile):
    robots = read(inputfile)

    imax, jmax = np.max(robots[:, 0, :], axis=0)
    idim, jdim = imax + 1, jmax + 1
    print(idim, jdim)
    shape = np.array([idim, jdim])

    N = len(robots)

    t = 1
    while True:
        robots = step(robots, shape)
        q = count(robots, shape)
        print(f"step {t}, {q=}")
        if max(q) > (N * 0.5):
            break
        t += 1
    dump(robots, shape)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
