import os
import logging
import numpy as np
import cv2

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)


def read(inputfile):
    pat = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
    robots = [ list(map(int, pat.match(l).groups())) for l in open(inputfile) ]
    robots = [ [[v[0], v[1]], [v[2], v[3]]] for v in robots ]
    return np.array(robots)


def dump(robots, shape):
    grid = np.zeros(shape, dtype=np.uint64)
    for p, _ in robots:
        grid[p[0], p[1]] += 1
    grid = grid[:-1:2,:-1:2] + grid[1::2,1::2]

    grid = grid.astype(np.str_)
    grid[grid == "0"] = "."
    grid = grid.T
    for l in grid:
        print("".join(l))


def draw(robots, shape):
    idim, jdim = shape[:2]
    grid = np.zeros((jdim, idim, 3), dtype=np.uint8)
    for (i, j), _ in robots:
        grid[j, i, :] += 1
    N = np.max(grid)
    grid[:, :, :] = grid[:, :, :] / N * 255
    return grid


def stat(robots, shape):
    p = np.array([p for p, _ in robots])
    return p.mean(axis=0), p.std(axis=0)


def step(robots, shape, t=1):
    robots2 = []
    for robot in robots:
        p, v = robot
        p2 = p + v * t
        p2 = p2 % shape
        robots2.append([p2, v])
    return robots2


def main(inputfile):
    robots = read(inputfile)

    imax, jmax = np.max(robots[:, 0, :], axis=0)
    idim, jdim = imax + 1, jmax + 1
    shape = np.array([idim, jdim])

    mu0, sigma0 = stat(robots, shape)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = 30
    writer = cv2.VideoWriter("video.mp4", fourcc, fps, (idim, jdim))
    grid = draw(robots, shape)
    writer.write(grid)

    t = 1
    while True:
        robots = step(robots, shape)
        mu, sigma = stat(robots, shape)
        print(f"step {t}, {mu=}, {sigma=}")
        grid = draw(robots, shape)
        if t % 60 == 0:
            writer.write(grid)
        if np.all(sigma < 0.7 * sigma0):
            break
        t += 1

    for _ in range(fps):
        writer.write(grid)
    dump(robots, shape)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="input.txt")
    args = parser.parse_args()
    main(args.input)
