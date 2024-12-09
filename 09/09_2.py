import os
import logging
import numpy as np
from collections import defaultdict
from itertools import combinations

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def main(inputfile):
    pattern = open(inputfile).readline().strip()
    pattern = list(map(int, list(pattern)))

    disk = []
    empty = False
    fid = 0
    for i in pattern:
        if empty:
            if i > 0:
                disk.append([-1, i])
        else:
            assert i > 0
            disk.append([fid, i])
            fid += 1
        empty = not empty

    tail = []
    done = set()
    logger.debug(f"start: {disk[:5]} .. {disk[-5:]} | {tail[:10]}")

    iloop = 0
    #while disk and iloop < 4:
    while disk:
        f = disk.pop()
        while f[0] < 0 or f[0] in done:
            tail.insert(0, f)
            f = disk.pop()
        assert f[0] >= 0

        logger.debug(f"moving {f}")
        moved = False
        for i, d in enumerate(disk):
            if d[0] < 0:
                if d[1] > f[1]:
                    disk.insert(i, [f[0], f[1]])
                    disk[i + 1] = [-1, d[1] - f[1]]
                    disk.append([-1, f[1]])

                    moved = True
                    #logger.debug(f"yes: {disk} | {tail}")
                    logger.debug(f"yes: {disk[:5]} .. {disk[-5:]} | {tail[:10]}")
                    break
                elif d[1] == f[1]:
                    disk[i] = [f[0], f[1]]
                    disk.append([-1, f[1]])

                    moved = True
                    #logger.debug(f"yes: {disk} | {tail}")
                    logger.debug(f"yes: {disk[:5]} .. {disk[-5:]} | {tail[:10]}")
                    break
        if not moved:
            tail.insert(0, f)
            #logger.debug(f"no: {disk} | {tail}")
            logger.debug(f"no: {disk[:5]} .. {disk[-5:]} | {tail[:10]}")

        done.add(f[0])
        iloop += 1

    disk = disk + tail
    #print(f"final: {disk}")
    #return

    s = 0
    i = 0
    for fid, len in disk:
        if fid >= 0:
            for j in range(len):
                print(f"adding {fid} * {i + j} = {fid * (i + j)}")
                s += fid * (i + j)
        i += len
    print(s)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
