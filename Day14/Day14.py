# AoC :: Day 14
import time
from math import log, ceil
from collections import defaultdict
day = 14

# Create a cave class
class Lattice:
    def __init__(self, pairs=None):
        if pairs is None:
            pairs = []
        
        self.x = defaultdict(set)
        self.y = defaultdict(set)

        for px, py in pairs:
            self.x[px].add(py)
            self.y[py].add(px)
    
    def __getitem__(self, px, py):
        """Indicate whether (px, py) is in Lattice"""
        return True if (px in self.x) and (py in self.y) else False

    def __delitem__(self, px, py):
        """delete (px, py) from Lattice"""
        if (px in self.x) and (py in self.y):
            self.x[px].remove(py)
            self.y[py].remove(px)
        else:
            raise KeyError(px, py)
    
    def __contains__(self, item):
        px, py = item
        if px in self.x:
            if py in self.x[px]:
                return True
        return False

    def copy(self):
        pairs = []
        for px in self.x:
            for py in self.x[px]:
                pairs.append((px, py))
        
        return Lattice(pairs)
    
    def add(self, px, py):
        """add (px, py) to the Lattice"""
        self.x[px].add(py)
        self.y[py].add(px)
    
    def __or__(self, other):
        pairs = []
        for px in (set(self.x) | set(other.x)):
            for py in (self.x[px] | other.x[px]):
                pairs.append((px, py))
        
        return Lattice(pairs)

    def __and__(self, other):
        pairs = []
        for px in self.x:
            for py in (self.x[px] & other.x[px]):
                pairs.append((px, py))
        
        return Lattice(pairs)

    def __sub__(self, other):
        pairs = []
        for px in self.x:
            for py in (self.x[px] - other.x[px]):
                pairs.append((px, py))
        
        return Lattice(pairs)

    def __len__(self):
        l = 0
        for px in self.x:
            l += len(self.x[px])
        return l
    
    def next_y(self, px, py, floor=None):
        """returns the y coordinate one less than the next py in the Lattice given a px"""
        y = max(self.y) + 1
        found = False

        for ny in self.x[px]:
            if (ny > py) and (ny < y):
                y = ny
                found = True
            else:
                continue
        
        if found:
            return y
        else:
            return floor

    
def print_ASCII_map(rocks, sand, filename=None, floor=None):
    (mx, Mx) = min(sand.x) - 2, max(sand.x) + 2
    (my, My) = min(sand.y) - 2, floor + 2 if floor else max(sand.y) + 2

    xdigits = ceil(log(Mx + 1, 10))
    ydigits = ceil(log(My + 1, 10))

    a = []

    for i in reversed(range(0, xdigits)):
        s = " "*(ydigits + 2)
        for x in range(mx, Mx + 1):
            digit = (x % 10**(i + 1)) // 10**i
            s += f"{digit}"
        a.append(s)

    for y in range(my, My + 1):
        s = f"{y}".ljust(ydigits + 2)
        for x in range(mx, Mx + 1):
            s += "#" if (x, y) in rocks else "#" if y == floor else "O" if (x, y) in sand else "."
        a.append(s)
    
    s = "\n".join(a)

    if filename is None:
        print(s)
    else:
        with open(filename, "w+") as f:
            print(s, file=f)


class AbyssException(Exception):
    """An error if sand flows into the abyss"""
    pass


class BlockedException(Exception):
    """An error if the place the sand is flowing from becomes blocked"""
    pass


class Cave:
    def __init__(self, rocks, sand=None):
        self.rocks = Lattice(rocks)
        # Note, sand contains rocks too and is only a separate object so that the initial rock formation is stored
        self.sand = self.rocks | Lattice(sand) if sand is not None else self.rocks.copy()

    def __contains__(self, item):
        return item in self.sand
    
    def count_sand(self):
        return len(self.sand - self.rocks)
    
    def add(self, px, py):
        self.sand.add(px, py)

    def drop_sand(self, px=500, py=0, floor=None):
        # y is the position of the grain of sand before it goes left, right or settles
        y = self.sand.next_y(px, py, floor=floor)

        if y is None:
            raise AbyssException(f"The grain was last spotted at {(px, py)} before falling into the abyss")
        else:
            # Detect floor state
            y -= 1
            floor_state = self.floor_state(px, y, floor=floor)
            if floor_state == 0:
                self.add(px, y)
                # print(f"landed: {(px, y)}")
            else:
                self.drop_sand(px + floor_state, y, floor=floor)

    def floor_state(self, px, py, floor=None):
        """
        return -1 if it goes to the left, +1 if it goes to the right else 0
        
        this method presumes that (px, py+1) is either rock or sand
        """
        if py + 1 == floor:
            return 0
        if (px - 1, py + 1) not in self:
            return -1
        elif (px + 1, py + 1) not in self:
            return +1
        else:
            return 0

# Parse inputs
def parse_path(string):
    coords = [tuple(int(x) for x in i.split(',')) for i in string.split(' -> ')]
    return coords

inputs = [parse_path(i[:-1]) for i in open('Day14.in').readlines()]

def line_to_set(start, end):
    x1, y1 = min(start[0], end[0]), min(start[1], end[1])
    x2, y2 = max(start[0], end[0]), max(start[1], end[1])
    if x1 == x2:
        return {(x1, y) for y in range(y1, y2+1)}
    elif y1 == y2:
        return {(x, y1) for x in range(x1, x2+1)}
    else:
        raise Exception(f"path {start} -> {end} is invalid")

def path_to_set(path):
    s = set()
    for start, end in zip(path[:-1], path[1:]):
        s |= line_to_set(start, end)
    
    return s

def paths_to_set(paths):
    s = set()
    for path in paths:
        s |= path_to_set(path)
    
    return s


# part one
def part_one(cave, sand_init = (500, 0)):
    # Print initial rock formation
    print_ASCII_map(cave.rocks, cave.sand, "map1_start.txt")
    
    while True:
        try:
            cave.drop_sand(*sand_init)
        except AbyssException:
            break
        
    print_ASCII_map(cave.rocks, cave.sand, "map1_end.txt")

    return cave.count_sand()


# part two
def part_two(cave, sand_init = (500, 0)):
    # init
    floor = max(cave.rocks.y) + 2
    print_ASCII_map(cave.rocks, cave.sand, "map2_start.txt", floor=floor)
    
    while sand_init not in cave:
        try:
            cave.drop_sand(*sand_init, floor=floor)
        except AbyssException:
            break
    
    print_ASCII_map(cave.rocks, cave.sand, "map2_end.txt", floor=floor)

    return cave.count_sand()


# run both solutions and print outputs + runtime
def main(inputs):
    print(f":: Advent of Code 2022 -- Day {day} ::")

    # Part One
    print(f":: Part One ::")
    t1 = -time.time()
    cave = Cave(paths_to_set(inputs))
    a1 = part_one(cave)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(f":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(cave)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main(inputs)
