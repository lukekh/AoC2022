# AoC :: Day 8
import time
day = 8


# Parse inputs
inputs = [[int(j) for j in i[:-1]] for i in open('Day08.in').readlines()]

# Utils
class Grid:
    def __init__(self, values):
        for prev, row in zip(values, values[1:]):
            assert len(prev) == len(row), "All rows in values must be the same length"

        self.values = values
        self.nrows = len(values)
        self.ncols = len(prev)
    
    def __getitem__(self, item):
        rows, columns = item
        if isinstance(rows, int):
            return self.values[rows][columns]
        else:
            return [
                row[columns] for row in self.values[rows]
            ]
    
    def __setitem__(self, item, value):
        row, col = item
        self.values[row, col] = value
    
    def __iter__(self):
        return self.values.__iter__()
    
    def visible_row(self, row):
        heights = list(enumerate(self[row,:]))
        idxs = set()
        max_height = -1
        max_idx = -1
        for i, h in heights:
            if h > max_height:
                max_height = h
                max_idx = i
                idxs.add((row, i))
        
        right_max = -1
        for i, h in heights[:max_idx:-1]:
            if h > right_max:
                right_max = h
                idxs.add((row, i))
        return idxs
    
    def visible_col(self, col):
        heights = list(enumerate(self[:,col]))
        idxs = set()
        max_height = -1
        max_idx = -1
        for i, h in heights:
            if h > max_height:
                max_height = h
                max_idx = i
                idxs.add((i, col))
        
        bottom_max = -1
        for i, h in heights[:max_idx:-1]:
            if h > bottom_max:
                bottom_max = h
                idxs.add((i, col))
        return idxs
    
    def score(self, item):
        row, col = item
        height = self[item]

        def score_lines(*lines, score=1):
            if lines:
                if lines[0]:
                    for i, h in enumerate(lines[0]):
                        if h >= height:
                            score *= i+1
                            return score_lines(*lines[1:], score=score)
                    score *= len(lines[0])
                    return score_lines(*lines[1:], score=score)
                else:
                    return 0
            else:
                return score
        
        return score_lines(self[row-1::-1,col] if row else [], self[row+1::,col], self[row, col-1::-1] if col else [], self[row, col+1::])
    
    def part_one(self):
        visible = set()
        for i in range(self.ncols):
            visible |= self.visible_col(i)
        for j in range(self.nrows):
            visible |= self.visible_row(j)
        return len(visible)

    def part_two(self):
        return max(
            max(
                (self.score((row, col)), (row+1, col+1)) for col in range(self.ncols)
            ) for row in range(self.nrows)
        )


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
    trees = Grid(inputs)
    visible_trees = trees.part_one()
    t1 += time.time()
    print(f"There are {visible_trees:,} distinct visible trees from the edge of the forest.")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(f":: Part Two ::")
    t2 = -time.time()
    score, (row, col) = trees.part_two()
    t2 += time.time()
    ordinal = lambda n: f'{n}st' if (n%10) == 1 else f'{n}nd' if (n%10) == 2 else f'{n}rd' if (n%10) == 3 else f'{n}th'
    print(f"With a scenic score of {score:,}, the {ordinal(col)} tree in the {ordinal(row)} row has the highest possible scenic score.")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main(inputs)
