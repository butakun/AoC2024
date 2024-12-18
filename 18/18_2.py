import os
import logging
import re
import numpy as np
from dijkstra import dijkstra

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


class Maze:
    def __init__(self, bytes, imax, jmax):
        self.bytes = bytes
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
    imax, jmax = np.array(bytes).max(axis=0)

    u0 = (0, 0)

    i_lower = 1
    i_upper = len(bytes)
    stop_at = None
    while True:
        i_mid = (i_upper + i_lower) // 2
        maze = Maze(bytes[:i_mid], imax, jmax)
        logger.debug(f"trying {i_mid=}, {i_lower=}, {i_upper=}")
        path, best_distance = dijkstra(maze, u0, lambda u: maze.is_goal(u), premature=True, debug_freq=1)
        if path is None:
            i_upper = i_mid
        else:
            i_lower = i_mid
        if i_upper == i_lower + 1:
            stop_at = i_upper
            break
    print(stop_at, bytes[stop_at-1])

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    parser.add_argument("--vis", action="store_true")
    args = parser.parse_args()
    main(args.input, args.vis)
