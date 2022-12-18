# AoC :: Day 6
import time
from collections import deque
day = 6


# Parse inputs
inputs = open('Day06.in').read()

# utils
def start_of_packet_scan(string, chars=4):
    d = deque(string[:chars])
    for i, char in enumerate(string[chars:]):
        d.popleft()
        d.append(char)
        if len(set(d)) == chars:
            return ''.join(d), i + chars + 1
    raise Exception("No start of packet/message detected")


# part one
def part_one(inputs):
    return start_of_packet_scan(inputs)


# part two
def part_two(inputs):
    return start_of_packet_scan(inputs, chars=14)


# run both solutions and print outputs + runtime
def main(inputs):
    print(f":: Advent of Code 2022 -- Day {day} ::")

    # Part One
    print(f":: Part One ::")
    t1 = -time.time()
    sop, i = part_one(inputs)
    t1 += time.time()
    print(f"Start of packet {sop} appears after character {i}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(f":: Part Two ::")
    t2 = -time.time()
    som, j = part_two(inputs)
    t2 += time.time()
    print(f"Start of message {som} appears after character {j}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main(inputs)
