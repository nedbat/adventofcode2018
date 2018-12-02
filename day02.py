# https://adventofcode.com/2018/day/2

import collections
import sys

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

# Part 2, brute force

def equal_but_one(s1, s2):
    """Are s1 and s2 the same except for one character?"""
    # For our purposes, the lengths are always the same, don't check.
    same = sum((c1 == c2) for c1, c2 in zip(s1, s2))
    return same == len(s1) - 1

@pytest.mark.parametrize("s1, s2, ret", [
    ("abcde", "axcye", False),
    ("fghij", "fguij", True),
])
def test_equal_but_one(s1, s2, ret):
    assert equal_but_one(s1, s2) == ret

def find_differ_by_one(ids):
    """Return a pair of ids that differ by one character."""
    for s1 in ids:
        for s2 in ids:
            if equal_but_one(s1, s2):
                return {s1, s2}

def common_chars(s1, s2):
    """Return the string of only the common chars between s1 and s2."""
    return "".join(c1 for c1, c2 in zip(s1, s2) if c1 == c2)

test_ids = [
    "abcde",
    "fghij",
    "klmno",
    "pqrst",
    "fguij",
    "axcye",
    "wvxyz",
    ]

def test_find_differ_by_one():
    assert find_differ_by_one(test_ids) == {"fguij", "fghij"}
    assert common_chars(*find_differ_by_one(test_ids)) == "fgij"

if __name__ == "__main__":
    if len(sys.argv) == 1:  # By defaut, run the brute force.
        ans = common_chars(*find_differ_by_one(puzzle_input()))
        print(f"Part 2: answer is {ans}")


def blank_ones(s):
    """Produce all the strings from s by blanking one character."""
    for i in range(len(s)):
        yield s[:i] + "_" + s[i+1:]

def test_blank_ones():
    assert list(blank_ones("abcde")) == ["_bcde", "a_cde", "ab_de", "abc_e", "abcd_"]

def find_differ_by_one_fast(ids):
    blanked = collections.defaultdict(list)
    for s in ids:
        for blank in blank_ones(s):
            blanked[blank].append(s)

    pairs = set(tuple(v) for v in blanked.values() if len(v) == 2)
    assert len(pairs) == 1
    pair = set(pairs.pop())
    return pair

def test_find_differ_by_one_fast():
    assert find_differ_by_one_fast(test_ids) == {"fguij", "fghij"}

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "fast":
        ans = common_chars(*find_differ_by_one_fast(puzzle_input()))
        print(f"Part 2: answer is {ans}")
