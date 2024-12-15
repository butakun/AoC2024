import cv2
import numpy as np


class Canvas:
    def __init__(self, D=10):
        self.writer = None
        self.D = D

    def draw_frame(self, grid):
        idim, jdim = grid.shape[:2]
        width, height = jdim * self.D, idim * self.D
        if not self.writer:
            fps = 30
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            self.writer = cv2.VideoWriter("video.mp4", fourcc, fps, (width, height))

        border = [100, 100, 100]
        bg = [0, 0, 0]
        fg = [0x87, 0x92, 0x65]
        image = np.zeros((height, width, 3), dtype=np.uint8)
        image[:, :, :] = bg
        d = self.D
        for i, j in np.stack(np.where(grid == "["), axis=-1):
            i1, j1 = i * d, j * d
            i2, j2 = (i+1) * d, (j+2) * d
            image[i1:i2, j1:j2, :] = fg
            image[i1, j1:j2, :] = border
            image[i2, j1:j2, :] = border
            image[i1:i2, j1, :] = border
            image[i1:i2, j2, :] = border
        for i, j in np.stack(np.where(grid == "#"), axis=-1):
            i1, j1 = i * d, j * d
            i2, j2 = (i+1) * d, (j+1) * d
            image[i1:i2, j1:j2, :] = [50, 50, 50]
            if i > 0 and grid[i-1, j] != "#":
                image[i1, j1:j2] = border
            if i < idim-1 and grid[i+1, j] != "#":
                image[i2, j1:j2] = border
            if j > 0 and grid[i, j-1] != "#":
                image[i1:i2, j1] = border
            if j < jdim-1 and grid[i, j+1] != "#":
                image[i1:i2, j2] = border

        i, j = np.where(grid == "@")
        i, j = i[0], j[0]
        i1, j1 = i * d, j * d
        i2, j2 = (i+1) * d, (j+1) * d
        image[i1:i2, j1:j2, :] = [0x8a, 0x8a, 0xff]

        self.writer.write(image)


