# https://adventofcode.com/2018/day/22

import itertools

class Cave:
    def __init__(self, depth, tx, ty):
        self.depth = depth
        self.tx = tx
        self.ty = ty
        self.regions = {}

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
