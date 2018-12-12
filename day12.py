# https://adventofcode.com/2018/day/12

INITIAL_STATE = "##..#..##.#....##.#..#.#.##.#.#.######..##.#.#.####.#..#...##...#....#....#.##.###..#..###...#...#.."

INPUT = """\
#..#. => .
.#..# => #
..#.# => .
..... => .
.#... => #
#..## => #
..##. => #
#.##. => #
#.#.# => .
###.# => #
.#### => .
..### => .
.###. => .
#.#.. => #
###.. => .
##.#. => .
##..# => .
##.## => .
#.### => .
...## => #
##... => #
####. => .
.#.## => .
#...# => #
.#.#. => #
....# => .
.##.. => .
...#. => .
..#.. => .
#.... => .
.##.# => #
##### => #
"""

TEST_INITIAL_STATE = "#..#.#..##......###...###"

TEST_INPUT = """\
...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
"""

class Automata:
    def __init__(self, input):
        self.rules = {}
        for line in input.splitlines():
            assert line[6:8] == '=>'
            self.rules[line[:5]] = line[9]
        
        # Be sure you can't get something from nothing.
        assert self.produces('.....') == '.'

    def produces(self, current):
        return self.rules.get(current, '.')

class Plants:
    def __init__(self, state, origin=0, gen=0):
        self.state = state
        self.origin = origin
        self.gen = gen

        # We want to be sure to have four dots at each end.
        l = len(self.state)
        s = self.state.lstrip(".")
        self.origin += (l - len(s)) - 4
        self.state = "...." + s.rstrip(".") + "...."

    def print(self):
        skip = (30 + self.origin) * " "
        print(f"{self.gen:3d}: {skip}{self.state}")

    def next(self, automata):
        new = []
        for i in range(len(self.state)-5):
            chunk = self.state[i:i+5]
            new.append(automata.produces(chunk))
        return Plants("".join(new), self.origin+2, self.gen+1)

    def sum(self):
        return sum(i for i, p in enumerate(self.state, start=self.origin) if p == '#')


def sum_after(initial, rules, gens):
    auto = Automata(rules)
    p = Plants(initial)
    for _ in range(gens):
        p = p.next(auto)
    return p.sum()

def test_it():
    assert sum_after(TEST_INITIAL_STATE, TEST_INPUT, 20) == 325

if __name__ == "__main__":
    print(f"Part 1: the sum is {sum_after(INITIAL_STATE, INPUT, 20)}")
