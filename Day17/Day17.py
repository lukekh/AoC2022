"""AoC :: Day 17"""
import time
# from typing import List
import numpy as np
day = 17

# Constants
CHAMBER_WIDTH = 7
BUFFER_LEFT = 2
BUFFER_HEIGHT = 3

# Make a class for the rock shapes
class Shape:
    """represents a rock shape"""
    def __init__(self, array: np.ndarray, flipped=True):
        self.array = np.flipud(array) if flipped else array
        self.height, self.width = self.array.shape

    def __iter__(self):
        return iter(self.array)

    def __getitem__(self, index):
        return self.array[index]

    def __reversed__(self):
        return reversed(self.array)

    def __eq__(self, other: "Shape"):
        try:
            return bool(np.all(self.array == other.array))
        except AttributeError:
            return False


ROCKS = [
    Shape(np.array([
        [True, True, True, True]
    ])),
    Shape(np.array([
        [False, True, False,],
        [True, True, True,],
        [False, True, False,],
    ])),
    Shape(np.array([
        [False, False, True,],
        [False, False, True,],
        [True, True, True,],
    ])),
    Shape(np.array([
        [True],
        [True],
        [True],
        [True],
    ])),
    Shape(np.array([
        [True, True,],
        [True, True,],
    ])),
]

MAX_HEIGHT = max([rock.height for rock in ROCKS])

# Parse inputs
def parse(instruction: str):
    """convert > into right and < into left"""
    if instruction == ">":
        return 1
    elif instruction == "<":
        return -1
    else:
        raise ValueError(f"instruction '{instruction}' is unhandled in parse function")

def clamp(lb: int, ub: int):
    """a clamp function to the lower and upper bounds"""
    def func(x: int):
        return max(min(x, ub), lb)

    return func

class InfiniteLoop:
    """Never ending loop over a list"""
    def __init__(self, items, ):
        self.items = items
        self.len = len(items)
        self.pos = 0

    def __iter__(self):
        return self

    def __next__(self):
        val = self.items[self.pos]
        self.pos += 1
        self.pos %= self.len

        return val


with open('Day17/Day17.in', encoding="utf8") as f:
    inputs = list(map(parse, f.read()[:-1]))

class LookUp:
    """Keep track of state"""
    def __init__(self, rocks: InfiniteLoop, instructions: InfiniteLoop):
        self.rocks = rocks
        self.instructions = instructions

        # self.table[rock_id][instruction_id] will give you an x position
        # If these begin repeating we've reached a cycle
        # Init with self.table[rock_id][instruction_id] = None
        self.table = {
            i: {j: None for j in range(len(instructions.items))} for i in range(len(rocks.items))
        }

        # Don't init all (rock, instruction) pairs as False since some
        # combinations may never appear
        self.checks = {
            i: {} for i in range(len(rocks.items))
        }
        self.ctr = 0
        self.height = None

    def cyclic(self):
        """Check if a cycle has been detected"""
        cyclic = True
        for instruction_dict in self.checks.values():
            cyclic &= all(instruction_dict.values())

        return cyclic

    def record(self, x, tower: "Tower"):
        """Record the behaviour to check if it's cyclic"""
        i, j = self.rocks.pos, self.instructions.pos
        val = self.table[i][j]
        self.table[i][j] = x

        if val == x:
            self.checks[i][j] = True
            self.ctr += 1
            # print(f"rock {i}: instruction {j}:: landing in the same spot {x}")
        else:
            self.checks[i][j] = False
            # if self.ctr != 0:
            #     print(f"before: ctr = {self.ctr}, instruction_id = {self.instructions.pos}")
            self.ctr = 0
            self.height = len(tower.tower)
            # if self.ctr != 0:
            #     print(f"after:  ctr = {self.ctr}")


