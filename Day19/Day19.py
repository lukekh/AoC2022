"""AoC :: Day 19"""
from dataclasses import dataclass
import re
import time
from typing import Dict, List, Literal, Optional, Pattern
day = 19


# Parse inputs
@dataclass
class Resources:
    """The price of doing business"""
    ore: int
    clay: int
    obsidian: int
    geodes: int = 0

    def __add__(self, other: "Resources"):
        return Resources(
            self.ore + other.ore,
            self.clay + other.clay,
            self.obsidian + other.obsidian,
            self.geodes + other.geodes,
        )

    def __sub__(self, other: "Resources"):
        return Resources(
            self.ore - other.ore,
            self.clay - other.clay,
            self.obsidian - other.obsidian,
            self.geodes - other.geodes,
        )

KINDS = Literal["resource", "robot"]
RESOURCES = Literal["ore", "clay", "obsidian", "geodes"]

@dataclass
class Symbol:
    """A symbolic representation of a free variable"""
    mins: int
    kind: Optional[KINDS] = None
    type: Optional[RESOURCES] = None

    @property
    def resource(self):
        """return symbol as kind==resource"""
        return Symbol(mins=self.mins, kind="resource", type=self.type)

    @property
    def robot(self):
        """return symbol as a kind==robot"""
        return Symbol(mins=self.mins, kind="robot", type=self.type)

    @property
    def ore(self):
        """return symbol as a type==ore"""
        return Symbol(mins=self.mins, kind=self.kind, type="ore")

    @property
    def clay(self):
        """return symbol as a type==clay"""
        return Symbol(mins=self.mins, kind=self.kind, type="clay")

    @property
    def obsidian(self):
        """return symbol as a type==obsidian"""
        return Symbol(mins=self.mins, kind=self.kind, type="obsidian")

    @property
    def geodes(self):
        """return symbol as a type==geodes"""
        return Symbol(mins=self.mins, kind=self.kind, type="geodes")

    def __hash__(self):
        return hash((self.mins, self.kind, self.type, "symbol"))

    def __call__(self, resource: Resources):
        if sum(map(abs, [resource.ore, resource.clay, resource.obsidian, resource.geodes])) != 1:
            raise ValueError(f"Resource must refer to a single kind of resource, got {resource}")
        if resource.ore:
            return self.ore
        elif resource.ore:
            return self.clay
        elif resource.obsidian:
            return self.obsidian
        elif resource.geodes:
            return self.geodes
        else:
            raise ValueError(f"something went wrong in symbol call with resource {resource}")

    def __add__(self, other):
        return AST(
            "+",
            left=self,
            right=other
        )

    def __sub__(self, other):
        return AST(
            "-",
            left=self,
            right=other
        )

    def __mul__(self, other):
        return AST(
            "*",
            left=self,
            right=other
        )

    def __lt__(self, other):
        return AST(
            operation="<",
            left=self,
            right=other
        )

    def __le__(self, other):
        return AST(
            operation="<",
            left=self,
            right=other+1
        )

    def __gt__(self, other):
        return AST(
            operation="<",
            left=other,
            right=self
        )

    def __ge__(self, other):
        return AST(
            operation="<",
            left=other-1,
            right=self
        )

    def __eq__(self, other):
        return AST(
            operation="==",
            left=self,
            right=other
        )

@dataclass
class AST:
    """An AST for building equations with ints and symbols"""
    operation: Literal["+", "-", "*", "<", "==", None] = None
    left: "AST" | Symbol | int
    right: "AST" | Symbol | int | None = None

    def __add__(self, other):
        if (self.left == 0) and (self.operation is None):
            return other
        return AST(
            operation="+",
            left=self,
            right=other
        )

    def __sub__(self, other):
        return AST(
            operation="-",
            left=self,
            right=other
        )

    def __mul__(self, other):
        return AST(
            operation="*",
            left=self,
            right=other
        )

    def __lt__(self, other):
        return AST(
            operation="<",
            left=self,
            right=other
        )

    def __le__(self, other):
        return AST(
            operation="<",
            left=self,
            right=other+1
        )

    def __gt__(self, other):
        return AST(
            operation="<",
            left=other,
            right=self
        )

    def __ge__(self, other):
        return AST(
            operation="<",
            left=other-1,
            right=self
        )

    def __eq__(self, other):
        return AST(
            operation="==",
            left=self,
            right=other
        )


@dataclass
class Blueprint:
    """A scenario"""
    # robot costs
    ore_robot: Resources
    clay_robot: Resources
    obsidian_robot: Resources
    geode_robot: Resources

    def formulate(self, mins: int = 24):
        """
        turn a blueprint into a MIP which should solve:
        `minimize: c @ x`\\
        subject to:\\
        `A_ub @ x <= b_ub`\\
        `A_eq @ x == b_eq`\\
        `lb <= x <= ub`

        :returns: (`A_eq`, `b_eq`), (`A_ub`, `b_ub`), `c`
        """
        equations = []

        # You can only buy one robot each minute
        for m in range(1, mins+1):
            eq = AST(None, 0)
            for resource in RESOURCES:
                equations.append(
                    0 <= Symbol(m, type=resource).robot
                )
                eq += Symbol(m, type=resource).robot
            equations.append(eq <= 1)

        # You must have enough accumulated resources to buy a robot
        for m in range(1, mins+1):
            eq = AST(None, 0)
            for j in range(1, m):
                pass


re_parse = re.compile(
    r"Blueprint \d+: Each ore robot costs (\d+) ore. "
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
            Resources( int(m.group(1)), 0, 0 ),
            Resources( int(m.group(2)), 0, 0 ),
            Resources( int(m.group(3)), int(m.group(4)), 0 ),
            Resources( int(m.group(5)), 0, int(m.group(6)) ),
        )
    raise ValueError("could not parse into Blueprint of Prices")


with open('Day19/Day19.in', encoding="utf8") as f:
    inputs = [parse(i[:-1]) for i in f.readlines()]


def part_one(blueprints: List[Blueprint], mins=24):
    """Solution to part one"""
    return 0

# part two
def part_two():
    """Solution to part two"""
    ans = 0
    return ans


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
    a2 = part_two()
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
