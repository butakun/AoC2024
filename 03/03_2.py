import os
import logging
import re

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def main(inputfile):
    lines = [l.strip() for l in open(inputfile)]

    big = "".join(lines)

    pat = re.compile(r"mul\(([0-9]+),([0-9]+)\)")

    def do(l):
        pairs = [(int(a), int(b)) for a, b in pat.findall(l)]
        muls = [ a * b for a, b in pairs ]
        return muls

    res = 0
    l = big
    stack = []
    while l:
        i = l.find("don't()")
        if i < 0:
            logger.debug(f"+ {l}")
            stack.append(l)
            break
        else:
            s = l[:i]
            if s:
                logger.debug(f"+ {s}")
                stack.append(s)
            l = l[i+7:]
            assert len(l) > 0
            i = l.find("do()")
            if i < 0:
                break
            else:
                l = l[i+4:]
    for buf in stack:
        muls = do(buf)
        s = sum(muls)
        logger.debug(f"{muls=}, {s=}")
        res += s
    print(res)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
