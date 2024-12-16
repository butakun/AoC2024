import os
import logging
import re
import numpy as np
from dijkstra2 import dijkstra

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


class Maze:
    def __init__(self, grid):
        self.grid = grid

    def __getitem__(self, u):
        turn = 1000
        i, j, dir = u
        vv = []
        if dir == "E":
            vv.append(((i, j, "N"), turn))
            vv.append(((i, j, "S"), turn))
            if self.grid[i, j+1] != "#":
                vv.append(((i, j+1, "E"), 1))
        elif dir == "W":
            vv.append(((i, j, "N"), turn))
            vv.append(((i, j, "S"), turn))
            if self.grid[i, j-1] != "#":
                vv.append(((i, j-1, "W"), 1))
        elif dir == "S":
            vv.append(((i, j, "E"), turn))
            vv.append(((i, j, "W"), turn))
            if self.grid[i+1, j] != "#":
                vv.append(((i+1, j, "S"), 1))
        elif dir == "N":
            vv.append(((i, j, "E"), turn))
            vv.append(((i, j, "W"), turn))
            if self.grid[i-1, j] != "#":
                vv.append(((i-1, j, "N"), 1))
        return vv

    def is_goal(self, u):
        i, j, _ = u
        return self.grid[i, j] == "E"


def read(inputfile):
    grid = [ list(l.strip()) for l in open(inputfile) ]
    return np.array(grid)


def main(inputfile, vis):
    grid = read(inputfile)
    i, j = np.stack(np.where(grid == "S"), axis=-1)[0]
    u0 = (int(i), int(j), "E")
    print(u0)

    maze = Maze(grid)

    nodes, distance = dijkstra(maze, u0, lambda u: maze.is_goal(u), debug_freq=1)
    logger.debug(f"{nodes}")
    logger.debug(f"{len(nodes)}")
    logger.debug(f"{distance=}")

    spots = set((i, j) for i, j, _ in nodes)
    print(spots)
    print(len(spots))

    g = grid.copy()
    for i, j in spots:
        g[i, j] = "O"
    print(g)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    parser.add_argument("--vis", action="store_true")
    args = parser.parse_args()
    main(args.input, args.vis)
