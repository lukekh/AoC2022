# AoC :: Day 5
import time
from collections import deque
day = 5


# Parse inputs
inputs = open('Day05.in').read()

# utils
def parse_stacks(text):
    lines = text.split('\n')
    stack_locs = [(idx, int(n)) for idx, n in enumerate(lines[-1]) if n != " "]
    stacks = {n: deque() for (_, n) in stack_locs}

    for line in reversed(lines[:-1]):
        for (idx, n) in stack_locs:
            if (char := line[idx]) != " ":
                stacks[n].append(char)
    
    return stacks

def parse_move(move):
    return [int(n) for idx, n in enumerate(move.split(" ")) if idx in (1, 3, 5)]

# move m boxes (one-by-one from stack i to stack j)
def move(stacks, m, i, j):
    stacks[j].extend(
        stacks[i].pop() for _ in range(m)
    )

def move9001(stacks, m, i, j):
    stacks[j].extend(
        reversed([stacks[i].pop() for _ in range(m)])
    )

# part one
def part_one(initial_state, instructions, move_fn):
    # parse stacks
    stacks = parse_stacks(initial_state)
    for i in instructions.split('\n')[:-1]:
        move_fn(stacks, *parse_move(i))
    
    # init ans string
    ans = ""
    for n in (range(1, max(stacks)+1)):
        ans += stacks[n].pop()
    return ans


# run both solutions and print outputs + runtime
def main(inputs):
    print(f":: Advent of Code 2022 -- Day {day} ::")

    # Parse inputs
    initial_state_raw, moves_raw = inputs.split('\n\n')

    # Part One
    print(f":: Part One ::")
    t1 = -time.time()
    a1 = part_one(initial_state_raw, moves_raw, move)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(f":: Part Two ::")
    t2 = -time.time()
    # part_one will also solve part two
    a2 = part_one(initial_state_raw, moves_raw, move9001)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main(inputs)
