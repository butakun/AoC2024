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

def measure_old(grid):
    plants = np.unique(grid)
    idim, jdim = grid.shape

    price = 0
    for plant in plants:
        area = np.sum(grid == plant)

        peri = 0
        for i in range(idim):
            for j in range(jdim):
                if grid[i, j] != plant:
                    continue
                for di, dj in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
                    i2 = i + di
                    j2 = j + dj
                    if i2 < 0 or i2 >= idim or j2 < 0 or j2 >= jdim:
                        peri += 1
                    elif grid[i2, j2] != plant:
                        peri += 1
        print(f"{plant}: {area=}, {peri=}")
        price += area * peri
    print(price)

def measure(grid):
    plants = np.unique(grid)
    idim, jdim = grid.shape

    G = defaultdict(set)
    for plant in plants:
        Q = np.stack(np.where(grid == plant), axis=-1).tolist()
        print(f"{plant}: {Q}")

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
        peri = 0
        for i, j in component:
            for di, dj in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
                i2 = i + di
                j2 = j + dj
                if i2 < 0 or i2 >= idim or j2 < 0 or j2 >= jdim:
                    peri += 1
                    continue
                if grid[i2, j2] != plant:
                    peri += 1
        print(f"{plant=}, {area=}, {peri=}")
        price += area * peri
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
