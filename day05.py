# https://adventofcode.com/2018/day/5

import re
import string

import pytest

# Make a crazy regex that matches reacting pairs

pair_rx = "|".join(c+c.upper() for c in string.ascii_lowercase)
pair_rx += "|" + pair_rx.swapcase()

def reduce_pairs(s):
    old_s = None
    while s != old_s:
        old_s = s
        s = re.sub(pair_rx, "", s)
    return s

def test_reduce_pairs():
    assert reduce_pairs("dabAcCaCBAcCcaDA") == "dabCBAcaDA"

def puzzle_input():
    with open("day05_input.txt") as f:
        return f.read().strip()

if __name__ == "__main__":
    result = reduce_pairs(puzzle_input())
    print(f"Part 1: result is {len(result)} units: {result}")
