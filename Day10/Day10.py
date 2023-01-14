# AoC :: Day 10
import time
day = 10


# Parse inputs
inputs = list(map(
    lambda l: (l[0], int(l[1])) if len(l) > 1 else (l[0], None),
    [i[:-1].split(' ') for i in open('Day10.in').readlines()]
))

# utils
class CPU:
    def __init__(self, X=1, cycle=0, interrogate=None):
        self.X = X
        self.cycle = 0
        self.interrogate = {} if interrogate is None else {i: None for i in interrogate}
        self.display = []
    
    def parse(self, instruction, arg=None):
        if instruction == "addx":
            self.addx(arg)
        elif instruction == "noop":
            self.noop()
        else:
            raise Exception(f"no way of handling {instruction} instructions")

    def addx(self, V):

        self.noop()
        self.noop()

        self.X += V
    
    def noop(self):
        self.draw()

        self.cycle += 1
        self.interrogation()
    
    def interrogation(self):
        if (self.cycle in self.interrogate):
            self.interrogate[self.cycle] = self.X

    def signal_strengths(self):
        return sum([i*self.interrogate[i] for i in self.interrogate])
    
    def draw(self):
        sprite = (self.X-1, self.X, self.X+1)
        if (self.cycle % 40) in sprite:
            self.display.append('#')
        else:
            self.display.append(' ')
    
    def print(self):
        lines = [self.display[40*i:40*i+39] for i in range(6)]
        return '\n'.join([''.join(line) for line in lines])

# part one
def part_one(inputs, interrogate=(20, 60, 100, 140, 180, 220), X=1, cycle=0):
    # init
    cpu = CPU(X, cycle, interrogate=interrogate)
    for i, v in inputs:
        cpu.parse(i, v)
    return cpu


# part two
def part_two(inputs):
    # init
    ans = 0
    return ans


# run both solutions and print outputs + runtime
def main(inputs):
    print(f":: Advent of Code 2022 -- Day {day} ::")

    # Part One
    print(f":: Part One ::")
    t1 = -time.time()
    cpu = part_one(inputs)
    t1 += time.time()
    print(f"Answer: {cpu.signal_strengths()}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(f":: Part Two ::")
    t2 = -time.time()
    print(f"Answer:\n{cpu.print()}")
    t2 += time.time()
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main(inputs)
