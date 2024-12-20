import os
import logging
from collections import Counter
import numpy as np
from dijkstra import dijkstra_distance, dijkstra


logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


class Maze:
    def __init__(self, grid):
        self.G = grid

    def __getitem__(self, u):
        i, j = u
        vv = []
        if self.G[i + 1, j] != "#":
            vv.append(((i + 1, j), 1))
        if self.G[i - 1, j] != "#":
            vv.append(((i - 1, j), 1))
        if self.G[i, j + 1] != "#":
            vv.append(((i, j + 1), 1))
        if self.G[i, j - 1] != "#":
            vv.append(((i, j - 1), 1))
        return vv

    def is_goal(self, u):
        i, j = u
        return self.G[i, j] == "E"


def read(inputfile):
    grid = [ list(l.strip()) for l in open(inputfile) ]
    return np.array(grid)


def dump(g):
    for row in g:
        print("".join(row))


def cheat(Dsrc, Ddst, distance_max, ncheats, min_save):
    cheats = Counter()
    for (i1, j1), dsrc in Dsrc.items():
        for (i2, j2), ddst in Ddst.items():
            di = i2 - i1
            dj = j2 - j1
            dcheat = abs(di) + abs(dj)
            if dcheat > ncheats:
                continue
            d_total = dsrc + dcheat + ddst
            cheats[d_total] += 1

    d_ = sorted(cheats.keys())
    total = 0
    for d in d_:
        dsave = distance_max - d
        count = cheats[d]
        logger.debug(f"{dsave=}, {d=}: {count=}") 
        if dsave >= min_save:
            total += count
    return total


def main(inputfile):
    ncheats = 20

    grid = read(inputfile)
    maze = Maze(grid)

    u0 = np.stack(np.where(grid == "S"), axis=-1)[0]
    u0 = int(u0[0]), int(u0[1])
    _, distance_max, Dsrc = dijkstra(maze, u0, lambda u: maze.is_goal(u))
    print(f"{distance_max=}")

    ug = np.stack(np.where(grid == "E"), axis=-1)[0]
    ug = int(ug[0]), int(ug[1])
    print(u0, ug)

    Ddst = dijkstra_distance(maze, ug)

    total = cheat(Dsrc, Ddst, distance_max, 2, 100)
    print(f"Part 1: {total}")

    total = cheat(Dsrc, Ddst, distance_max, 20, 100)
    print(f"Part 2: {total}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
