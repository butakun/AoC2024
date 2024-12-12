import os
import logging
import numpy as np
from collections import defaultdict

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "DEBUG"))
logger = logging.getLogger(__name__)


def read(inputfile):
    line = open(inputfile).readline().strip().split()
    grid = [ list(l.strip()) for l in open(inputfile) ]
    grid = np.array(grid)
    return grid

def make_graph(grid):
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
    return G

def count_sides(peri):
    peri = list(peri)
    print(f"{len(peri)}")

    GS = defaultdict(set)
    for p1, n1 in peri:
        for p2, n2 in peri:
            if n1[0] != n2[0] or n1[1] != n2[1]:
                # different direction
                continue
            di = p2[0] - p1[0]
            dj = p2[1] - p1[1]
            if (abs(di) + abs(dj)) != 1:
                # not neighbor
                continue
            print(f"  {p1},{n1} <-> {p2},{n2}")
            GS[(p1, n1)].add((p2, n2))
            GS[(p2, n2)].add((p1, n1))
        if (p1, n1) not in GS:
            GS[(p1, n1)] = set()
    print(f"{GS=}")

    Q = set(GS.keys())
    print(f"{Q=}, {len(Q)=}")

    components = []
    while Q:
        q = [Q.pop()]
        component = set()
        while q:
            p = q.pop()
            if p in component:
                continue
            component.add(p)
            for pnei in GS[p]:
                q.append(pnei)
        print(f"{component=}")
        components.append(component)
        for c in component:
            if c in Q:
                Q.remove(c)
    return len(components)


def measure(grid):
    idim, jdim = grid.shape

    G = make_graph(grid)
    print(f"{G=}")

    H = set()
    plots = []
    for i in range(idim):
        for j in range(jdim):
            if (i, j) in H:
                continue

            Q = [(i, j)]
            component = set()
            while Q:
                ii, jj = Q.pop(0)
                if (ii, jj) in H:
                    continue
                plant = str(grid[ii, jj])
                print(f"{plant=}")
                H.add((ii, jj))
                component.add((ii, jj))
                for nei in G[(ii, jj)]:
                    component.add(nei)
                    if nei not in H:
                        Q.append(nei)
            print(f"{plant}: {component}")
            plots.append([plant, component])
    print(plots)

    price = 0
    for plant, component in plots:
        area = len(component)
        peri = set()
        for i, j in component:
            for di, dj in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
                i2 = i + di
                j2 = j + dj
                if i2 < 0 or i2 >= idim or j2 < 0 or j2 >= jdim:
                    peri.add(((i, j), (di, dj)))
                    continue
                if grid[i2, j2] != plant:
                    peri.add(((i, j), (di, dj)))
        sides = count_sides(peri)
        print(f"{plant=}, {area=}, {sides=}")
        price += area * sides
    print(price)


def main(inputfile):
    grid = read(inputfile)
    print(grid)

    measure(grid)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
