# https://adventofcode.com/2018/day/18

import itertools

TEST_INPUT = """\
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
""".splitlines()

OPEN, TREE, LUMBER = ".|#"

def adjacent(x, y):
    yield x-1, y-1
    yield x-1, y
    yield x-1, y+1
    yield x, y-1
    yield x, y+1
    yield x+1, y-1
    yield x+1, y
    yield x+1, y+1

class Area:
    def __init__(self, cells=None):
        self.cells = cells or {}

    def read(self, lines):
        for y, line in enumerate(lines):
            for x, ch in enumerate(line.strip()):
                self.cells[x, y] = ch

    def freeze(self):
        return tuple(sorted(self.cells.items()))

    def tick(self):
        new = {}
        for x, y in self.cells:
            num_open = 0
            num_tree = 0
            num_lumber = 0
            for ax, ay in adjacent(x, y):
                adj = self.cells.get((ax, ay))
                if adj == OPEN:
                    num_open += 1
                elif adj == TREE:
                    num_tree += 1
                elif adj == LUMBER:
                    num_lumber += 1

            this = that = self.cells[x, y]
            if this == OPEN:
                if num_tree >= 3:
                    that = TREE 
            elif this == TREE:
                if num_lumber >= 3:
                    that = LUMBER
            else:
                assert this == LUMBER
                if num_lumber >= 1 and num_tree >= 1:
                    that = LUMBER
                else:
                    that = OPEN
            new[x, y] = that
        return Area(new)

    def print(self):
        print("="*80)
        for y in itertools.count():
            if self.cells.get((0, y)) is None:
                break
            for x in itertools.count():
                this = self.cells.get((x, y))
                if this is None:
                    break
                print(this, end="")
            print()

    def resource_value(self):
        num_tree = sum(1 for thing in self.cells.values() if thing == TREE)
        num_lumber = sum(1 for thing in self.cells.values() if thing == LUMBER)
        return num_tree * num_lumber

def run_area(area, gens, print_every=1):
    for gen in range(gens):
        area = area.tick()
        if gen % print_every == 0:
            area.print()
            print(f"Resource value is {area.resource_value()}")
    return area

def test_area():
    area = Area()
    area.read(TEST_INPUT)
    assert run_area(area, 10).resource_value() == 1147

if __name__ == "__main__":
    area = Area()
    with open("day18_input.txt") as f:
        area.read(f)
    ans = run_area(area, 10).resource_value()
    print(f"Part 1: the resource value after 10 steps is {ans}")

def run_with_history(area, gens):
    history = {area.freeze(): 0}
    zoomed = False
    gen = 0
    while gen < gens:
        gen += 1
        area = area.tick()
        frozen = area.freeze()
        if zoomed:
            assert (gen - history[frozen]) % step == 0
        else:
            if frozen in history:
                # We found a loop, we can zoom ahead
                old = history[frozen]
                print(f"\nGen {gen} is the same as {old}")
                step = gen - old
                nsteps = (gens - gen) // step
                gen += nsteps * step
                zoomed = True
            history[frozen] = gen
    return area

if __name__ == "__main__":
    area = Area()
    with open("day18_input.txt") as f:
        area.read(f)
    ans = run_with_history(area, 1_000_000_000).resource_value()
    print(f"Part 2: the resource value after a billion steps is {ans}")
