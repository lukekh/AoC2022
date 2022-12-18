# AoC :: Day 4
import time
day = 4


# Parse inputs
class Assignment:
    def __init__(self, start, stop):
        self.start = int(start)
        self.stop = int(stop)
    
    def __and__(self, other):
        return Assignment(max(self.start, other.start), min(self.stop, other.stop))
    
    def __le__(self, other):
        return (self.start >= other.start) and (self.stop <= other.stop)

    def __pow__(self, other):
        return (self <= other) or (self >= other)

    def __bool__(self):
        return self.start <= self.stop

    def __str__(self):
        if self:
            return f"A({self.start}, {self.stop})"
        else:
            return "A()"
    
    def __repr__(self):
        return str(self)


def parse(line):
    r1, r2 = line[:-1].split(",")
    return  (Assignment(*r1.split('-')), Assignment(*r2.split('-')))

inputs = [parse(i) for i in open('Day04.in').readlines()]


# part one
def part_one(inputs):
    return len([1 for a1, a2 in inputs if a1 ** a2])

# part two
def part_two(inputs):
    return len([1 for a1, a2 in inputs if a1 & a2])


# run both solutions and print outputs + runtime
def main(inputs):
    print(f":: Advent of Code 2022 -- Day {day} ::")

    # Part One
    print(f":: Part One ::")
    t1 = -time.time()
    a1 = part_one(inputs)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(f":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(inputs)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main(inputs)
