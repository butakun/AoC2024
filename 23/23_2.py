import os
import logging
from collections import defaultdict

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def main(inputfile):
    connections = [ l.strip().split("-") for l in open(inputfile) ]
    
    G = defaultdict(set)
    for a, b in connections:
        G[a].add(b)
        G[b].add(a)
    G = dict(G)

    biggest = None
    for a in G.keys():
        bb = G[a]
        g = [a]
        for b in bb:
            ok = True
            for m in g:
                if b not in G[m]:
                    ok = False
                    break
            if ok:
                g.append(b)
        g = tuple(sorted(g))
        if biggest is None or len(g) > len(biggest):
            biggest = g

    print(",".join(sorted(biggest)))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
