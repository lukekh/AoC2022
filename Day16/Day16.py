"""AoC :: Day 16"""
import re
import time
from typing import Dict, Set
day = 16


# Valve class
class Valve:
    """An object representing a valve"""
    # regex for parsing inputs, some examples:
    # - Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
    # - Valve AA has flow rate=9; tunnel leads to valve DD
    re_parse = re.compile(r"Valve (\w+) has flow rate=(-?\d+); tunnels? leads? to valves? (.+)")
    all_valves = {}
    valve_graph = {}
    fm_valve_graph = {}

    def __init__(self, string):
        m = self.re_parse.match(string)
        self.id = m.group(1)
        self.flow = int(m.group(2))
        self._connections = [v.strip() for v in m.group(3).split(',')]

        # Some globals
        self.all_valves[self.id] = self
        self.valve_graph[self.id] = {}
        self.valve_graph[self.id][self.id] = 0
        for connection in self._connections:
            self.valve_graph[self.id][connection] = 1

    @property
    def connections(self) -> Dict["Valve", int]:
        """The connected valves"""
        return self.fm_valve_graph[self]

    def __repr__(self):
        return f"Valve({self.id}, {self.flow}, {self._connections})"

    def __hash__(self):
        return hash((self.id, "Valve"))

    def __eq__(self, other):
        return hash(self) == hash(other)

    @classmethod
    def perform_FloydWarshall(cls):
        """Perform the Floyd Warshall Algorithm to find the minimal distance between nodes"""
        def update_shortest(i, j, k):
            """Some None handling"""
            if (k in cls.valve_graph[i]) and (j in cls.valve_graph[k]):
                if j in cls.valve_graph[i]:
                    cls.valve_graph[i][j] = min(cls.valve_graph[i][k] + cls.valve_graph[k][j], cls.valve_graph[i][j])
                    cls.valve_graph[j][i] = min(cls.valve_graph[i][k] + cls.valve_graph[k][j], cls.valve_graph[i][j])
                else:
                    cls.valve_graph[i][j] = cls.valve_graph[i][k] + cls.valve_graph[k][j]
                    cls.valve_graph[j][i] = cls.valve_graph[i][k] + cls.valve_graph[k][j]

        for k in cls.all_valves:
            for i in cls.all_valves:
                for j in cls.all_valves:
                    update_shortest(i, j, k)

        for v in cls.all_valves.values():
            cls.fm_valve_graph[v] = {}
            for w in cls.all_valves.values():
                if (w.flow > 0) and (w != v):
                    cls.fm_valve_graph[v][w] = cls.valve_graph[v.id][w.id]


with open('Day16.in', encoding="utf8") as f:
    inputs = {v.id: v for v in [Valve(i) for i in f.readlines()]}

# This creates a valve graph that minimally reveals distance between non-zero-flow valves
Valve.perform_FloydWarshall()

# part one
def recursive_action(open_time=1):
    """Returns a curried function so that we don't have to keep specifying open_time"""
    def func(valve: Valve, time_remaining: int, closed_valves: set, pressure: int):
        if (not closed_valves) or (time_remaining < 1):
            # print(pressure, valve)
            return pressure

        pressure += valve.flow * (time_remaining)
        closed_valves = closed_valves - {valve}

        if not closed_valves:
            # print(pressure, valve)
            return pressure

        # Different moves to open a valve (worth opening)
        M = []

        for m in closed_valves:
            move_time = valve.connections[m]
            val = func(
                m,
                time_remaining = time_remaining-move_time-open_time,
                closed_valves = closed_valves,
                pressure = pressure
            )
            M.append(val)

        # Return the max pressure of options
        if M:
            return max(M)
        return pressure

    return func

def part_one(args, time_remaining=30, open_time=1, position="AA"):
    """Solution to part one"""
    ans = recursive_action(open_time)(
        args[position],
        time_remaining,
        {v for v in inputs.values() if v.flow > 0},
        0
    )
    return ans


# part two
def recursive_actions(open_time=1, total_time=26):
    """A modification from part one to handle two entities opening valves"""
    strategies = {}
    def func(v1: Valve, v2: Valve, t1: int, t2: int, closed_valves: Set[Valve], pressure: int):
        # Branch cut to check less states
        strategy = tuple(sorted([v.id for v in closed_valves]))
        if (s := strategies.get(strategy)):
            st1, st2, p = s
            if (st1 + st2 <= t1 + t2) and (pressure <= p):
                return pressure
        strategies[strategy] = (t1, t2, pressure)

        # init M
        M = []

        # If person 1 can still make a move + open
        if t1 < total_time - 3:
            # Allow person in v1 to move first
            for m1 in closed_valves:
                mt1 = v1.connections[m1]
                new_t1 = t1 + mt1 + open_time
                if new_t1 < total_time:
                    new_pressure = pressure + (total_time - new_t1) * m1.flow
                    new_closed_valves = closed_valves - {m1}
                else:
                    new_pressure = pressure
                    new_closed_valves = closed_valves
                if t2 < total_time - 3:
                    for m2 in new_closed_valves:
                        mt2 = v2.connections[m2]
                        new_t2 = t2 + mt2 + open_time
                        if t2 < total_time:
                            new_pressure2 = new_pressure + (total_time - new_t2) * m2.flow
                        else:
                            new_pressure2 = new_pressure
                        val = func(m1, m2, new_t1, new_t2, new_closed_valves - {m2}, new_pressure2)
                        M.append(val)
                else:
                    val = func(m1, v2, new_t1, t2, new_closed_valves, new_pressure)
                    M.append(val)
        # Else if person 2 can still viably move + open
        elif t2 < total_time - 3:
            for m2 in closed_valves:
                mt2 = v2.connections[m2]
                new_t2 = t2 + mt2 + open_time
                if t2 < total_time:
                    new_pressure = pressure + (total_time - new_t2) * m2.flow
                    val = func(v1, m2, t1, new_t2, closed_valves - {m2}, new_pressure)
                    M.append(val)
        # Else we're done
        else:
            return pressure

        # Return the max pressure of options
        if M:
            return max(M)
        return pressure

    return func

def part_two(args, time_remaining=26, open_time=1, position="AA"):
    """Solution to part two"""
    ans = recursive_actions(open_time, time_remaining)(
        args[position],
        args[position],
        0,
        0,
        {v for v in inputs.values() if v.flow > 0},
        0,
    )
    return ans


# run both solutions and print outputs + runtime
def main(args):
    """The day's solution"""
    print(f":: Advent of Code 2022 -- Day {day} ::")

    # Part One
    print(":: Part One ::")
    t1 = -time.time()
    a1 = part_one(args)
    t1 += time.time()
    print(f"Answer: {a1}")
    print(f"runtime: {t1: .4f}s")

    # Part Two
    print(":: Part Two ::")
    t2 = -time.time()
    a2 = part_two(args)
    t2 += time.time()
    print(f"Answer: {a2}")
    print(f"runtime: {t2: .4f}s")
    print(f":: total runtime: {t1+t2: .4f}s ::")


if __name__ == "__main__":
    main(inputs)
