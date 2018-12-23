# https://adventofcode.com/2018/day/23

from dataclasses import dataclass
import re


@dataclass
class Nanobot:
    x: int
    y: int
    z: int
    r: int

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

def part1(lines):
    bots = [parse_line(l) for l in lines]
    strongest = max(bots, key=lambda b: b.r)
    print(f"Strongest has r = {strongest.r}")
    num_in_range = sum(1 for b in bots if distance(strongest, b) <= strongest.r)
    return num_in_range

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
