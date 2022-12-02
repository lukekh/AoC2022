# Day01
import time
day = 1
inputs = [i[:-1] for i in open('Day01.in').readlines()]


# Part One
def part_one(inputs):
    # init
    max_calories = 0
    elf = 0
    total = 0

    # iterate over inputs
    for row in inputs:
        if row:
            total += int(row)
        else:
            # update max
            max_calories = max(max_calories, total)
            max_elf = elf

            # init next elf
            elf += 1
            total = 0
    return max_calories, max_elf


# Part Two
def part_two(inputs):
    # init
    calories = []
    total = 0

    # iterate over inputs
    for row in inputs:
        if row:
            total += int(row)
        else:
            # update max
            calories.append(total)

            # init next elf
            total = 0
    return sorted(calories)[-3:]


# Main
def main(inputs):
    print(f":: Solutions to Day {day} ::")
    
    # Part One
    print(f":: Part One ::")
    c, e = part_one(inputs)
    print(f"Elf {e} is carrying {c} total calories.")

    # Part Two
    print(f":: Part Two ::")
    c = part_two(inputs)
    print(f"The top three calorie counts are {', '.join([str(i) for i in c])} hence the total is {sum(c)} calories.")


# Run main
if __name__ == "__main__":
    t = time.time()
    main(inputs)
    print(f":: Finished in {time.time() - t: .4f} seconds ::")

