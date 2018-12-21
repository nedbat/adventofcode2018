# https://adventofcode.com/2018/day/20/input

import pytest

DIRS = {
    'N': (0, -1),
    'E': (1, 0),
    'S': (0, 1),
    'W': (-1, 0),
}

class Atom:
    def __init__(self):
        self.atom = ""

    def __repr__(self):
        return self.atom

    def depth(self):
        return 1

    def visit(self, tips, grid):
        next_tips = set()
        for x, y in tips:
            for c in self.atom:
                dist = grid[x, y]
                dx, dy = DIRS[c]
                x += dx
                y += dy
                if (x, y) not in grid:
                    grid[x, y] = dist + 1
            next_tips.add((x, y))
        return next_tips

class Compound:
    def __init__(self):
        self.elts = []

    def __repr__(self):
        return f"{self.__class__.__name__}(" + ", ".join(map(repr, self.elts)) + ")"

    def depth(self):
        return max(e.depth() for e in self.elts) + 1
        # Can't use a comprehension, it adds an extra stack frame, blowing the
        # recursion limit.
        depths = []
        for e in self.elts:
            depths.append(e.depth())
        return max(depths) + 1

class Seq(Compound):
    def visit(self, tips, grid):
        for e in self.elts:
            tips = e.visit(tips, grid)
        return tips

class Opt(Compound):
    def visit(self, tips, grid):
        next_tips = set()
        for e in self.elts:
            next_tips.update(e.visit(tips, grid))
        return next_tips

class Parser:
    def __init__(self, regex):
        self.chars = iter(regex)
        self.eat()

    def eat(self):
        self.char = next(self.chars, "")

    def opt(self):
        """opt: LPAREN seq (PIPE seq)* RPAREN"""
        assert self.char in "^("
        self.eat()

        opt = Opt()
        opt.elts.append(self.seq())
        while self.char == "|":
            self.eat()
            opt.elts.append(self.seq())

        assert self.char in "$)"
        self.eat()

        if len(opt.elts) == 1:
            return opt.elts[0]
        else:
            return opt

    def seq(self):
        """seq: ( atom | opt )+"""
        seq = Seq()
        while True:
            if self.char in "NEWS":
                seq.elts.append(self.atom())
            elif self.char == "(":
                seq.elts.append(self.opt())
            else:
                break
        if len(seq.elts) == 0:
            return Atom()
        elif len(seq.elts) == 1:
            return seq.elts[0]
        else:
            return seq

    def atom(self):
        atom = Atom()
        while self.char in "NEWS":
            atom.atom += self.char
            self.eat()
        return atom

def parse(regex):
    parser = Parser(regex)
    val = parser.opt()
    return val

def test_input():
    with open("day20_input.txt") as f:
        return parse(f.read())

def visit_rooms(paths):
    rooms = {(0, 0): 0}
    tips = {(0, 0)}
    end_tips = paths.visit(tips, rooms)
    return rooms

def longest_path(paths):
    rooms = visit_rooms(paths)
    return max(rooms.values())

@pytest.mark.parametrize("regex, ans", [
    ("^WNE$", 3),
    ("^ENWWW(NEEE|SSE(EE|N))$", 10),
    ("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$", 18),
    ("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$", 23),
    ("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$", 31),
])
def test_longest_path(regex, ans):
    assert longest_path(parse(regex)) == ans

if __name__ == "__main__":
    ans = longest_path(test_input())
    print(f"Part 1: the shortest path to the farthest room is {ans} doors")
