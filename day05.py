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


def remove_units(s, c):
    return re.sub(r"(?i)" + c, "", s)

def test_remove_units():
    assert remove_units("dabAcCaCBAcCcaDA", "a") == "dbcCCBcCcD"
    assert remove_units("dabAcCaCBAcCcaDA", "b") == "daAcCaCAcCcaDA"
    assert remove_units("dabAcCaCBAcCcaDA", "c") == "dabAaBAaDA"
    assert remove_units("dabAcCaCBAcCcaDA", "d") == "abAcCaCBAcCcaA"

def polymers_with_units_removed(polymer):
    for c in string.ascii_lowercase:
        yield remove_units(polymer, c)

def best_reduction(polymer):
    reduced = (reduce_pairs(p) for p in polymers_with_units_removed(polymer))
    return min(reduced, key=len)

def test_best_reduction():
    assert best_reduction("dabAcCaCBAcCcaDA") == "daDA"

if __name__ == "__main__":
    best_reduced = best_reduction(puzzle_input())
    print(f"Part 2: best reduced is {best_reduced}, length {len(best_reduced)}")
