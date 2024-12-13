import os
import logging
import numpy as np
from collections import defaultdict
from itertools import combinations
from math import prod
from factor import prime_factors

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def read(inputfile):
    machines = []
    with open(inputfile) as f:
        while True:
            try:
                buttons = []
                for _ in range(2):
                    tokens = f.readline().strip().split()
                    dx, dy = tokens[2], tokens[3]
                    dx, dy = int(dx[2:-1]), int(dy[2:])
                    buttons.append([dx, dy])
                tokens = f.readline().strip().split()
                x, y = tokens[1], tokens[2]
                x, y = int(x[2:-1]), int(y[2:])
                x += 10000000000000
                y += 10000000000000
                machines.append([buttons, [x, y]])
                f.readline()
            except:
                break

    return machines


def play(machine):
    buttons, (x, y) = machine
    ax, ay = buttons[0]
    bx, by = buttons[1]
    logger.debug(ax, ay, bx, by, x, y)

    # ax * a + bx * b = x
    # ay * a + by * b = y
    # by * ax * a + by * bx * b = by * x
    # bx * ay * a + bx * by * b = bx * y
    # (by * ax - bx * ay) * a = by * x - bx * y
    lhs = by * ax - bx * ay
    rhs = by * x - bx * y
    rem_a = rhs % lhs
    if rem_a != 0:
        return None
    a = rhs // lhs

    # bx * b = x - ax * a
    bxb = x - ax * a
    rem_b = bxb % bx
    if rem_b != 0:
        return None
    b = bxb // bx

    return a * 3 + b


def main(inputfile):
    machines = read(inputfile)
    logger.debug(machines)

    total = 0
    for machine in machines:
        tokens = play(machine)
        if tokens is not None:
            total += tokens
    print(total)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
