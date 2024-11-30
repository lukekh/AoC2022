"""
AoC :: Day 19

I have totally stolen this solution from [here](https://github.com/BeatrizBL/Adventofcode_2022/blob/master/19_Not_Enough_Minerals/not_enough_minerals.py)
"""
from dataclasses import dataclass
import re
import time
from typing import List, Literal, Pattern
from cvxopt.glpk import ilp, options
from cvxopt import matrix, solvers
day = 19

RESOURCES = ["ore", "clay", "obsidian", "geode"]

@dataclass
class Resources:
    """Some amount of ore, clay and obsidian"""
    ore: int
    clay: int
    obsidian: int

    def __getitem__(self, item: Literal["ore", "clay", "obsidian", "geode"]) -> int:
        return self.__getattribute__(item)


@dataclass
class Blueprint:
    """The robot costs for each blueprint"""
    id: int
    ore: Resources
    clay: Resources
    obsidian: Resources
    geode: Resources

    def __getitem__(self, item: Literal["ore", "clay", "obsidian", "geode"]) -> Resources:
        return self.__getattribute__(item)


re_parse = re.compile(
    r"Blueprint (\d+): Each ore robot costs (\d+) ore. "
    r"Each clay robot costs (\d+) ore. "
    r"Each obsidian robot costs (\d+) ore and (\d+) clay. "
    r"Each geode robot costs (\d+) ore and (\d+) obsidian."
)

def parse(s: str, regex: Pattern = re_parse):
    """
    Extract blueprint details

    e.g.
    Blueprint 1: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 13 clay. Each geode robot costs 3 ore and 7 obsidian.
    """
    m = regex.match(s)
    if m is not None:
        return Blueprint(
            id = int(m.group(1)),
            ore = Resources( int(m.group(2)), 0, 0 ),
            clay = Resources( int(m.group(3)), 0, 0 ),
            obsidian = Resources( int(m.group(4)), int(m.group(5)), 0 ),
            geode = Resources( int(m.group(6)), 0, int(m.group(7)) ),
        )
    raise ValueError("could not parse into Blueprint of Prices")


with open('Day19/Day19.in', encoding="utf8") as f:
    inputs = [parse(i[:-1]) for i in f.readlines()]


def linear_optimization(blueprint: Blueprint, mins: int = 24):
    """
    Set up the constraints and objective, then do linear optimization

    We will need to find the optimal decisions to maximise the number of geodes.
    For each t in {1, 2, ..., mins} you may spend resources to purchase a robot.
    So for each type of robot we will have a free variable every minute: R^{t}_min, where t \in {ore, clay, obsidian, geode}.
    """
    obj = [0]*mins + [0]*mins + [0]*mins + [-(mins-i) for i in range(mins)]
    nvars = len(obj)
    lhs_ineq = []
    rhs_ineq = []
    # Current number of robots never higher than the total materials needed minus used
    for robot_idx, robot in enumerate(RESOURCES):
        for resource_idx, resource in enumerate(RESOURCES):
            if resource == "geode":
                continue
            v = blueprint[robot][resource]
            if v > 0:
                for i in range(1, mins):
                    lhs_ineq_i = [0]*nvars
                    lhs_ineq_i[robot_idx*mins + i] = blueprint[robot][resource]
                    for j in range(i-1):
                        lhs_ineq_i[resource_idx*mins + j] = -1
                    for k, r in enumerate(RESOURCES):
                        cost = blueprint[r]
                        if k != robot_idx:
                            lhs_ineq_i[k*mins + i - 1] += cost[resource]
                    lhs_ineq.append(lhs_ineq_i)
                    rhs_ineq.append(0 if resource!='ore' else blueprint[resource][resource])
    # Current number of robots at most 1 more than in previous step
    for i in range(1, mins):
        lhs_ineq_i = [0]*nvars
        for j in range(len(RESOURCES)):
            lhs_ineq_i[j*mins + i] = 1
            lhs_ineq_i[j*mins + i-1] = -1
        lhs_ineq.append(lhs_ineq_i)
        rhs_ineq.append(1)
    # Not possible to lose robots
    for i in range(len(RESOURCES)):
        for j in range(1, mins):
            lhs_ineq_j = [0]*nvars
            lhs_ineq_j[i*mins + j] = -1
            lhs_ineq_j[i*mins + j - 1] = 1
            lhs_ineq.append(lhs_ineq_j)
            rhs_ineq.append(0)
    # Starting with just one ore robot
    lhs_eq = []
    rhs_eq = []
    for i in range(len(RESOURCES)):
        lhs_eq_i = [0]*nvars
        lhs_eq_i[i*mins] = 1
        lhs_eq.append(lhs_eq_i)
        rhs_eq.append((1 if i==0 else 0))
    # Optimum
    (_,x) = ilp(
        c=matrix(obj, tc='d'), 
        G=matrix(lhs_ineq, tc='d').T, 
        h=matrix(rhs_ineq, tc='d'),
        A=matrix(lhs_eq, tc='d').T, 
        b=matrix(rhs_eq, tc='d'), 
        I=set(range(len(obj))),
    )
    return list(x[(3*mins):(4*mins)])


def part_one(blueprints: List[Blueprint], mins: int = 24):
    """Solution to part one"""
    quality = 0
    for blueprint in blueprints:
        geode_times = linear_optimization(blueprint, mins)
        n = sum(len(geode_times) - geode_times.index(i+1) for i in range(int(max(geode_times))))
        quality += blueprint.id * n
    return quality

# part two
def part_two(blueprints: List[Blueprint], mins: int = 32, n: int = 3):
    """Solution to part two"""
    value = 1
    for blueprint in blueprints[:n]:
        geode_times = linear_optimization(blueprint, mins)
        n = sum(len(geode_times) - geode_times.index(i+1) for i in range(int(max(geode_times))))
        value *= n
    return value


# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2022 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(inputs)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(inputs)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
