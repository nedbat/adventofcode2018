# https://adventofcode.com/2018/day/25

from dataclasses import dataclass
import itertools

import pytest


@dataclass
class Point:
    w: int
    x: int
    y: int
    z: int

    @classmethod
    def from_line(cls, line):
        return cls(*map(int, line.split(",")))

def distance(pt1, pt2):
    return (
        abs(pt1.w - pt2.w) +
        abs(pt1.x - pt2.x) +
        abs(pt1.y - pt2.y) +
        abs(pt1.z - pt2.z)
        )

def pt_in_con(pt, con):
    """Is `pt` part of the constellation `con`?"""
    return any(distance(pt, conpt) <= 3 for conpt in con)

def constellations(pts):
    cons = []
    for pt in pts:
        in_cons, not_in_cons = [], []
        for con in cons:
            if pt_in_con(pt, con):
                in_cons.append(con)
            else:
                not_in_cons.append(con)
        cons = not_in_cons
        cons.append(list(itertools.chain(*in_cons)) + [pt])
    return cons

@pytest.mark.parametrize("pts, num_cons", [
    ("""\
    0,0,0,0
    3,0,0,0
    0,3,0,0
    0,0,3,0
    0,0,0,3
    0,0,0,6
    9,0,0,0
    12,0,0,0
    """, 2),
    ("""\
    -1,2,2,0
    0,0,2,-2
    0,0,0,-2
    -1,2,0,0
    -2,-2,-2,2
    3,0,2,-1
    -1,3,2,2
    -1,0,-1,0
    0,2,1,-2
    3,0,0,0
    """, 4),
    ("""\
    1,-1,0,1
    2,0,-1,0
    3,2,-1,0
    0,0,3,1
    0,0,-1,-1
    2,3,-2,0
    -2,2,0,0
    2,-2,0,-1
    1,-1,0,-1
    3,2,0,2
    """, 3),
    ("""\
    1,-1,-1,-2
    -2,-2,0,1
    0,2,1,3
    -2,3,-2,1
    0,2,3,-2
    -1,-1,1,-2
    0,-2,-1,0
    -2,2,3,-1
    1,2,2,0
    -1,-2,0,-2
    """, 8),
])
def test_constellations(pts, num_cons):
    pts = [Point.from_line(l) for l in pts.splitlines() if l.strip()]
    cons = constellations(pts)
    assert len(cons) == num_cons

if __name__ == "__main__":
    with open("day25_input.txt") as f:
        pts = [Point.from_line(l) for l in f]
        cons = constellations(pts)
        print(f"Part 1: there are {len(cons)} constellations")