class Tower:
    """represents the tower of rocks in the chamber"""
    def __init__(self, width=CHAMBER_WIDTH):
        self.width = width
        self.tower = np.array([[True for _ in range(width)]])

        self.memory = {}

    def lock(self, shape: Shape, x: int, y: int):
        """lock a shape in the tower"""
        height = len(self.tower)
        new_rows = y + shape.height - height
        if new_rows > 0:
            self.tower = np.vstack([
                self.tower,
                np.array([[False for _ in range(self.width)] for _ in range(new_rows)])
            ])

        self.tower[y:y+shape.height, x:x+shape.width] |= shape.array

    def cyclic(self):
        """detect a cycle"""

    def test_step(self, shape: Shape, y: int, x: int, x_new: int):
        """
        return a pair of booleans that indicate movement
        
        The first bool indicates whether the shape moves left/right and
        then second bool indicates whether it falls or comes to rest
        """
        # Test move
        rows = self.tower[y:y+shape.height, :]
        if x != x_new:
            no_move = False
            for row, line in zip(rows, shape):
                no_move |= (row[x_new:x_new+shape.width] & line).any()
            if not no_move:
                x = x_new
        else:
            no_move = True

        # Test fall
        rows = self.tower[y-1:y+shape.height-1, :]
        no_fall = False
        for row, line in zip(rows, shape):
            no_fall |= (row[x:x+shape.width] & line).any()
        return not no_move, not no_fall

    def drop(self, shape: Shape, instructions):
        """drop a shape"""
        # x, y represent the bottom left corner of the bounding box of the shape
        # n.b that 0 <= x <= CHAMBER_WIDTH - shape.width
        x = BUFFER_LEFT
        x_max = CHAMBER_WIDTH - shape.width
        y =  len(self.tower) + BUFFER_HEIGHT

        # Clamp function
        c = clamp(0, x_max)

        for instruction in instructions:
            x_new = c(x + instruction)
            move, fall = self.test_step(shape, y, x, x_new)
            # Does shape move
            if move:
                x = x_new
            # Does shape fall
            if fall:
                y -= 1
            else:
                break

        self.lock(shape, x, y)

    def drop_pt2(self, shape: Shape, instructions, lookup: LookUp):
        """drop a shape and save in lookup table"""
        # x, y represent the bottom left corner of the bounding box of the shape
        # n.b that 0 <= x <= CHAMBER_WIDTH - shape.width
        x = BUFFER_LEFT
        x_max = CHAMBER_WIDTH - shape.width
        y =  len(self.tower) + BUFFER_HEIGHT

        # Clamp function
        c = clamp(0, x_max)

        for instruction in instructions:
            x_new = c(x + instruction)
            move, fall = self.test_step(shape, y, x, x_new)
            # Does shape move
            if move:
                x = x_new
            # Does shape fall
            if fall:
                y -= 1
            else:
                break

        self.lock(shape, x, y)
        lookup.record(x, self)

    def print(self):
        """print"""
        for row in reversed(self.tower):
            print('|' + ''.join(["#" if r else "." for r in row]) + '|')


# part one
def part_one(args, N=2022):
    """Solution to part one"""
    t = Tower()
    instructions = InfiniteLoop(args)
    rocks = InfiniteLoop(ROCKS)

    for n, rock in enumerate(rocks):
        if n >= N:
            break
        t.drop(rock, instructions)

    return len(t.tower) - 1

def part_two(args, N=1_000_000_000_000):
    """Solution to part two"""
    t = Tower()
    instructions = InfiniteLoop(args)
    rocks = InfiniteLoop(ROCKS)
    lookup = LookUp(rocks, instructions)
    reset_lookup = True
    look_for_cycle = True
    cycle_height = None

    for n, rock in enumerate(rocks):
        if (n >= len(args)) & reset_lookup:
            print("resetting lookup")
            reset_lookup = False
            lookup = LookUp(rocks, instructions)
        if n >= N:
            break
        t.drop_pt2(rock, instructions, lookup)
        if look_for_cycle and lookup.cyclic():
            h = len(t.tower) - lookup.height
            n_cycles = (N - n)//lookup.ctr
            cycle_height = h * n_cycles
            N -= n_cycles * lookup.ctr
            look_for_cycle = False

    return len(t.tower) - 1 + cycle_height


# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2022 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(inputs, 2022)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(inputs, 1_000_000_000_000)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
