"""AoC :: Day 23"""
from enum import Enum
import time
day = 23

class Direction(Enum):
    """A direction on this grid"""
    E  = ( 1,  0)
    NE = ( 1, -1)
    N  = ( 0, -1)
    NW = (-1, -1)
    W  = (-1,  0)
    SW = (-1,  1)
    S  = ( 0,  1)
    SE = ( 1,  1)

DIRECTIONS = [
    Direction.E,
    Direction.NE,
    Direction.N,
    Direction.NW,
    Direction.W,
    Direction.SW,
    Direction.S,
    Direction.SE,
]

# The proposals
PROPOSAL_DICT = {
    Direction.N: [Direction.N, Direction.NE, Direction.NW],
    Direction.S: [Direction.S, Direction.SE, Direction.SW],
    Direction.W: [Direction.W, Direction.NW, Direction.SW],
    Direction.E: [Direction.E, Direction.NE, Direction.SE],
}
PROPOSALS = [
    Direction.N,
    Direction.S,
    Direction.W,
    Direction.E,
]

class Elf(tuple[int, int]):
    """
    Coordinates of an elf along with some relevant methods
    """
    def __add__(self, other):
        return Elf((self[0] + other[0], self[1] + other[1]))

    def consider(self, elves: set["Elf"]) -> set["Elf"]:
        """Return the elves that surround this elf"""
        return {self + d.value for d in DIRECTIONS} & elves

    def propose(self, elves: set["Elf"], proposals: list[Direction]):
        """Return the elves that surround this elf"""
        for direction in proposals:
            if not {self + p.value for p in PROPOSAL_DICT[direction]} & elves:
                return self + direction.value

# Parse inputs
with open('Day23/Day23.in', encoding="utf8") as f:
    ELVES: set[Elf] = set()
    for row, s in enumerate([i[:-1] for i in f.readlines()]):
        for col, char in enumerate(s):
            if char == "#":
                ELVES.add(Elf((col, row)))
    ELVES_PT2 = ELVES.copy()


def rectangle(elves: set[Elf]):
    """Calculate the number of empty tiles in the smallest rectangle bounding elves"""
    mx = Mx = my = My = None

    for elf in elves:
        if (mx is None) or (elf[0] < mx):
            mx = elf[0]
        if (Mx is None) or (elf[0] > Mx):
            Mx = elf[0]
        if (my is None) or (elf[1] < my):
            my = elf[1]
        if (My is None) or (elf[1] > My):
            My = elf[1]

    return (Mx - mx + 1) * (My - my + 1) - len(elves)


# part one
def do_round(elves: set[Elf], proposals: list[Direction]) -> bool:
    """
    returns True if there is movement else False 
    """
    movement_occurs = False
    considered: set[Elf] = set()
    # First half of the round
    for elf in elves:
        if elf in considered:
            continue
        if (surrounding := elf.consider(elves)):
            considered.add(elf)
            considered.update(surrounding)

    # Second half of a round
    movement: dict[Elf, list[Elf]] = {}
    for elf in considered:
        p = elf.propose(considered, proposals)
        if p is not None:
            if p not in movement:
                movement[p] = [elf]
            else:
                movement[p].append(elf)
    for p, es in movement.items():
        if len(es) == 1:
            elves.remove(es[0])
            elves.add(p)
            movement_occurs = True

    return movement_occurs

def part_one(elves: set[Elf], proposals: list[Direction], rounds: int = 10):
    """Solution to part one"""
    for r in range(rounds):
        do_round(elves, proposals[(r % 4):] + proposals[:(r % 4)])
    return rectangle(elves)


# part two
def part_two(elves: set[Elf], proposals: list[Direction], rounds: int = 10):
    """
    Solution to part two
    
    Note: we just start from where part one leaves off
    """
    movement = True
    while movement:
        movement = do_round(elves, proposals[(rounds % 4):] + proposals[:(rounds % 4)])
        rounds += 1

    return rounds


# run both solutions and print outputs + runtime
def main():
    """The full days solution"""
    print(f":: Advent of Code 2022 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(ELVES, PROPOSALS)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(ELVES, PROPOSALS)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main()
