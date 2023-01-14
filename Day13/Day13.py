# AoC :: Day 13
import time
from functools import cmp_to_key
day = 13


# Parse inputs
parse = lambda l: tuple(map(eval, l))
inputs = [parse(i.split('\n')) for i in open('Day13.in').read()[:-1].split('\n\n')]

# utils
def ordered(i1, i2):
    if isinstance(i1, int):
        if isinstance(i2, int):
            return ordered_ints(i1, i2)
        elif isinstance(i2, list):
            return ordered_int_list(i1, i2)
        else:
            raise TypeError(f"{type(i2)} is neither an int or a list:: i2: {i2}, {type(i2)}")
    elif isinstance(i1, list):
        if isinstance(i2, int):
            return ordered_list_int(i1, i2)
        elif isinstance(i2, list):
            return ordered_lists(i1, i2)
        else:
            raise TypeError(f"{type(i2)} is neither an int or a list:: i2: {i2}, {type(i2)}")
    else:
        raise TypeError(f"{type(i1)} is neither an int or a list:: i2: {i2}, {type(i2)}")

def ordered_ints(i1, i2):
    """return True if strictly lt, False if strictly gt and None if neither"""
    if i1 < i2:
        return True
    elif i1 > i2:
        return False
    else:
        return None

def ordered_int_list(i1, i2):
    """convert int i1 to a list and then compare"""
    return ordered_lists([i1], i2)

def ordered_list_int(i1, i2):
    """return True if strictly lt, False if strictly gt and None if neither"""
    return ordered_lists(i1, [i2])

def ordered_lists(i1, i2):
    n = 0
    result = None
    while result is None:
        try:
            x1 = i1[n]
        except IndexError:
            result = True
        
        try:
            x2 = i2[n]
        except IndexError:
            if result:
                return None
            elif result is None:
                return False
            else:
                raise Exception("Something went wrong: result shouldn't get set to False without exiting")

        if result is None:
            result = ordered(x1, x2)
        n += 1
    return result


class Packet:
    def __init__(self, val):
        self.val = val

    def __lt__(self, other):
        return ordered(self.val, other.val)
    
    def __eq__(self, other):
        return self.val == other


# part one
def part_one(inputs):
    # init
    ans = 0

    for n, (i1, i2) in enumerate(inputs):
        if ordered(i1, i2):
            ans += n + 1
    return ans


# part two
def part_two(inputs, decoder_packets=([[2]], [[6]])):
    # init
    flat_inputs = [Packet(item) for pair in inputs for item in pair]
    flat_inputs += [Packet(decoder_packet) for decoder_packet in decoder_packets]
    flat_inputs = sorted(flat_inputs)

    d1_idx = flat_inputs.index(decoder_packets[0]) + 1
    d2_idx = flat_inputs.index(decoder_packets[1], d1_idx) + 1

    return d1_idx*d2_idx


# run both solutions and print outputs + runtime
def main(inputs):
    print(f":: Advent of Code 2022 -- Day {day} ::")

    # Part One
    print(f":: Part One ::")
    t1 = -time.time()
    a1 = part_one(inputs)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(f":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(inputs)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main(inputs)
