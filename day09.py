# https://adventofcode.com/2018/day/9
# Nudgy bookkeeping

import itertools

import pytest

class Game:
    def __init__(self, nplayers, last_marble):
        self.nplayers = nplayers
        self.scores = [0] * nplayers
        self.last_marble = last_marble
        self.circle = None
        self.current = 0

    def high_score(self):
        return max(self.scores)

    def print_circle(self):
        for i, marble in enumerate(self.circle):
            if i == self.current:
                print(f"({marble:2d})", end='')
            else:
                print(f" {marble:2d} ", end='')
        print()

    def play(self):
        # Place the 0th marble
        self.circle = [0]
        self.current = 0
        marbles = range(1, self.last_marble + 1)
        player_turns = itertools.cycle(range(self.nplayers))
        for marble, player in zip(marbles, player_turns):
            #self.print_circle()
            if marble % 23:
                # Not a multiple of 23: the usual case
                i = (self.current + 2) % len(self.circle)
                if i == 0:
                    i = len(self.circle)
                self.circle[i:i] = [marble]
                self.current = i
            else:
                # Special case
                self.scores[player] += marble
                i = (self.current - 7) % len(self.circle)
                self.scores[player] += self.circle[i]
                del self.circle[i]
                self.current = i


@pytest.mark.parametrize("nplayers, last_marble, high_score", [
    (9, 25, 32),
    (10, 1618, 8317),
    (13, 7999, 146373),
    (17, 1104, 2764),
    (21, 6111, 54718),
    (30, 5807, 37305),
])
def test_game(nplayers, last_marble, high_score):
    game = Game(nplayers, last_marble)
    game.play()
    assert game.high_score() == high_score

INPUT = (468, 71010)

if __name__ == "__main__":
    game = Game(*INPUT)
    game.play()
    print(f"Part 1: the winning elf's score is {game.high_score()}")
