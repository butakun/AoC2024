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


def main(inputfile):
    grid = read(inputfile)
    idim, jdim = grid.shape

    heads = np.stack(np.where(grid == "0"), axis=-1).tolist()
    heads = [ (i, j) for i, j in heads ]

    sum = 0
    for head in heads:
        Q = [head]
        H = set()
        nines = set()
        while Q:
            i, j = Q.pop(0)
            if (i, j) in H:
                continue
            H.add((i, j))
            v = int(grid[i, j])
            nei = []
            for i2, j2 in [[i+1,j], [i-1,j], [i,j+1], [i,j-1]]:
                if i2 < 0 or i2 >= idim or j2 < 0 or j2 >= jdim:
                    continue
                v2 = grid[i2, j2]
                if v2 == ".":
                    continue
                v2 = int(v2)
                if v2 != v + 1:
                    continue
                if v2 == 9:
                    nines.add((i2, j2))
                    continue
                Q.append((i2, j2))
        logger.debug(f"{head} -> {nines}, {len(nines)}")
        sum += len(nines)
    print(sum)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
