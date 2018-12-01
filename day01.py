# https://adventofcode.com/2018/day/1

import itertools

import pytest


with open("day01_input.txt") as f:
    result = sum(map(eval, f))

print(f"Part 1: The resulting frequency is {result}")


def frequencies(changes):
    freq = 0
    yield freq
    for ch in changes:
        freq += ch
        yield freq

with open("day01_input.txt") as f:
    puzzle_input = list(map(eval, f))

for freq in frequencies(puzzle_input):
    pass

print(f"Part 1 again: The resulting frequency is {freq}")


def first_duplicate(seq):
    seen = set()
    for value in seq:
        if value in seen:
            return value
        seen.add(value)

@pytest.mark.parametrize("seq, dup", [
    ("abcdefb", "b"),
    ("aa", "a"),
    ("abcdefghijklmnopqrstuvwxyzmabcde", "m"),
])
def test_first_duplicate(seq, dup):
    assert first_duplicate(seq) == dup


def first_dup_frequency(changes):
    return first_duplicate(frequencies(itertools.cycle(changes)))

@pytest.mark.parametrize("seq, dup", [
    ([+1, -1], 0),
    ([+3, +3, +4, -2, -4], 10),
    ([-6, +3, +8, +5, -6], 5),
    ([+7, +7, -2, -7, -4], 14),
])
def test_first_dup_frequency(seq, dup):
    assert first_dup_frequency(seq) == dup
    

print(f"Part 2: the first duplicate frequency is {first_dup_frequency(puzzle_input)}")
