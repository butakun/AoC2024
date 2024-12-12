import os
import logging
import numpy as np
from collections import defaultdict
from itertools import combinations
import cv2

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


def gather_sides(peri):
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

    return components


def color_plants(grid, plots):
    level = lambda i: 150 + 100 // 3 * i
    palette = [ (level(i), level(j), level(k)) for i in range(4) for j in range(4) for k in range(4) ]
    plants = [ str(c) for c in np.unique(grid) ]
    colors = { p: palette[i] for i, p in enumerate(plants) }
    return colors


class Canvas:
    def __init__(self, grid, plots):
        idim, jdim = grid.shape[:2]
        plants = set([ p for p, _, _ in plots ])
        colors = color_plants(grid, plots)

        d = 6
        t = 2
        width = jdim * d
        height = idim * d
        background = np.ones((height, width, 3), dtype=np.uint8)

        for i in range(idim):
            for j in range(jdim):
                color = colors[str(grid[i, j])]
                background[d * i: d * (i + 1), d * j: d * (j + 1), :] = color
        self.d = d
        self.t = t
        self.width = width
        self.height = height
        self.background = background
        self.frame = background.copy()

    def step(self, side):
        t = self.t
        d = self.d
        n = side[0][1]
        for (i, j), (di, dj) in side:
            assert di == n[0] and dj == n[1]
            if di == 0:
                ei1 = d * i
                ei2 = d * (i + 1)
                if dj == -1:
                    ej1 = d * j
                    ej2 = ej1 + t
                elif dj == 1:
                    ej1 = d * (j + 1)
                    ej2 = ej1 + t
                else:
                    raise ValueError
            if dj == 0:
                ej1 = d * j
                ej2 = d * (j + 1)
                if di == -1:
                    ei1 = d * i
                    ei2 = ei1 + t
                elif di == 1:
                    ei1 = d * (i + 1)
                    ei2 = ei1 + t
                else:
                    raise ValueError
            self.frame[ei1:ei2, ej1:ej2, :] = 0



def main(inputfile):
    grid = read(inputfile)
    idim, jdim = grid.shape

    G = make_plant_graph(grid)
    logger.debug(f"{G=}")

    def new_plot(component):
        anchor = component[0]
        plant = str(grid[anchor[0], anchor[1]])
        logger.info(f"new plot {plant}: {component}")
        return [plant, component, None]

    plots = connected_components(G, new_plot)

    for plot in plots:
        plant, component, _ = plot
        area = len(component)
        peri = set()
        for i, j in component:
            for di, dj in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
                i2 = i + di
                j2 = j + dj
                if (i2 < 0 or i2 >= idim or j2 < 0 or j2 >= jdim) or grid[i2, j2] != plant:
                    peri.add(((i, j), (di, dj)))
        plot[2] = peri

    canvas = Canvas(grid, plots)
    print(f"{canvas.width=}, {canvas.height=}")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter("video.mp4", fourcc, 30.0, (canvas.width, canvas.height))

    for plant, component, peri in plots:
        sides = gather_sides(peri)
        for side in sides:
            canvas.step(side)
        #cv2.imwrite(f"frame.{iframe:05d}.png", canvas.frame)
        #iframe += 1
        writer.write(canvas.frame)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
