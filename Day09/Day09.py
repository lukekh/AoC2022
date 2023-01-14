# AoC :: Day 9
import time
day = 9


# Parse inputs
inputs = list(map(
    lambda l: (l[0], int(l[1])),
    [i[:-1].split(' ') for i in open('Day09.in').readlines()]
))

def lastzip(*args, default=None):
    args = [iter(arg) for arg in args]
    terminate = [False for _ in args]
    last = [default for _ in args]

    while 1:
        for i, arg in enumerate(args):
            try:
                last[i] = next(arg)
            except StopIteration:
                terminate[i] = True
        if not all(terminate):
            yield tuple(last)
        else:
            return None


class Rope:
    def __init__(self):
        self.Hx, self.Hy = 0, 0
        self.Tx, self.Ty = 0, 0
        self.pts = {(0,0)}
    
    def move(self, direction, magnitude):
        self.Hx += magnitude if direction == "R" else -magnitude if direction == "L" else 0
        self.Hy += magnitude if direction == "U" else -magnitude if direction == "D" else 0
        self.update()

    def update(self):
        dx = 1 if self.Tx <= self.Hx else -1
        dy = 1 if self.Ty <= self.Hy else -1

        Txs = range(self.Tx, self.Hx + dx, dx)
        Tys = range(self.Ty, self.Hy + dy, dy)

        Tpts = [pt for pt in lastzip(Txs, Tys)][:-1]
        if Tpts:
            self.Tx, self.Ty = Tpts[-1]
            self.pts.update(Tpts)

    def quick_move(self, direction, magnitude):
        self.Hx += magnitude if direction == "R" else -magnitude if direction == "L" else 0
        self.Hy += magnitude if direction == "U" else -magnitude if direction == "D" else 0
        self.quick_update()
    
    def quick_update(self):
        dx = 1 if self.Tx <= self.Hx else -1
        dy = 1 if self.Ty <= self.Hy else -1

        Txs = range(self.Tx, self.Hx + dx, dx)
        Tys = range(self.Ty, self.Hy + dy, dy)

        Tpts = [pt for pt in lastzip(Txs, Tys)]
        if len(Tpts) < 2:
            return
        else:
            self.Tx, self.Ty = Tpts[-2]
            return


class Chain:
    def __init__(self, knots):
        self.knots = knots
        self.ropes = [Rope() for _ in range(knots)]
        self.pts = self.ropes[-1].pts
        
    def __getitem__(self, item):
        return self.ropes[item]

    def move(self, direction, magnitude):
        if magnitude > 0:
            self[0].quick_move(direction, 1)
            for i, r in enumerate(self[1:]):
                r.Hx, r.Hy = self[i].Tx, self[i].Ty
                if i < self.knots - 2:
                    r.quick_update()
                else:
                    r.update()
        else:
            return
        self.move(direction, magnitude-1)

        


# part one
def part_one(inputs):
    # init
    r = Rope()
    for direction, magnitude in inputs:
        r.move(direction, magnitude)
    return r


# part two
def part_two(inputs, knots=9):
    # init
    c = Chain(knots)
    for direction, magnitude in inputs:
        c.move(direction, magnitude)
    return c


# run both solutions and print outputs + runtime
def main(inputs):
    print(f":: Advent of Code 2022 -- Day {day} ::")

    # Part One
    print(f":: Part One ::")
    t1 = -time.time()
    r = part_one(inputs)
    t1 += time.time()
    print(f"Answer: {len(r.pts)}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(f":: Part Two ::")
    t2 = -time.time()
    n = 9
    c = part_two(inputs, n)
    t2 += time.time()
    print(f"Answer: {len(c.pts)}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main(inputs)
