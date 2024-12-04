import os
import logging
import numpy as np

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def main(inputfile):
    grid = [ list(l.strip()) for l in open(inputfile)]
    grid = np.array(grid)
    idim, jdim = grid.shape

    patterns = [
            [["M", ".", "M"],
             [".", "A", "."],
             ["S", ".", "S"]],
            [["M", ".", "S"],
             [".", "A", "."],
             ["M", ".", "S"]],
            [["S", ".", "S"],
             [".", "A", "."],
             ["M", ".", "M"]],
            [["S", ".", "M"],
             [".", "A", "."],
             ["S", ".", "M"]],
            ]
    patterns = [np.array(p) for p in patterns]

    count = 0
    for i in range(1, idim-1):
        for j in range(1, jdim-1):
            part = grid[i-1:i+2, j-1:j+2].copy()
            part[0,1] = "."
            part[1,0] = "."
            part[1,2] = "."
            part[2,1] = "."
            for pattern in patterns:
                if np.all(pattern == part):
                    count += 1
                    print(count, part)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
