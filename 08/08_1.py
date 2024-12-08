import os
import logging
import numpy as np
from collections import defaultdict
from itertools import combinations

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def read(inputfile):
    grid = np.array([ list(l.strip()) for l in open(inputfile) ])
    return grid


def main(inputfile):
    grid = read(inputfile)
    idim, jdim = grid.shape

    nodes = set()

    ij = np.where(grid != ".")
    ants = [ (i, j) for i, j in zip(ij[0], ij[1]) ]
    freqs = defaultdict(list)
    for i1, j1 in ants:
        freq = grid[i1, j1]
        freqs[freq].append((i1, j1))
    logger.debug(f"{freqs=}")

    for freq, pp in freqs.items():
        logger.debug(f"{freq}:")
        for p1, p2 in combinations(pp, 2):
            p1 = np.array(p1)
            p2 = np.array(p2)
            logger.debug(f"-> {p1}, {p2}")
            d = p2 - p1
            p3 = p1 - d
            p4 = p2 + d
            for pa in [p3, p4]:
                if pa[0] < 0 or pa[0] >= idim or pa[1] < 0 or pa[1] >= jdim:
                    continue
                nodes.add((pa[0], pa[1]))
                logger.debug(f"   => {pa[0]}, {pa[1]}")

    logger.debug(f"{nodes=}")
    print(len(nodes))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
