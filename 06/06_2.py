import os
import logging
import numpy as np
from collections import defaultdict

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def read(inputfile):
    grid = [ list(l.strip()) for l in open(inputfile) ]
    grid = np.array(grid)
    return grid


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


def step(grid, p, past):

    idim, jdim = grid.shape
    p_ = tuple(p)
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
        return None, True
    g2 = grid[p2[0], p2[1]]
    if g2 == "#":
        to = turn(g)
        grid[p[0], p[1]] = to
        past[p_].add(to)
        return p, False

    p2_ = tuple(p2)
    if g in past[p2_]:
        return p2, True
    past[p2_].add(g)

    grid[p2[0], p2[1]] = g
    p = p2
    return p, False


def main(inputfile):
    grid = read(inputfile)
    grid_start = grid.copy()
    print(grid)

    idim, jdim = grid.shape
    past = defaultdict(set)

    i, j = np.where(np.logical_and(grid != ".", grid != "#"))
    p = np.array([int(i[0]), int(j[0])])
    p_start = p.copy()
    print(p)

    g = grid[p[0], p[1]]
    p_ = tuple(p)
    past[p_].add(g)

    grid = grid_start.copy()
    p = p_start.copy()
    done = False
    while not done:
        p, done = step(grid, p, past)

    obstacles = []
    for p_ in past.keys():
        if p_[0] == p_start[0] and p_[1] == p_start[1]:
            continue
        obstacles.append(p_)

    loop = 0
    for o_ in obstacles:
        grid = grid_start.copy()
        grid[o_[0], o_[1]] = "#"
        past = defaultdict(set)
        p = p_start.copy()
        done = False
        while not done:
            p, done = step(grid, p, past)
        if p is not None:
            loop += 1
        print(f"{loop=}")




if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
