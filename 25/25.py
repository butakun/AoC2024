import os
import logging
import numpy as np
from collections import defaultdict

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def read(inputfile):
    f = open(inputfile)
    shapes = []
    shape = []
    for l in f:
        l = l.strip()
        if len(l) == 0:
            shapes.append(shape)
            shape = []
        else:
            shape.append(l)
    assert shape
    shapes.append(shape)

    hole_height = None
    locks = []
    keys = []
    for s in shapes:
        s = np.array([ list(l) for l in s ])
        is_key = np.all(s[0, :] == "#")
        idim, jdim = s.shape[:2]
        assert hole_height is None or hole_height == idim
        hole_height = idim
        vv = np.zeros(jdim, dtype=np.int64)
        if is_key:
            for j in range(jdim):
                h = s[:, j].tolist().index(".")
                vv[j] = h - 1
            locks.append(vv)
        else:
            for j in range(jdim):
                h = s[:, j].tolist().index("#")
                vv[j] = idim - h -1
            keys.append(vv)

    hole_height -= 2

    return locks, keys, hole_height

def main(inputfile):
    locks, keys, hole_height = read(inputfile)
    print(f"{hole_height=}")

    match = 0
    for lock in locks:
        for key in keys:
            hh = lock + key
            if np.all(hh <= hole_height):
                print(f"{key=} matches {lock=}")
                match += 1
    print(match)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
