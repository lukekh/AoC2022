"""AoC :: Day 21"""
from dataclasses import dataclass
from typing import Literal, Union
import time
day = 21

class Monkey:
    """Yells a number or calculates a number based on an operation"""
    MONKEYS: dict[str, "Monkey"] = dict()

    def __init__(self, name: str, instruction: Union[int, "Operation"]):
        self.name = name
        self.instruction = instruction
        self.MONKEYS[name] = self

    def yell(self) -> int:
        """Monkey yells an operation"""
        match self.instruction:
            case int():
                return self.instruction
            case Operation():
                if isinstance(self.instruction.left, int):
                    left = self.instruction.left
                else:
                    left = self.MONKEYS[self.instruction.left].yell()
                if isinstance(self.instruction.right, int):
                    right = self.instruction.right
                else:
                    right = self.MONKEYS[self.instruction.right].yell()

                match self.instruction.operation:
                    case "+":
                        return left + right
                    case "-":
                        return left - right
                    case "*":
                        return left * right
                    case "/":
                        return left / right

@dataclass
class Operation:
    """A job for a Monkey to perform"""
    left: str | int
    right: str | int
    operation: Literal["+", "-", "*", "/"]



# Parse inputs
def tryint(s: str):
    """try to process the number as an int, otherwise return the string"""
    try:
        return int(s)
    except ValueError:
        return s

with open('Day21.in', encoding="utf8") as f:
    for i in f.readlines():
        n, rest = i[:-1].split(": ")
        rest = rest.split(" ")
        if len(rest) == 1:
            Monkey(n, int(rest[0]))
        else:
            l, op, r = rest
            Monkey(n, Operation(tryint(l), tryint(r), op))

# part one
def part_one():
    """Solution to part one"""
    return int(Monkey.MONKEYS["root"].yell())


# part two
def sign_change(n1, n2):
    """Check if two numbers have a different sign"""
    if n1 > 0:
        return n2 <= 0
    return n2 > 0

def part_two():
    """Solution to part two"""
    root = Monkey.MONKEYS["root"]
    root.instruction.operation = "-"
    humn = Monkey.MONKEYS["humn"]
    low = humn.instruction = 1
    init = root.yell()

    # Get the two bounds
    while not sign_change(init, root.yell()):
        low = humn.instruction
        humn.instruction *= 2

    # Binary search
    high = humn.instruction
    while root.yell():
        mid = (low + high)//2
        humn.instruction = mid
        new_val = root.yell()
        if not sign_change(init, new_val):
            low = mid
        else:
            high = mid

    return humn.instruction


# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2022 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one()
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two()
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
