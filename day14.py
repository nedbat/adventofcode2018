# https://adventofcode.com/2018/day/14

import pytest

class Board:
    def __init__(self):
        self.recipes = [3, 7]
        self.elf1 = 0
        self.elf2 = 1

    def tick(self):
        score1 = self.recipes[self.elf1]
        score2 = self.recipes[self.elf2]
        self.recipes.extend(map(int, str(score1 + score2)))
        self.elf1 = (self.elf1 + score1 + 1) % len(self.recipes)
        self.elf2 = (self.elf2 + score2 + 1) % len(self.recipes)

def board_result(steps):
    board = Board()
    for _ in range(steps+10):
        #print(" ".join(map(str, board.recipes)))
        board.tick()
    return "".join(map(str, board.recipes[steps:steps+10]))

@pytest.mark.parametrize("steps, result", [
    (9, "5158916779"),
    (5, "0124515891"),
    (18, "9251071085"),
    (2018, "5941429882"),
])
def test_board_results(steps, result):
    assert board_result(steps) == result

INPUT = 74501

if __name__ == "__main__":
    ans = board_result(INPUT)
    print(f"Part 1: the scores are {ans}")

def find_scores(scores):
    scores = list(map(int, scores))
    board = Board()
    while True:
        # 
        if board.recipes[-len(scores):] == scores:
            return len(board.recipes) - len(scores)
        if board.recipes[-(len(scores)+1):-1] == scores:
            return len(board.recipes) - len(scores) - 1
        board.tick()

@pytest.mark.parametrize("scores, result", [
    ("51589", 9),
    ("01245", 5),
    ("92510", 18),
    ("59414", 2018),
])
def test_find_scores(scores, result):
    assert find_scores(scores) == result

INPUT = "074501"

if __name__ == "__main__":
    ans = find_scores(INPUT)
    print(f"Part 2: {ans} recipes appear before {INPUT}")
