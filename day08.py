# https://adventofcode.com/2018/day/8

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Node:
    children: List[Node] = field(default_factory=list)
    metadata: List[int] = field(default_factory=list)


def build_tree(nums):
    nchildren = next(nums)
    nmeta = next(nums)
    node = Node()
    for _ in range(nchildren):
        node.children.append(build_tree(nums))
    for _ in range(nmeta):
        node.metadata.append(next(nums))
    return node

def all_metadata(node):
    return sum(node.metadata) + sum(map(all_metadata, node.children))

TEST_INPUT = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"

def test_all_metadata():
    tree = build_tree(map(int, TEST_INPUT.split()))
    assert all_metadata(tree) == 138

def puzzle_input():
    with open("day08_input.txt") as f:
        return map(int, f.read().split())

if __name__ == "__main__":
    ans = all_metadata(build_tree(puzzle_input()))
    print(f"Part 1: the sum of all metadata is {ans}")
