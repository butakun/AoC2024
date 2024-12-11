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
    stones2 = dict()
    for stone, count in stones.items():
        st = str(stone)
        lst = len(st)
        if stone == 0:
            if 1 in stones2:
                stones2[1] += count
            else:
                stones2[1] = count
        elif lst % 2 == 0:
            i = lst // 2
            stone_l = int(st[:i])
            stone_r = int(st[i:])
            for s in [stone_l, stone_r]:
                if s in stones2:
                    stones2[s] += count
                else:
                    stones2[s] = count
        else:
            i = int(stone * 2024)
            if i in stones2:
                stones2[i] += count
            else:
                stones2[i] = count
    return stones2


def main(inputfile):
    stones = read(inputfile)
    logger.debug(stones)

    m = dict()
    for stone in stones:
        if stone in m:
            m[stone] += 1
        else:
            m[stone] = 1
    stones = m

    for i in range(75):
        stones = blink(stones)
        logger.debug(stones)

    print(sum(stones.values()))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
