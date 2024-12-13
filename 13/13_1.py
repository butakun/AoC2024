import os
import logging
import numpy as np
from collections import defaultdict
from itertools import combinations
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
                machines.append([buttons, [x, y]])
                f.readline()
            except:
                break

    return machines

def play(machine):
    buttons, (x, y) = machine
    ax, ay = buttons[0]
    bx, by = buttons[1]
    print(ax, ay, bx, by, x, y)

    min_cost = None
    A, B = None, None
    for a in range(100):
        for b in range(100):
            xx = a * ax + b * bx
            yy = a * ay + b * by
            if xx != x or yy != y:
                continue
            cost = 3 * a + b
            if min_cost is None or cost < min_cost:
                A, B = a, b
                min_cost = cost
    print(A, B, min_cost)
    return min_cost

def main(inputfile):
    machines = read(inputfile)
    print(machines)

    total = 0
    for machine in machines:
        min_cost = play(machine)
        if min_cost is not None:
            total += min_cost
    print(total)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
