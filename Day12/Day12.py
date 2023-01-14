# AoC :: Day 12
import time
import numpy as np
day = 12


# Parse inputs
inputs = np.array([list(map(ord, i[:-1])) for i in open('Day12.in').readlines()])
Mx, My = inputs.shape

# utils
cardinal = (
    np.array([ 1, 0]),
    np.array([-1, 0]),
    np.array([ 0, 1]),
    np.array([ 0,-1]),
)

def possible(pos, topography, delta, directions, Mx=Mx, My=My):
    """Check the height is within range for each cardinal direction and return options"""
    h = topography[pos] + delta
    px, py = pos
    return (
        v for dx, dy in directions if 
        (-1 < px + dx < Mx) and (-1 < py + dy < My) and topography[(v:= (px + dx, py + dy))] <= h
    )

def recursive_walk(positions:set, goal, topography=inputs, delta=1, dirs=cardinal, visited:set=None, n=0):
    # init new step
    new_positions = set()
    if visited is None:
        visited = set()
    visited |= positions

    # find new steps
    for pos in positions:
        for step in possible(pos, topography, delta, dirs):
            if step == goal:
                # break if found
                return n+1
            new_positions.add(step)
    
    # trim positions we've already searched (they're being visited by a suboptimal path)
    new_positions -= visited

    return recursive_walk(new_positions, goal, topography, delta, dirs, visited, n+1)


# part one
def part_one(start, goal, topography, delta=1):
    # init
    ans = recursive_walk(start, goal, topography, delta)
    return ans


# run both solutions and print outputs + runtime
def main(inputs):
    print(f":: Advent of Code 2022 -- Day {day} ::")

    # Part One
    print(f":: Part One ::")
    t1 = -time.time()
    start_pos = tuple(*np.argwhere(inputs == ord('S')))
    goal_pos = tuple(*np.argwhere(inputs == ord('E')))
    inputs[start_pos] = ord('a')
    inputs[goal_pos] = ord('z')
    a1 = part_one({start_pos}, goal_pos, inputs)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(f":: Part Two ::")
    t2 = -time.time()
    all_as = {tuple(p) for p in np.argwhere(inputs == ord('a'))}
    a2 = part_one(all_as, goal_pos, inputs)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main(inputs)
