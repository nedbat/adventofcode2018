# https://adventofcode.com/2018/day/22

import itertools

class Cave:
    def __init__(self, depth, tx, ty):
        self.depth = depth
        self.tx = tx
        self.ty = ty
        self.regions = {}
        self.erosion_level(0, 0)

    def erosion_level(self, x, y):
        if (x, y) not in self.regions:
            if (x, y) == (0, 0):
                gindex = 0
            elif (x, y) == (self.tx, self.ty):
                gindex = 0
            elif x == 0:
                gindex = y * 48271
            elif y == 0:
                gindex = x * 16807
            else:
                gindex = self.erosion_level(x-1, y) * self.erosion_level(x, y-1)
            level = (gindex + self.depth) % 20183
            self.regions[x, y] = level
        return self.regions[x, y]

    def risk_level(self, x, y):
        return self.erosion_level(x, y) % 3

    def print(self):
        for y in range(self.ty+1):
            for x in range(self.tx+1):
                if (x, y) == (0, 0):
                    print("M", end="")
                elif (x, y) == (self.tx, self.ty):
                    print("T", end="")
                else:
                    print(".=|"[self.risk_level(x, y)], end="")
            print()

    def area_risk_level(self):
        return sum(self.risk_level(x, y) for x, y in itertools.product(range(self.tx+1), range(self.ty+1)))

def test_it():
    test_cave = Cave(510, 10, 10)
    test_cave.print()
    assert test_cave.area_risk_level() == 114

if __name__ == "__main__":
    cave = Cave(4080, 14, 785)
    risk = cave.area_risk_level()
    print(f"Part 1: total risk level is {risk}")


from astar import State, search


def neighbors(x, y):
    """Orthogonal neighbors, but not negative."""
    if x > 0:
        yield x-1, y
    if y > 0:
        yield x, y-1
    yield x+1, y
    yield x, y+1


ROCKY, WET, NARROW = 0, 1, 2
NEITHER, TORCH, CLIMBING = TOOLS = "neither torch climbing".split()

def is_valid_tool(tool, region_type):
    if region_type == ROCKY:
        return tool in (TORCH, CLIMBING)
    elif region_type == WET:
        return tool in (CLIMBING, NEITHER)
    else:
        assert region_type == NARROW
        return tool in (TORCH, NEITHER)

MOVE_COST = 1
TOOL_COST = 7

class CaveState(State):
    def __init__(self, cave, x=0, y=0, tool=TORCH):
        self.cave = cave
        self.x = x
        self.y = y
        self.tool = tool

    def __hash__(self):
        return hash((self.x, self.y, self.tool))

    def __eq__(self, other):
        return (self.x, self.y, self.tool) == (other.x, other.y, other.tool)

    def is_goal(self):
        return (
            self.x == self.cave.tx and
            self.y == self.cave.ty and
            self.tool == TORCH
            )

    def guess_completion_cost(self):
        moving_cost = abs(self.cave.tx - self.x) + abs(self.cave.ty - self.y)
        tool_cost = 0 if self.tool == TORCH else TOOL_COST
        return moving_cost + tool_cost

    def summary(self):
        return (
            f"at {(self.x, self.y)} with {self.tool}, "
            f"cave has {len(self.cave.regions):,d} regions"
            )

    def next_states(self, cost):
        # Maybe we can move, takes 1 minute
        for nx, ny in neighbors(self.x, self.y):
            there = self.cave.risk_level(nx, ny)
            if is_valid_tool(self.tool, there):
                nstate = self.__class__(self.cave, nx, ny, self.tool)
                yield nstate, cost + MOVE_COST

        # Maybe we can change our tool, takes 7 minutes
        for tool in TOOLS:
            if tool != self.tool:
                here = self.cave.risk_level(self.x, self.y)
                if is_valid_tool(tool, here):
                    nstate = self.__class__(self.cave, self.x, self.y, tool)
                    yield nstate, cost + TOOL_COST

def test_search():
    test_cave = Cave(510, 10, 10)
    time = search(CaveState(test_cave), log=True)
    assert time == 45

if __name__ == "__main__":
    cave = Cave(4080, 14, 785)
    time = search(CaveState(cave), log=True)
    print(f"Part 2: fewest minutes to reach target is {time}")
