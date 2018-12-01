# https://adventofcode.com/2018/day/1

with open("day01_input.txt") as f:
    result = sum(map(eval, f))

print(f"The resulting frequency is {result}")
