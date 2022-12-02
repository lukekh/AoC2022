# Day02
import time
day = 2
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

# Main
def main(inputs):
    print(f":: Solutions to Day {day} ::")
    
    # Part One
    print(f":: Part One ::")
    print(f"Your score would be {part_one(inputs)} if everything goes to plan.")

    # Part Two
    print(f":: Part Two ::")
    print(f"Your score would be {part_two(inputs)} if everything goes to the strategy guide.")


# Run main
if __name__ == "__main__":
    t = time.time()
    main(inputs)
    print(f":: Finished in {time.time() - t: .4f} seconds ::")
