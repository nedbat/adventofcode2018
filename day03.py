# https://adventofcode.com/2018/day/3

import collections
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Claim:
    id: int
    left: int
    top: int
    wide: int
    tall: int

    @classmethod
    def parse(cls, text):
        # Don't be particular: get all the numbers from the text.
        nums = re.findall(r"\d+", text)
        if len(nums) == 5:
            return Claim(*map(int, nums))

    @classmethod
    def parse_all(cls, text):
        return list(filter(None, map(Claim.parse, text.splitlines())))

    def covered_squares(self):
        """What squares does this claim cover?"""
        for x in range(self.left, self.left + self.wide):
            for y in range(self.top, self.top + self.tall):
                yield (x, y)

def test_claim_parse():
    assert Claim.parse("#123 @ 3,2: 5x4") == Claim(123, 3, 2, 5, 4)

def puzzle_input():
    with open("day03_input.txt") as f:
        return Claim.parse_all(f.read())

def multiply_covered_squares(claims):
    """Which squares are covered by multiple claims?"""
    # Key is (x,y), value is number of claims.
    grid = collections.Counter()
    for claim in claims:
        for square in claim.covered_squares():
            grid[square] += 1

    return [square for square, claims in grid.items() if claims > 1]

TEST_INPUT = """
    #1 @ 1,3: 4x4
    #2 @ 3,1: 4x4
    #3 @ 5,5: 2x2
    """

def test_multiply_covered_squares():
    claims = Claim.parse_all(TEST_INPUT)
    assert len(multiply_covered_squares(claims)) == 4

if __name__ == "__main__":
    ans = len(multiply_covered_squares(puzzle_input()))
    print(f"Part 1: {ans} square inches of fabric are within two or more claims")


def unlapped_claims(claims):
    """Which claims don't overlap with any other?"""
    # Key is (x,y), value is a list of claims.
    grid = collections.defaultdict(list)
    for claim in claims:
        for square in claim.covered_squares():
            grid[square].append(claim)

    # A set of candidates for non-overlappedness.
    ok = set(claims)

    # Any square with more than one claim disqualifies all the claims on that
    # square.
    for claims in grid.values():
        if len(claims) > 1:
            ok.difference_update(claims)

    return ok

def test_unlapped_claims():
    claims = Claim.parse_all(TEST_INPUT)
    unlapped = unlapped_claims(claims)
    assert len(unlapped) == 1
    assert unlapped.pop().id == 3


if __name__ == "__main__":
    unlapped = unlapped_claims(puzzle_input())
    assert len(unlapped) == 1
    ans = unlapped.pop()
    print(f"Part 2: the only claim that doesn't overlap is #{ans.id}")
