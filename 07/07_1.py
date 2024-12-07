import os
import logging

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def read(inputfile):
    eqs = []
    for l in open(inputfile):
        v, coefs = l.strip().split(":")
        v = int(v)
        coefs = list(map(int, coefs.split()))
        eqs.append([v, coefs])

    return eqs


def evaluate(coefs, ops):
    v = coefs[0]
    for op, v2 in zip(ops, coefs[1:]):
        if op == "+":
            v = v + v2
        elif op == "*":
            v = v * v2
    return v

def test(v, coefs):

    ss = [""]
    for i in range(len(coefs)-1):
        ss2 = []
        for s in ss:
            ss2 += [s + "*"]
            ss2 += [s + "+"]
        ss = ss2

    for ops in ss:
        vv = evaluate(coefs, ops)
        if v == vv:
            logger.debug(f"{coefs}, {ops}, {vv}")
            return True
    return False


def main(inputfile):
    eqs = read(inputfile)

    s = 0
    for v, coefs in eqs:
        ok = test(v, coefs)
        if ok:
            s += v
    print(s)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
