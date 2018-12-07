# https://adventofcode.com/2018/day/7

import collections
import re

import pytest

TEST_INPUT = """\
    Step C must be finished before step A can begin.
    Step C must be finished before step F can begin.
    Step A must be finished before step B can begin.
    Step A must be finished before step D can begin.
    Step B must be finished before step E can begin.
    Step D must be finished before step E can begin.
    Step F must be finished before step E can begin.
    """.splitlines()

def step_names(lines):
    names = set()
    for line in lines:
        pair = re.findall(r" ([A-Z]) ", line)
        if pair:
            names.update(pair)
    return names

def test_step_names():
    assert step_names(TEST_INPUT) == set("ABCDEF")

def collect_requirements(lines):
    requires = collections.defaultdict(set)
    for line in lines:
        pair = re.findall(r" ([A-Z]) ", line)
        if pair:
            requires[pair[1]].add(pair[0])
    return requires

def order_steps(lines):
    steps = step_names(lines)
    requires = collect_requirements(lines)
    steps_done = set()
    steps_remaining = set(steps)
    while steps_remaining:
        # Find the steps that can be done
        steps_ready = set()
        for step in steps_remaining:
            steps_needed = requires[step]
            if steps_needed <= steps_done:
                steps_ready.add(step)
        # Find the first ready step
        this_step = min(steps_ready)
        yield this_step
        steps_done.add(this_step)
        steps_remaining.remove(this_step)

def test_order_steps():
    assert "".join(order_steps(TEST_INPUT)) == "CABDFE"

def puzzle_input():
    with open("day07_input.txt") as f:
        return f.readlines()

if __name__ == "__main__":
    steps = "".join(order_steps(puzzle_input()))
    print(f"Part 1: steps should be completed in this order: {steps}")
