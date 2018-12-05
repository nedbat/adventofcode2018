"""Generate a new data set for day 2."""

# I was disappointed that the brute force approach worked for day 2. I had
# expected that a cleverer algorithm would be needed.  I knew what algorithm to
# use, but didn't have a data set big enough to show O(n) working where O(n**2)
# didn't.  This generates me a larger data set.

import itertools
import random
import string
import sys

alphabet = "abcdefghijklmnopqrstuvwyz"  # no x
different = "x"

def change_at(s, pos):
    other = s[:pos] + different + s[pos+1:]
    return other

def change_at_many(s, poss):
    for pos in poss:
        s = change_at(s, pos)
    return s

def generate(length):
    # Pick a random word.
    start = "".join(random.choice(alphabet) for _ in range(length))
    yield start

    # Change it in one position.
    pos1 = random.randint(0, length-1)
    other = change_at(start, pos1)
    yield other

    # The other words will be changed in the other positions, at least two of
    # them.
    change_places = list(set(range(length)) - set([pos1]))

    # We'll generate many changed words by changing letters to x in different
    # positions.  We'll choose all combinations of possible positions, first
    # two of them, then four, six, etc.  We can't change in two and then three
    # positions, because changing at (1, 2) and then (1, 2, 3) would give us a
    # pair that differs by one character.
    for num_changes in range(2, 10, 2):
        for poss in itertools.combinations(change_places, num_changes):
            yield change_at_many(start, poss)

if __name__ == "__main__":
    length = 20
    number = int(sys.argv[1])

    output = list(itertools.islice(generate(length), number))
    random.shuffle(output)
    print("\n".join(output))
