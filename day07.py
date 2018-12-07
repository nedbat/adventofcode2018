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

def next_step(requires, remaining, done):
    ready = set()
    for step in remaining:
        needed = requires[step]
        if needed <= done:
            ready.add(step)
    # Find the first ready step
    if ready:
        return min(ready)
    else:
        return None

def order_steps(lines):
    steps = step_names(lines)
    requires = collect_requirements(lines)
    done = set()
    remaining = set(steps)
    while remaining:
        # Find the first ready step
        this_step = next_step(requires, remaining, done)
        yield this_step
        done.add(this_step)
        remaining.remove(this_step)

def test_order_steps():
    assert "".join(order_steps(TEST_INPUT)) == "CABDFE"

def puzzle_input():
    with open("day07_input.txt") as f:
        return f.readlines()

if __name__ == "__main__":
    steps = "".join(order_steps(puzzle_input()))
    print(f"Part 1: steps should be completed in this order: {steps}")

def work_sequence(lines, num_workers, extra_time):
    steps = step_names(lines)
    requires = collect_requirements(lines)
    # workers is a list of workers, each is a pair:
    #   [secs-til-done, step] or None
    workers = [[0, None] for _ in range(num_workers)]
    done = set()
    remaining = set(steps)
    time = 0
    while remaining or len(done) < len(steps):
        # Find something for the idle workers to do.
        for iw, (sec_left, step) in enumerate(workers):
            if sec_left == 0:
                if step is not None:
                    yield time, step
                    done.add(step)
                if remaining:
                    step = next_step(requires, remaining, done)
                    if step is not None:
                        time_to_complete = ord(step) - ord("A") + 1 + extra_time
                        workers[iw] = [time_to_complete, step]
                        remaining.remove(step)
                    else:
                        workers[iw] = [0, None]
        # Find the next time a worker can do something.
        advance = min(sec_left for sec_left, step in workers if step is not None)
        time += advance
        workers = [[t - advance if t > 0 else 0, step] for t, step in workers]

def test_work_sequence():
    assert list(work_sequence(TEST_INPUT, 2, 0)) == [(3, 'C'), (4, 'A'), (6, 'B'), (9, 'F'), (10, 'D'), (15, 'E')]

if __name__ == "__main__":
    work_steps = list(work_sequence(puzzle_input(), 5, 60))
    step_order = "".join(step for t, step in work_steps)
    finish_time = work_steps[-1][0]
    print(f"Part 2: it took {finish_time} seconds to do these steps: {step_order}")
