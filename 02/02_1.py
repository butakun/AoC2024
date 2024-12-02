import os
import logging
import numpy as np
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))


def read(filename):
    reports = [ l.split() for l in open(filename) ]
    reports = [ [int(i) for i in l ] for l in reports ]
    return reports


def main(inputfile):
    reports = read(inputfile)

    count = 0
    for r in reports:
        r = np.array(r)
        d = r[1:] - r[:-1]
        ok = False
        if np.all(d > 0) and np.all(d <= 3):
            count += 1
        elif np.all(d < 0) and np.all(d >= -3):
            count +=1
    print(count)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
