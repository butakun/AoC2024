import os
import logging
import numpy as np
from collections import defaultdict

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def read(inputfile):
    line = open(inputfile).readline().strip().split()
    stones = list(map(int, line))
    return stones

def blink(stones):
    stones2 = []
    for stone in stones:
        st = str(stone)
        lst = len(st)
        if stone == 0:
            stones2.append(1)
        elif lst % 2 == 0:
            i = lst // 2
            stones2.append(int(st[:i]))
            stones2.append(int(st[i:]))
        else:
            stones2.append(stone * 2024)
    return stones2


def main(inputfile):
    stones = read(inputfile)
    logger.debug(stones)

    for _ in range(25):
        stones = blink(stones)
        logger.debug(stones)
    print(len(stones))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
