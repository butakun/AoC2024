import os
import logging
import numpy as np

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def read(inputfile):
    f = open(inputfile)
    rules = []
    for l in f:
        l = l.strip()
        if len(l) == 0:
            break
        p1, p2 = l.split("|")
        p1, p2 = int(p1), int(p2)
        rules.append((p1, p2))

    updates = []
    for l in f:
        update = [int(i) for i in l.split(",")]
        updates.append(update)

    print(rules)
    print(updates)

    return rules, updates


def check(update, rules):
    for page1, page2 in rules:
        try:
            i1 = update.index(page1)
        except:
            i1 = -1
        try:
            i2 = update.index(page2)
        except:
            i2 = -1
        if i1 >= 0 and i2 >= 0:
            if i1 > i2:
                return False
    return True


def main(inputfile):
    rules, updates = read(inputfile)

    count = 0
    for i, update in enumerate(updates):
        if check(update, rules):
            print(i, update)
            l = len(update)
            assert l % 2 == 1
            imid = int(l / 2)
            print(update[imid])
            count += update[imid]
    print(count)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
