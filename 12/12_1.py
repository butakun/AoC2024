import os
import logging
import numpy as np
from collections import defaultdict
from itertools import combinations

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def read(inputfile):
    line = open(inputfile).readline().strip().split()
    grid = [ list(l.strip()) for l in open(inputfile) ]
    grid = np.array(grid)
    return grid


def make_plant_graph(grid):
    idim, jdim = grid.shape

    G = defaultdict(set)
    for i in range(idim):
        for j in range(jdim):
            plant = str(grid[i, j])
            for di, dj in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
                i2 = i + di
                j2 = j + dj
                if i2 < 0 or i2 >= idim or j2 < 0 or j2 >= jdim:
                    continue
                if grid[i2, j2] == plant:
                    G[(i, j)].add((i2, j2))
            if (i, j) not in G:
                G[(i, j)] = set()
    G = dict(G)
    return G


def connected_components(G, new_component_func=None):
    Q = list(G.keys())
    H = set()
    C = []
    while Q:
        c = set()
        q = [Q[0]]
        while q:
            p = q.pop()
            if p in c:
                continue
            c.add(p)
            for nei in G[p]:
                q.append(nei)
        c = list(c)
        if new_component_func is None:
            C.append(c)
        else:
            C.append(new_component_func(c))
        for node in c:
            Q.remove(node)
    return C


def main(inputfile):
    grid = read(inputfile)
    idim, jdim = grid.shape

    G = make_plant_graph(grid)
    logger.debug(f"{G=}")

    def new_plot(component):
        anchor = component[0]
        plant = str(grid[anchor[0], anchor[1]])
        logger.info(f"new plot {plant}: {component}")
        return plant, component

    plots = connected_components(G, new_plot)

    price = 0
    for plant, component in plots:
        area = len(component)
        peri = set()
        for i, j in component:
            for di, dj in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
                i2 = i + di
                j2 = j + dj
                if (i2 < 0 or i2 >= idim or j2 < 0 or j2 >= jdim) or grid[i2, j2] != plant:
                    peri.add(((i, j), (di, dj)))
        logger.info(f"{plant=}, {area=}, {len(peri)=}")
        price += area * len(peri)
    print(price)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
