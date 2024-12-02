import os
import logging
import numpy as np

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def read(filename):
    reports = [ l.split() for l in open(filename) ]
    reports = [ [int(i) for i in l ] for l in reports ]
    return reports


def check(r):
    d = r[1:] - r[:-1]
    if np.all(d > 0) and np.all(d <= 3):
        return True
    elif np.all(d < 0) and np.all(d >= -3):
        return True 
    return False

def loose_check(r):
    if check(r):
        return True

    for i in range(len(r)):
        r2 = r.copy().tolist()
        r2.pop(i)
        r2 = np.array(r2)
        if check(r2):
            logger.debug(f"but {r2} is ok")
            return True

    return False


def main(inputfile):
    reports = read(inputfile)

    count = 0
    for r in reports:
        r = np.array(r)
        logger.debug(f"* {r}")
        if loose_check(r):
            logger.debug("OK")
            count += 1
    print(count)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
