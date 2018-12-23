# https://adventofcode.com/2018/day/23

from dataclasses import dataclass
import functools
import re


def overlap(start1, end1, start2, end2):
    """Does the range (start1, end1) overlap with (start2, end2)?"""
    return end1 >= start2 and end2 >= start1

@dataclass
class Boct:
    """A bounding octagon."""
    xyz: range
    mxyz: range
    xmyz: range
    xymz: range

    def __bool__(self):
        return bool(self.xyz and self.mxyz and self.xmyz and self.xymz)

def intersect_range(r1, r2):
    if r1 is None or r2 is None:
        return None
    inter = range(max(r1.start, r2.start), min(r1.stop, r2.stop))
    if len(inter) > 0:
        return inter
    else:
        return None

def intersect_boct(b1, b2):
    if not b1 or not b2:
        return None
    return Boct(
        intersect_range(b1.xyz, b2.xyz),
        intersect_range(b1.mxyz, b2.mxyz),
        intersect_range(b1.xmyz, b2.xmyz),
        intersect_range(b1.xymz, b2.xymz),
        )

@dataclass
class Nanobot:
    x: int
    y: int
    z: int
    r: int

    def boct(self):
        x, y, z, r = self.x, self.y, self.z, self.r
        return Boct(
            range(x + y + z - r, x + y + z + r),
            range(-x + y + z - r, -x + y + z + r),
            range(x - y + z - r, x - y + z + r),
            range(x + y - z - r, x + y - z + r),
            )

def parse_line(line):
    nums = re.findall(r"-?\d+", line)
    if len(nums) != 4:
        raise Exception(f"Unparsable line: {line!r}")
    return Nanobot(*map(int, nums))

def distance(bot1, bot2):
    """How manhattan-far away are two bots?"""
    return (
        abs(bot1.x - bot2.x) +
        abs(bot1.y - bot2.y) +
        abs(bot1.z - bot2.z)
        )

def bots_in_range(bot, bots):
    return [b for b in bots if distance(bot, b) <= bot.r]

def num_in_range(bot, bots):
    return len(bots_in_range(bot, bots))

def part1(lines):
    bots = [parse_line(l) for l in lines]
    strongest = max(bots, key=lambda b: b.r)
    return num_in_range(strongest, bots)

TEST_INPUT = """\
pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1
"""

def test_part1():
    assert part1(TEST_INPUT.splitlines()) == 7

def the_input():
    with open("day23_input.txt") as f:
        return list(f)

if __name__ == "__main__":
    ans = part1(the_input())
    print(f"Part 1: {ans} bots are in range of the strongest")

def part2(lines):
    bots = [parse_line(l) for l in the_input()]
    census = [(bots_in_range(b, bots), b) for b in bots]
    census.sort(key=lambda pair: len(pair[0]), reverse=True)
    for in_range, bot in census:
        bocts = [bot.boct() for bot in in_range]
        print(len(bocts))
        inter = functools.reduce(intersect_boct, bocts)
        print(inter)
        if inter is not None:
            return inter.xyz.start

if __name__ == "__main__":
    ans = part2(the_input())
    print(f"Part 2: shortest manhattan distance is {ans}")
