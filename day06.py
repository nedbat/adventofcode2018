# https://adventofcode.com/2018/day/6

import collections
import itertools
import string


def taxi_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def read_points(lines):
    return [eval(line) for line in lines if line.strip()] 

TEST_INPUT = """\
    1, 1
    1, 6
    8, 3
    3, 4
    5, 5
    8, 9
    """.splitlines()

def bounds(points):
    """Return minx,maxx,miny,maxy of the grid that encloses all points, plus one extra all around."""
    return (
        min(p[0] for p in points) - 1,
        max(p[0] for p in points) + 1,
        min(p[1] for p in points) - 1,
        max(p[1] for p in points) + 1,
        )

def grid_points(minx, maxx, miny, maxy):
    """Yield all points in the grid."""
    yx = itertools.product(range(miny, maxy+1), range(minx, maxx+1)) 
    return ((x, y) for y, x in yx)

def test_grid_points():
    assert len(list(grid_points(*bounds(read_points(TEST_INPUT))))) == 110

def map_the_grid(points):
    grid = {}   # Maps point to index of nearest point, or None for tie

    # Fill in the grid.
    for gpt in grid_points(*bounds(points)):
        distances = [(taxi_dist(gpt, pt), ipt) for ipt, pt in enumerate(points)]
        distances.sort()
        if distances[0][0] != distances[1][0]:
            # Not a tie.
            grid[gpt] = distances[0][1]

    return grid

labels = string.ascii_uppercase

def show_grid(points, grid):
    point_names = {pt: ipt for ipt, pt in enumerate(points)}
    y = None
    for gpt in grid_points(*bounds(points)):
        if gpt[1] != y:
            print()
            y = gpt[1]
        if gpt in point_names:
            print(labels[point_names[gpt]], end='')
        else:
            nearest = grid.get(gpt)
            if nearest is None:
                print(".", end='')
            else:
                print(labels[nearest].lower(), end='')
    print()

def largest_finite_area(points, grid):
    # Find the infinite areas. Whatever points the grid edges are nearest,
    # are infinite.
    infinite_points = set()
    minx, maxx, miny, maxy = bounds(points)
    for x in range(minx, maxx+1):
        for y in [miny, maxy]:
            infinite_points.add(grid.get((x, y)))
    for y in range(miny, maxy+1):
        for x in [minx, maxx]:
            infinite_points.add(grid.get((x, y)))

    # Total up the areas for each point.
    count = collections.Counter()
    count.update(grid.values())
    for infpt in infinite_points:
        del count[infpt]

    return count.most_common(1)[0][1]

def test_largest_finite_area():
    test_points = read_points(TEST_INPUT)
    grid = map_the_grid(test_points)
    ans = largest_finite_area(test_points, grid)
    assert ans == 17

def puzzle_input():
    with open("day06_input.txt") as f:
        return read_points(f)

if __name__ == "__main__":
    points = puzzle_input()
    grid = map_the_grid(points)
    ans = largest_finite_area(points, grid)
    print(f"Part 1: the largest finite area is {ans}")
