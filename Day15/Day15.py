# AoC :: Day 15
import time
import re
from collections import defaultdict
day = 15


# Parse inputs
re_parse = r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"

def parse(s, re_pattern=re_parse):
    """Turn a string into """
    m = re.match(re_pattern, s)
    return (int(m[1]), int(m[2])), (int(m[3]), int(m[4]))

inputs = [parse(i[:-1]) for i in open('Day15/Day15.in').readlines()]

# Distance between a sensor and beacon
manhattan = lambda sensor, beacon: sum(abs(xi - yi) for xi, yi in zip(sensor, beacon))

class Borel:
    def __init__(self, sets=None):
        self.sets = set(sets) if sets is not None else set()
    
    def add(self, s):
        start, stop = s

        if stop < start:
            return None
        
        for r_start, r_stop in self.sets.copy():
            if (start - 1 <= r_stop) and (r_start <= stop + 1):
                start = min(start, r_start)
                stop = max(stop, r_stop)
                self.sets.remove((r_start, r_stop))
        
        self.sets.add((start, stop))
    
    def remove(self, s):
        # print(f"removing {s} from {self.sets}")
        start, stop = s

        for r_start, r_stop in self.sets.copy():
            if (start <= r_stop) and (r_start <= stop):
                self.sets.remove((r_start, r_stop))
                if start <= r_start:
                    if stop < r_stop:
                        self.sets.add((stop + 1, r_stop))
                else:
                    self.sets.add((r_start, start - 1))
                    if stop < r_stop:
                        self.sets.add((stop + 1, r_stop))
        # print(f"result={self.sets}")
        

    def __len__(self):
        ctr = 0
        for start, stop in self.sets:
            ctr += stop - start + 1
        return ctr
    
    def __contains__(self, pt):
        for start, stop in self.sets:
            if start <= pt <= stop:
                return True
        return False
    
    def part_two(self, start, stop):
        pts = Borel({(start, stop)})

        for s in self.sets:
            pts.remove(s)
        
        if len(pts) == 1:
            return list(pts.sets)[0][0]
        elif len(pts) > 1:
            raise Exception(f"Something has gone wrong: {pts.sets}")
        else:
            return None


# part one
def part_one(beacons:dict, row=2_000_000):
    
    no_beacon = Borel()

    for bx, by in beacons:
        for sx, sy in beacons[(bx, by)]:
            d = abs(bx - sx) + abs(by - sy)
            radius = d - abs(sy - row)
            no_beacon.add((sx - radius, sx + radius))

    # Remove locations that already contain a beacon
    return len(no_beacon) - sum(1 for beacon in beacons if beacon[1]==row)


def weird_range_iterator(start, stop):
    midpoint = (stop + start) // 2
    r = iter(range(midpoint, stop))
    l = iter(reversed(range(start, midpoint)))
    
    rt = True
    lt = True
    while True:
        try:
            rx = next(r)
            yield rx
        except StopIteration:
            rt = False
            if lt:
                pass
            else:
                break
        try:
            lx = next(l)
            yield lx
        except StopIteration:
            lt = False
            if rt:
                pass
            else:
                break
            

# part two
def part_two(beacons, search_x=(0, 4_000_001), search_y=(0, 4_000_001)):

    no_beacon = defaultdict(Borel)

    tuning_frequency = lambda x, y: 4_000_000 * x + y

    for row in weird_range_iterator(*search_y):
        for bx, by in beacons:
            for sx, sy in beacons[(bx, by)]:
                d = abs(bx - sx) + abs(by - sy)
                radius = d - abs(sy - row)
                if radius >= 0:
                    no_beacon[row].add((sx - radius, sx + radius))
        
        pt = no_beacon[row].part_two(*search_x)
        if pt:
            return tuning_frequency(pt, row)


# run both solutions and print outputs + runtime
def main(inputs):
    print(f":: Advent of Code 2022 -- Day {day} ::")

    # Part One
    print(f":: Part One ::")
    t1 = -time.time()

    # init data structure with beacons
    beacons = defaultdict(set)
    row = 2_000_000

    for sensor, beacon in inputs:
        beacons[beacon].add(sensor)

    a1 = part_one(beacons, row=row)

    t1 += time.time()
    print(f"Number of locations that the beacon cannot be in row {row}: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(f":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(beacons)
    t2 += time.time()
    print(f"Tuning Frequency: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main(inputs)
