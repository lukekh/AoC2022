# AoC :: Day 3
import time
day = 3


# Parse inputs
inputs = [i[:-1] for i in open('Day03.in').readlines()]
test = [
    "vJrwpWtwJgWrhcsFMMfFFhFp",
    "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
    "PmmdzqPrVvPwwTWBwg",
    "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
    "ttgJtRGJQctTZtZT",
    "CrZsJsPPZsGzwwsLwLmpwMDw",
]

# helper functions
priority = lambda letter: i - 64 + 26 if (i:=ord(letter)) < 97 else (i - 96)
compartments = lambda rucksack: (rucksack[:(split:=len(rucksack)//2)], rucksack[split:])

# part one
def part_one(inputs):
    repeats = [
        priority(list(set(c1) & set(c2))[0]) for c1, c2 in [compartments(i) for i in inputs]
    ]
    return sum(repeats)


# part two
def part_two(inputs):
    
    badge = lambda i, r=inputs: list(set(r[i]) & set(r[i + 1]) & set(r[i + 2]))[0]

    badges = [
        priority(badge(i*3)) for i in range(len(inputs)//3)
    ]

    return sum(badges)


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
