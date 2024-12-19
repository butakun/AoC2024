import os
import logging
from collections import defaultdict, deque

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def read(inputfile):
    f = open(inputfile)
    towels = f.readline().strip().replace(" ", "").split(",")
    f.readline()
    designs = [ l.strip()  for l in f ]
    return towels, designs


def design_a_towel(design, towels):
    Q = deque([0])
    H = set()
    D = defaultdict(set)
    N = len(design)

    while Q:
        i = Q.popleft()
        if i >= N:
            continue
        if i in H:
            continue
        H.add(i)

        head = design[i:]
        for t in towels:
            if head.startswith(t):
                logger.debug(f"{i}: {head=} - {t=}")
                Q.append(i + len(t))
                D[i].add(t)

    assert i <= N

    N = len(design)
    HH = dict()
    def dig(ii):
        if ii in HH:
            return HH[ii]
        if ii >= N:
            assert ii == N
            return 1
        leaves_here = 0
        for t in D[ii]:
            leaves_here += dig(ii + len(t))
        HH[ii] = leaves_here
        return leaves_here
    leaves = dig(0)

    return leaves, D


def main(inputfile):
    towels, designs = read(inputfile)

    possible = 0
    total = 0
    for design in designs:
        count, D = design_a_towel(design, towels)
        total += count
        print(f"{design=}, {count=}, {total=}")
        if count > 0:
            possible += 1
    print(total, possible)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
