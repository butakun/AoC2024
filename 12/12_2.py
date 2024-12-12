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


def build_graph(nodes, connected):
    G = defaultdict(set)
    for node1, node2 in combinations(nodes, 2):
        if connected(node1, node2):
            G[node1].add(node2)
            G[node2].add(node1)
    # orphan nodes
    for node in nodes:
        if node not in G:
            G[node] = set()
    return dict(G)


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


def count_sides(peri):
    peri = list(peri)

    def connected_perimeter(peri1, peri2):
        p1, n1 = peri1
        p2, n2 = peri2
        if n1[0] != n2[0] or n1[1] != n2[1]:
            return False
        di = p2[0] - p1[0]
        dj = p2[1] - p1[1]
        if (abs(di) + abs(dj)) != 1:
            return False
        return True

    GS = build_graph(peri, connected_perimeter)
    logger.debug(f"{GS=}")

    components = connected_components(GS)

    return len(components)


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
        sides = count_sides(peri)
        logger.info(f"{plant=}, {area=}, {sides=}")
        price += area * sides
    print(price)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
