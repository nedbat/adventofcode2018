# https://adventofcode.com/2018/day/10

from dataclasses import dataclass
import itertools
import re

@dataclass
class Point:
    x: int
    y: int
    dx: int
    dy: int

    def move(self):
        return self.__class__(self.x+self.dx, self.y+self.dy, self.dx, self.dy)

    @classmethod
    def from_line(cls, line):
        return cls(*map(int, re.findall(r"-?\d+", line)))

class Sky:
    def __init__(self, points):
        self.points = list(points)

    def tick(self):
        return self.__class__(p.move() for p in self.points)

    def bounds(self):
        minx = min(p.x for p in self.points)
        maxx = max(p.x for p in self.points)
        miny = min(p.y for p in self.points)
        maxy = max(p.y for p in self.points)
        return minx, maxx, miny, maxy

    def area(self):
        minx, maxx, miny, maxy = self.bounds()
        return (maxx - minx + 1) * (maxy - miny + 1)

    def print(self):
        minx, maxx, miny, maxy = self.bounds()
        for y in range(miny, maxy+1):
            for x in range(minx, maxx+1):
                if any((p.x, p.y) == (x, y) for p in self.points):
                    char = "#"
                else:
                    char = "."
                print(char, end="")
            print()

def the_input(fname):
    with open(fname) as f:
        return f.read().splitlines()

def find_minimal_area(sky):
    last_sky = sky
    for second in itertools.count():
        sky = last_sky.tick()
        if sky.area() > last_sky.area():
            return last_sky, second
        last_sky = sky

def results(input_name):
    sky = Sky(Point.from_line(l) for l in the_input(input_name))
    message_sky, seconds = find_minimal_area(sky)
    message_sky.print()
    print(f"It took {seconds} seconds!")

results("day10_test_input.txt")
print()
results("day10_input.txt")
