# https://adventofcode.com/2018/day/11

import itertools

import pytest

class Grid:
    def __init__(self, serial_number):
        self.serial_number = serial_number

    def power_level(self, x, y):
        power = ((x + 10) * y + self.serial_number) * (x + 10)
        hundreds = (power // 100) % 10
        return hundreds - 5

    def squares(self):
        for x, y in range2d(1, 300, 1, 300):
            total = sum(self.power_level(xx, yy) for xx, yy in range2d(x, x+2, y, y+2))
            yield total, x, y

    def best_square(self):
        return max(self.squares())


@pytest.mark.parametrize("serial_number, x, y, power", [
    (8, 3, 5, 4),
    (57, 122, 79, -5),
    (39, 217, 196, 0),
    (71, 101, 153, 4),
])
def test_power_level(serial_number, x, y, power):
    assert Grid(serial_number).power_level(x, y) == power


def range2d(xlo, xhi, ylo, yhi):
    return itertools.product(range(xlo, xhi+1), range(ylo, yhi+1))

@pytest.mark.parametrize("serial_number, x, y, power", [
    (18, 33, 45, 29),
    (42, 21, 61, 30),
])
def test_best_square(serial_number, x, y, power):
    assert Grid(serial_number).best_square() == (power, x, y)

INPUT = 5535

if __name__ == "__main__":
    power, x, y = Grid(INPUT).best_square()
    print(f"Part 1: the fuel cell with the largest total power is at {(x,y)}")


class Grid2(Grid):
    def __init__(self, serial_number):
        super().__init__(serial_number)

        self.total = [[0] * 301 for _ in range(301)]

        for x, y in range2d(1, 300, 1, 300):
            self.total[x][y] = self.total[x][y-1] + self.total[x-1][y] - self.total[x-1][y-1] + self.power_level(x, y)

    def square_total_power(self, x, y, size):
        x -= 1
        y -= 1
        return self.total[x+size][y+size] - self.total[x][y+size] - self.total[x+size][y] + self.total[x][y]

    def squares(self):
        for x, y in range2d(1, 300, 1, 300):
            large = max(x, y)
            for size in range(1, 301-large+1):
                power = self.square_total_power(x, y, size)
                yield (power, x, y, size)

    def best_square(self):
        return max(self.squares())

@pytest.mark.parametrize("serial_number, x, y, size, power", [
    (18, 90, 269, 16, 113),
    (42, 232, 251, 12, 119),
])
def test_grid2(serial_number, x, y, size, power):
    assert Grid2(serial_number).best_square() == (power, x, y, size)


if __name__ == "__main__":
    power, x, y, size = Grid2(INPUT).best_square()
    print(f"Part 2: the square with the largest total power is {(x,y,size)}")
