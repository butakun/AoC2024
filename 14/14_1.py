import os
import logging
import re
import numpy as np

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def read(inputfile):
    pat = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
    robots = [ list(map(int, pat.match(l).groups())) for l in open(inputfile) ]
    robots = [ [[v[0], v[1]], [v[2], v[3]]] for v in robots ]
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
    c = q[0] * q[1] * q[2] * q[3]
    return c


def main(inputfile):
    robots = read(inputfile)
    print(robots)

    imax, jmax = np.max(robots[:, 0, :], axis=0)
    idim, jdim = imax + 1, jmax + 1
    shape = np.array([idim, jdim])

    dump(robots, shape)

    t = 100
    robots2 = []
    for robot in robots:
        p, v = robot
        p2 = p + v * t
        p2 = p2 % shape
        robots2.append([p2, v])

    dump(robots2, shape)
    c = count(robots2, shape)
    print(c)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
