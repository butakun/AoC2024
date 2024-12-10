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

    total = 0
    for head in heads:
        Q = [head]
        rating = 0
        while Q:
            i, j = Q.pop(0)
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
                    rating += 1
                    continue
                Q.append((i2, j2))
        logger.debug(f"{head} -> {rating}")
        total += rating
    print(total)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
