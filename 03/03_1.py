import os
import logging
import re

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def main(inputfile):
    lines = [l.strip() for l in open(inputfile)]

    res = 0
    pat = re.compile(r"mul\(([0-9]+),([0-9]+)\)")
    for l in lines:
        pairs = [(int(a), int(b)) for a, b in pat.findall(l)]
        print(pairs)
        muls = [ a * b for a, b in pairs ]
        res += sum(muls)
    print(res)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
