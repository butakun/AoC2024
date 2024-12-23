import os
import logging
from collections import defaultdict
from itertools import combinations

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def main(inputfile):
    connections = [ l.strip().split("-") for l in open(inputfile) ]
    
    links = { a: b for a, b in connections }
    computers = set(links.keys())

    g = defaultdict(set)
    for a, b in connections:
        g[a].add(b)
        g[b].add(a)
    g = dict(g)

    t_groups = set()
    for c1, c2, c3 in combinations(computers, 3):
        if c1[0] == "t" or c2[0] == "t" or c3[0] == "t":
            if c1 in g[c2] and c1 in g[c3] and c2 in g[c3]:
                group = tuple(set([c1, c2, c3]))
                t_groups.add(group)
                print(group)
    print(len(t_groups))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
