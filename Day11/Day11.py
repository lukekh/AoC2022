# AoC :: Day 11
from collections import deque
import re
import time
day = 11


# Parse inputs
re_title = r"Monkey (\d+):\n"
re_items = r"\s+Starting items: ((?:\d+,? ?)+)\n"
re_operation = r"\s+Operation: new = ([\w \+*]+)\n"
re_condition = r"\s+If (?:true|false): throw to monkey (\d+)\n"
re_test = f"\s+Test: divisible by (\d+)\n{re_condition*2}"
monkey_template = re_title + re_items + re_operation + re_test

parse = lambda t: (
    int(t[0]),
    deque(int(i) for i in t[1].split(', ')),
    t[2],
    int(t[3]),
    int(t[4]),
    int(t[5]),
)

class Monkey:
    def __init__(self, items, operation, condition, true, false):
        self.items = items
        self.operation = operation
        self.condition = condition
        self.true = true
        self.false = false
        self.panic_level = None

        self.inspection_count = 0
    
    def conditional(self, arg):
        return self.false if arg % self.condition else self.true
    
    def inspect(self, old):
        self.inspection_count += 1
        new = eval(self.operation)

        return new//3

    def panic(self, old):
        self.inspection_count += 1
        return eval(self.operation) % self.panic_level
    
    def __repr__(self):
        return f"Monkey({self.items}, {self.operation}, {self.condition}: {self.true}/{self.false})"
    
    def append(self, item):
        self.items.append(item)

    def turn(self, monkeys):
        while self.items:
            item = self.items.popleft()
            worry = self.inspect(item)
            m = self.conditional(worry)
            monkeys[m].append(worry)
    
    def turn2(self, monkeys):
        while self.items:
            item = self.items.popleft()
            worry = self.panic(item)
            m = self.conditional(worry)
            monkeys[m].append(worry)


inputs = lambda: {i: Monkey(*args) for i, *args in [parse(m) for m in re.findall(monkey_template, open('Day11.in').read())]}


# part one
def part_one(inputs, rounds=20):
    for _ in range(rounds):
        for monkey in inputs.values():
            monkey.turn(inputs)

    return int.__mul__(*sorted([m.inspection_count for m in inputs.values()])[-2:])


# part two
def part_two(inputs, rounds=10_000):
    product = lambda p=1, *args: args and product(p*args[0], *args[1:]) or p
    panic_level = product(*[m.condition for m in inputs.values()])

    # Add panic level
    for monkey in inputs.values():
        monkey.panic_level = panic_level
    
    for _ in range(rounds):
        for monkey in inputs.values():
            monkey.turn2(inputs)

    return int.__mul__(*sorted([m.inspection_count for m in inputs.values()])[-2:])


# run both solutions and print outputs + runtime
def main(inputs):
    print(f":: Advent of Code 2022 -- Day {day} ::")

    # Part One
    print(f":: Part One ::")
    t1 = -time.time()
    a1 = part_one(inputs())
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(f":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(inputs())
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main(inputs)
