import os
import logging
from collections import deque

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def read(inputfile):
    f = open(inputfile)
    towels = [ t.strip() for t in f.readline().strip().split(",") ]
    f.readline()
    designs = [ l.strip()  for l in f ]
    return towels, designs


def design_a_towel(design, towels):
    Q = deque([0])
    H = set()
    N = len(design)

    while Q:
        i = Q.popleft()
        if i >= N:
            break
        if i in H:
            continue
        H.add(i)

        head = design[i:]
        for t in towels:
            if head.startswith(t):
                logger.debug(f"{i}: {head=} - {t=}")
                Q.append(i + len(t))

    assert i <= len(design)
    return i == N


def main(inputfile):
    towels, designs = read(inputfile)

    count = 0
    for design in designs:
        possible = design_a_towel(design, towels)
        if possible:
            print(f"OK {design}")
            count += 1
        else:
            print(f"NO {design}")

    print(count)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
