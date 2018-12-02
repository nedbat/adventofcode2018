# https://adventofcode.com/2018/day/2

import collections

import pytest

def puzzle_input():
    with open("day02_input.txt") as f:
        return f.read().splitlines()

def char_counts(s):
    """Given a string, return a set of character counts occurring."""
    return set(collections.Counter(s).values())

@pytest.mark.parametrize("s, counts", [
    ("abcdef", {1}),
    ("bababc", {1, 2, 3}),
    ("abbcde", {1, 2}),
    ("abcccd", {1, 3}),
    ("aabcdd", {1, 2}),
    ("abcdee", {1, 2}),
    ("ababab", {3}),
])
def test_char_counts(s, counts):
    assert char_counts(s) == counts

def checksum(ids):
    counts = [char_counts(s) for s in ids]
    num2 = sum((2 in cc) for cc in counts)
    num3 = sum((3 in cc) for cc in counts)
    return num2 * num3

def test_checksum():
    ids = [
        "abcdef",
        "bababc",
        "abbcde",
        "abcccd",
        "aabcdd",
        "abcdee",
        "ababab",
        ]
    assert checksum(ids) == 12

if __name__ == "__main__":
    ans = checksum(puzzle_input())
    print(f"Part 1: the checksum is {ans}")
