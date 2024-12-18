import os
import logging
import re
import numpy as np
from dijkstra import dijkstra

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


class Maze:
    def __init__(self, bytes):
        self.bytes = bytes
        ary = np.array(bytes)
        imax, jmax = ary.max(axis=0)
        idim, jdim = imax + 1, jmax + 1
        self.idim = idim
        self.jdim = jdim

    def __getitem__(self, u):
        i, j = u
        vv = []
        if i > 0 and (i-1, j) not in self.bytes:
            vv.append(((i-1, j), 1))
        if i < self.idim - 1 and (i+1, j) not in self.bytes:
            vv.append(((i+1, j), 1))
        if j > 0 and (i, j-1) not in self.bytes:
            vv.append(((i, j-1), 1))
        if j < self.jdim - 1 and (i, j+1) not in self.bytes:
            vv.append(((i, j+1), 1))
        logger.debug(f"maze: {u=}, {vv=}")
        return vv

    def is_goal(self, u):
        i, j = u
        return i == self.idim - 1 and j == self.jdim - 1


def read(inputfile):
    bytes = [ tuple(list(map(int, l.strip().split(",")))) for l in open(inputfile) ]
    return bytes


def main(inputfile, vis):
    bytes = read(inputfile)

    maze = Maze(bytes[:1024])

    u0 = (0, 0)
    print(maze[u0])
    dijkstra(maze, u0, lambda u: maze.is_goal(u), debug_freq=1)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    parser.add_argument("--vis", action="store_true")
    args = parser.parse_args()
    main(args.input, args.vis)
