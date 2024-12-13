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


def common(f1, f2):
    multiplier = dict()
    multiplier1 = dict()
    multiplier2 = dict()

    factors = set(f1) | set(f2)
    for f in factors:
        c1 = f1.count(f)
        c2 = f2.count(f)
        c = max(c1, c2)
        multiplier[f] = c
        multiplier1[f] = c - c1
        multiplier2[f] = c - c2
    return multiplier1, multiplier2, multiplier


def play(machine):
    buttons, (x, y) = machine
    ax, ay = buttons[0]
    bx, by = buttons[1]
    print("PLAY")
    print(ax, ay, bx, by, x, y)

    fax = prime_factors(ax)
    fay = prime_factors(ay)
    fbx = prime_factors(bx)
    fby = prime_factors(by)
    fx = prime_factors(x)
    fy = prime_factors(y)

    print(fax, fay, fbx, fby, fx, fy)

    # cancell b terms
    ffbx, ffby, ffb = common(fbx, fby)
    print(f"b multipliers = {ffbx}, {ffby}, {ffb}")

    feval = lambda ff: prod(pow(f, c) for f, c in ff.items())

    # coef for ax
    cax = defaultdict(lambda: 0)
    for f in fax:
        cax[f] += 1
    for f, c in ffbx.items():
        cax[f] += c
    cax = dict(cax)
    print(f"{cax=}")

    # coef for ay
    cay = defaultdict(lambda: 0)
    for f in fay:
        cay[f] += 1
    for f, c in ffby.items():
        cay[f] += c
    cay = dict(cay)
    print(f"{cay=}")

    # RHS x
    cx = defaultdict(lambda: 0)
    for f in fx:
        cx[f] += 1
    for f, c in ffbx.items():
        cx[f] += c
    cx = dict(cx)
    print(f"{cx=}, {feval(cx)=}")

    # RHS y
    cy = defaultdict(lambda: 0)
    for f in fy:
        cy[f] += 1
    for f, c in ffby.items():
        cy[f] += c
    cy = dict(cy)
    print(f"{cy=}, {feval(cy)=}")


    lhs = feval(cax) - feval(cay)
    rhs = feval(cx) - feval(cy)
    rem = rhs % lhs
    print(f"{lhs} a = {rhs} -> {rem=}")

    if rem == 0:
        a = rhs // lhs
        bxb = (x - ax * a)
        rem2 = bxb % bx
        if rem2 == 0:
            assert bxb % bx == 0, ValueError(f"{a=},{bxb=},{bx=}")
            b = bxb // bx
            tokens = a * 3 + b
            print(f"OK!: {a=}, {b=}, {tokens=}")
            return tokens

    return None

def main(inputfile):
    machines = read(inputfile)
    print(machines)

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
