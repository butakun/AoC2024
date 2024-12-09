import os
import logging
import numpy as np
from collections import defaultdict
from itertools import combinations

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def main(inputfile):
    blocks = open(inputfile).readline().strip()
    blocks = list(map(int, list(blocks)))
    print(blocks)
    N = sum(blocks)
    print(N)

    disk = ["."] * N
    empty = False
    j = 0
    i = 0
    for b in blocks:
        if empty:
            for _ in range(b):
                disk[j] = "."
                j += 1
        else:
            for _ in range(b):
                disk[j] = i
                j += 1
            i += 1
        empty = not empty
    print(disk)

    i = disk.index(".")
    j = N - 1
    while i < j:
        if disk[j] != ".":
            disk[i] = disk[j]
            j -= 1
            try:
                i_ = disk[i:].index(".")
                i = i + i_
            except:
                print("no more empty slot")
        else:
            j -= 1
        #print("".join(list(map(str, disk))))

    try:
        end = disk.index(".")
        if end > j:
            end = j + 1
    except:
        end = j + 1
    print("".join(list(map(str, disk[:end]))))

    s = 0
    for i, b in enumerate(disk[:end]):
        s += i * b
    print(s)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
