import os
import logging
import numpy as np

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def main(inputfile):
    grid = [ list(l.strip()) for l in open(inputfile)]
    grid = np.array(grid)
    idim, jdim = grid.shape

    xmas = list("XMAS")

    dijs = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (-1, -1), (1, -1)]
    ijs = np.where(grid == "X")
    ijs = [ (int(i), int(j)) for i, j in zip(ijs[0], ijs[1]) ]
    patterns = [ [ij] * len(dijs) for ij in ijs ]
    print(patterns)

    for letter2 in list("MAS"):
        patterns2 = []
        for pattern in patterns:
            print(pattern)
            pattern2 = [None] * 8
            found = False
            for k, dij in enumerate(dijs):
                ij = pattern[k]
                if ij is None:
                    continue
                ij2 = ij[0] + dij[0], ij[1] + dij[1]
                print(f"{ij}->{ij2}")
                if ij2[0] < 0 or ij2[0] >= idim or ij2[1] < 0 or ij2[1] >= jdim:
                    continue
                if grid[ij2[0], ij2[1]] == letter2:
                    pattern2[k] = ij2
                    found = True
            if found:
                print(pattern2)
                patterns2.append(pattern2)
        patterns = patterns2

    count = 0
    for i, pattern in enumerate(patterns):
        for p in pattern:
            if p is not None:
                count += 1
        print(i, pattern)
    print(count)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
