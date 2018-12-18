# https://adventofcode.com/2018/day/17

import itertools
import re

TEST_INPUT = """
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
""".splitlines()

def parse_input(lines):
    """Produce x,y pairs"""
    for line in lines:
        m = re.search(r"([xy])=(\d+), [xy]=(\d+)\.\.(\d+)", line)
        if m:
            first, only, low, high = m.groups()
            if first == 'x':
                x = int(only)
                for y in range(int(low), int(high)+1):
                    yield (x, y)
            else:
                y = int(only)
                for x in range(int(low), int(high)+1):
                    yield (x, y)
        elif line.strip():
            raise Exception(f"Don't understand {line!r}")

SAND, CLAY, PASSED, REST, SPRING = ".#|~+"

class Ground:
    def __init__(self):
        self.scan = {}
        self.water = [(500, 0)]
        self.leftright = []
        self.flowing_left = True
        self.last_down = False
        self.choices = []

    def read_input(self, lines):
        self.scan = {}
        for x, y in parse_input(lines):
            self.scan[x, y] = CLAY
        self.scan[500, 0] = SPRING
        self.minx = min(x for x, y in self.scan)-1
        self.maxx = max(x for x, y in self.scan)+1
        self.miny = min(y for x, y in self.scan)
        self.maxy = max(y for x, y in self.scan)

    def at(self, x, y):
        return self.scan.get((x, y), SAND)

    def print(self):
        print("=" * 80)
        for y in range(self.miny, min(self.maxy+1, 9999)):
            for x in range(self.minx, self.maxx+1):
                print(self.at(x, y), end='')
            print()

    def advance(self):
        while True:
            x, y = self.water[-1]
            if self.at(x, y+1) == SAND:
                y += 1
                if y <= self.maxy:
                    self.scan[x, y] = PASSED
                    self.water.append((x, y))
                    self.last_down = True
                    self.flowing_left = True
                    return True
                elif self.choices:
                    backto = self.choices.pop()
                    del self.water[backto:]
                    self.flowing_left = False
                else:
                    return False
            elif self.flowing_left:
                if self.last_down:
                    self.choices.append(len(self.water))
                    #print(f"At {x},{y}: self.choices is {self.choices}")
                if self.at(x-1, y) == SAND:
                    x -= 1
                    self.scan[x, y] = PASSED
                    self.water.append((x, y))
                    self.last_down = False
                    return True
                else:
                    backto = self.choices.pop()
                    del self.water[backto:]
                    #print(f"Back: tip is {self.water[-1]}")
                    self.flowing_left = False
            else:
                if self.at(x+1, y) == SAND:
                    x += 1
                    self.scan[x, y] = PASSED
                    self.water.append((x, y))
                    self.last_down = False
                    return True
                else:
                    # Maybe a blocked row.
                    #print(f"Blocked at {x, y}")
                    x0 = x
                    while self.at(x, y) == PASSED:
                        x -= 1
                    if self.at(x, y) == CLAY:
                        # Blocked.
                        for x in range(x+1, x0+1):
                            self.scan[x, y] = REST
                        while self.water[-1][1] == y:
                            self.water.pop()
                        self.flowing_left = True
                        self.choices.append(len(self.water))
                    else:
                        backto = self.choices.pop()
                        del self.water[backto:]
                        self.flowing_left = False

    def run(self):
        try:
            while self.advance():
                #self.print()
                pass
        finally:
            self.print()
        # Sum the REST and PASS cells
        return sum(c in [REST, PASSED] for c in self.scan.values())

def test_ground():
    ground = Ground()
    ground.read_input(TEST_INPUT)
    num = ground.run()
    assert num == 57

if __name__ == "__main__":
    ground = Ground()
    with open("day17_input.txt") as f:
        ground.read_input(f)
    num = ground.run()
    print(f"Part 1: water can reach {num} tiles")
