"""AoC :: Day 20"""
import time
from dataclasses import dataclass
day = 20

@dataclass
class Number:
    """A number in a linked list with references to the previous and next element"""
    id: int
    val: int
    prev: int
    next: int

    _init_id: int

    def step(self, n: int, file: dict[int, "Number"]) -> "Number":
        """return the next number n steps away"""
        n = n % (N - 1)
        return self.step_no_modulo(n, file)

    def reset(self, decryption_key: int):
        """reset for part two"""
        self.id = self._init_id
        self.prev = (self._init_id - 1) % N
        self.next = (self._init_id + 1) % N
        self.val *= decryption_key

    def step_no_modulo(self, n: int, file: dict[int, "Number"]) -> "Number":
        """do step without modulo calc"""
        if n == 0:
            return self

        num = self
        for _ in range(n):
            num = file[num.next]
        return num

    def shift(self, file: dict[int, "Number"]):
        """shift a number n along"""
        if self.val % (N - 1) != 0:
            child = file[self.prev]
            parent = file[self.next]
            new_child = self.step(self.val, file)
            new_parent = file[new_child.next]

            # lift from current position
            child.next = parent.id
            parent.prev = child.id

            # shift to new position
            new_child.next = self.id
            self.prev = new_child.id
            self.next = new_parent.id
            new_parent.prev = self.id

# Parse inputs
with open('Day20.in', encoding="utf8") as f:
    FILE = {n: Number(n, int(i[:-1]), n-1, n+1, n) for n, i in enumerate(f.readlines())}
    N = len(FILE)
    FILE[0].prev = N - 1
    FILE[N - 1].next = 0
    INIT = list(FILE.values())
    ZERO = None
    for i in INIT:
        if i.val == 0:
            ZERO = i
            break
    else:
        raise ValueError("No zero value in inputs")
    N = len(INIT)

# part one
def part_one(numbers: list[Number], file: dict[int, Number]):
    """Solution to part one"""
    for n in numbers:
        n.shift(file)

    grove_numbers = []
    z: Number = ZERO
    for _ in range(3):
        z = z.step(1000, file)
        grove_numbers.append(z.val)
    return sum(grove_numbers)


# part two
def part_two(numbers: list[Number], file: dict[int, Number], decryption_key: int = 811589153):
    """Solution to part two"""
    for n in numbers:
        n.reset(decryption_key)

    for _ in range(10):
        for n in numbers:
            n.shift(file)

    grove_numbers = []
    z: Number = ZERO
    for _ in range(3):
        z = z.step(1000, file)
        grove_numbers.append(z.val)
    return sum(grove_numbers)


# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2022 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(INIT, FILE)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(INIT, FILE)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
