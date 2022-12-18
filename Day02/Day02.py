# AoC :: Day 2
import time
day = 2

# Parse inputs
inputs = [i[:-1].split(" ") for i in open('Day02.in').readlines()]


# Helper functions
score_modifier = {
    "X": 1,
    "Y": 2,
    "Z": 3,
}

def rps(p1, p2, modifier=score_modifier):
    lose = [("A", "Z"), ("B", "X"), ("C", "Y"),]
    draw = [("A", "X"), ("B", "Y"), ("C", "Z"),]
    if (p1, p2) in lose:
        return 0 + modifier[p2]
    elif (p1, p2) in draw:
        return 3 + modifier[p2]
    else:
        return 6 + modifier[p2]


# Part One
def part_one(inputs):
    return sum(
        [rps(*i) for i in inputs]
    )

def strat(p1, result):
    modifier = {"A": 1, "B": 2, "C": 3}
    plays = {
        "X": {"A": "C", "B": "A", "C": "B"},
        "Y": {"A": "A", "B": "B", "C": "C"},
        "Z": {"A": "B", "B": "C", "C": "A"},
    }
    results = {"X": 0, "Y": 3, "Z": 6}

    return results[result] + modifier[plays[result][p1]]

# Part Two
def part_two(inputs):
    return sum(
        [strat(*i) for i in inputs]
    )


# run both solutions and print outputs + runtime
def main(inputs):
    print(f":: Advent of Code 2022 -- Day {day} ::")

    # Part One
    print(f":: Part One ::")
    t1 = -time.time()
    a1 = part_one(inputs)
    t1 += time.time()
    print(f"Your score would be {a1} if everything goes to plan.")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(f":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(inputs)
    t2 += time.time()
    print(f"Your score would be {a2} if everything goes to the strategy guide.")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main(inputs)
