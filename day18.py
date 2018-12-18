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

def run_area(lines, gens):
    area = Area()
    area.read(lines)
    area.print()
    for _ in range(gens):
        area = area.tick()
        area.print()
    return area.resource_value()

def test_area():
    assert run_area(TEST_INPUT, 10) == 1147

if __name__ == "__main__":
    with open("day18_input.txt") as f:
        ans = run_area(f, 10)
    print(f"Part 1: the resource value is {ans}")
