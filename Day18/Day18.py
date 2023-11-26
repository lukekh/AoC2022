"""AoC :: Day 18"""
import time
from typing import List
import numpy as np
day = 18


# Parse inputs
def parse(triple: str):
    """turn string 'x,y,z' -> (x, y, z) integer tuple"""
    return tuple([int(x) for x in triple.split(',')])

with open('Day18/Day18.in', encoding="utf8") as f:
    inputs = [parse(i[:-1]) for i in f.readlines()]
    MAX = [max(inputs, key=lambda t: t[i])[i]+1 for i in range(3)]


class Droplet:
    """A collection of coordinates defining a droplet"""
    def __init__(self, coords: List[tuple]):
        self.array = np.full(MAX, fill_value=False, dtype=bool)
        for x, y, z in coords:
            self.array[x, y, z] = True

    @property
    def surface_area(self):
        """The surface area of the droplet"""
        return self._count_x_faces() + self._count_y_faces() + self._count_z_faces()

    def _count_x_faces(self):
        faces = self.array[0, :, :].sum() + self.array[-1, :, :].sum()

        layers = self.array.shape[0]
        for i in range(layers-1):
            s_front = self.array[i, :, :]
            s_back = self.array[i+1, :, :]
            faces += s_back.sum() - (s_front & s_back).sum()
            faces += s_front.sum() - (s_front & s_back).sum()

        return faces

    def _count_y_faces(self):
        faces = self.array[:, 0, :].sum() + self.array[:, -1, :].sum()

        layers = self.array.shape[1]
        for i in range(layers-1):
            s_front = self.array[:, i, :]
            s_back = self.array[:, i+1, :]
            faces += s_back.sum() - (s_front & s_back).sum()
            faces += s_front.sum() - (s_front & s_back).sum()

        return faces

    def _count_z_faces(self):
        faces = self.array[:, :, 0].sum() + self.array[:, :, -1].sum()

        layers = self.array.shape[2]
        for i in range(layers-1):
            s_front = self.array[:, :, i]
            s_back = self.array[:, :, i+1]
            faces += s_back.sum() - (s_front & s_back).sum()
            faces += s_front.sum() - (s_front & s_back).sum()

        return faces

    def flood_fill(self, start=(0, 0, 0)):
        """Embed the droplet in a slightly larger cube and then flood fill around it"""
        # Ensure the droplet isn't touching the edges in a way that prevents
        # a flood fill
        flood_fill = np.full([m+2 for m in MAX], False, dtype=bool)
        new_droplet = np.full([m+2 for m in MAX], False, dtype=bool)
        new_droplet[1:MAX[0]+1, 1:MAX[1]+1, 1:MAX[2]+1] = self.array

        # Make a function that looks at neighbouring pts
        def adjacent(pt: tuple, drop, flood):
            x, y, z = pt
            new_pts = {
                (max(x-1, 0), y, z), (min(x+1, MAX[0]+1), y, z),
                (x, max(y-1, 0), z), (x, min(y+1, MAX[1]+1), z),
                (x, y, max(z-1, 0)), (x, y, min(z+1, MAX[2]+1)),
            }

            remove = {npt for npt in new_pts if drop[npt] or flood[npt]}

            return new_pts - remove

        boundary = {start}
        ctr = 0
        while boundary:
            ctr += 1
            new_boundary = set()
            for pt in boundary:
                flood_fill[pt] = True
            for pt in boundary:
                new_boundary |= adjacent(pt, new_droplet, flood_fill)
            boundary = new_boundary

        self.array = ~flood_fill


# part one
def part_one(args: List[tuple]):
    """Solution to part one"""
    droplet = Droplet(args)
    return droplet.surface_area


# part two
def part_two(args: List[tuple]):
    """Solution to part two"""
    droplet = Droplet(args)
    droplet.flood_fill()
    return droplet.surface_area


# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2022 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(inputs)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(inputs)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
