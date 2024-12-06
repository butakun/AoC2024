import os
import logging
import numpy as np

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def read(inputfile):
    grid = [ list(l.strip()) for l in open(inputfile) ]
    grid = np.array(grid)
    return grid


def main(inputfile):
    grid = read(inputfile)
    print(grid)

    i, j = np.where(np.logical_and(grid != ".", grid != "#"))
    p = np.array([int(i[0]), int(j[0])])
    print(p)

    idim, jdim = grid.shape

    def turn(g):
        if g == "^":
            return ">"
        elif g == ">":
            return "v"
        elif g == "v":
            return "<"
        elif g == "<":
            return "^"
        else:
            assert False, g

    while True:
        g = grid[p[0], p[1]]
        if g == "^":
            d = np.array([-1, 0])
        elif g == ">":
            d = np.array([0, 1])
        elif g == "v":
            d = np.array([1, 0])
        elif g == "<":
            d = np.array([0, -1])
        else:
            assert False, "g"

        p2 = p + d
        if p2[0] < 0 or p2[0] >= idim or p2[1] < 0 or p2[1] >= jdim:
            break
        g2 = grid[p2[0], p2[1]]
        if g2 == "#":
            grid[p[0], p[1]] = turn(g)
        else:
            grid[p2[0], p2[1]] = g
            p = p2

    print(grid)
    count = np.logical_and(grid != ".", grid != "#").sum()
    print(count)



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
