# https://adventofcode.com/2018/day/13

from dataclasses import dataclass
import itertools

CART_DIRECTIONS = {
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0),
    '^': (0, -1),
}

CART_ARROWS = {dxdy: char for char, dxdy in CART_DIRECTIONS.items()}

TURN_LEFT = {
    (1, 0): (0, -1),
    (0, 1): (1, 0),
    (-1, 0): (0, 1),
    (0, -1): (-1, 0),
}

TURN_RIGHT = {after: before for before, after in TURN_LEFT.items()}

@dataclass
class Track:
    lx: int
    ly: int
    ux: int
    uy: int

    def paint(self, canvas):
        canvas[self.lx, self.ly] = canvas[self.ux, self.uy] = "/"
        canvas[self.lx, self.uy] = canvas[self.ux, self.ly] = "\\"
        for x in range(self.lx+1, self.ux):
            canvas[x, self.ly] = canvas[x, self.uy] = "-"
        for y in range(self.ly+1, self.uy):
            canvas[self.lx, y] = canvas[self.ux, y] = "|"

@dataclass
class Cart:
    track: Track
    x: int
    y: int
    dx: int
    dy: int

    def __post_init__(self):
        self.turns = itertools.cycle([TURN_LEFT, None, TURN_RIGHT])

    def paint(self, canvas):
        canvas[self.x, self.y] = CART_ARROWS[self.dx, self.dy]

class Canvas:
    def __init__(self, sizex, sizey):
        self.chars = [[' '] * sizex for _ in range(sizey)]

    def __setitem__(self, coords, char):
        self.chars[coords[1]][coords[0]] = char

    def print(self):
        for line in self.chars:
            print("".join(line))

TEST_INPUT = r"""
/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   
""".lstrip("\n").splitlines()

class World:
    def __init__(self):
        self.tracks = []
        # key: (x, y); value: (horiz track, vert track)
        self.intersections = {}
        # key: (x, y); value: cart
        self.carts = {}

    def read_map(self, lines):
        # key: x coord; value: Track
        columns = {}
        for y, line in enumerate(lines):
            in_span = None
            for x, char in enumerate(line):
                if char in r'\/':
                    if in_span is None:
                        if x in columns:
                            # We are ending a box
                            assert char == "\\"
                            in_span = columns[x]
                        else:
                            assert char == "/"
                            in_span = Track(x, y, None, None)
                            columns[x] = in_span
                    else:
                        if x in columns:
                            # We are ending a box
                            assert char == "/"
                            assert in_span.ux == x
                            in_span.uy = y
                            self.tracks.append(in_span)
                            del columns[in_span.lx]
                            del columns[in_span.ux]
                        else:
                            assert char == "\\"
                            in_span.ux = x
                            columns[x] = in_span
                        in_span = None
                elif char == '+':
                    assert in_span is not None
                    assert columns[x] is not None
                    self.intersections[(x, y)] = (in_span, columns[x])
                elif char in '><^v':
                    if char in '><':
                        track = in_span
                    else:
                        track = columns[x]
                    assert track is not None
                    dx, dy = CART_DIRECTIONS[char]
                    self.carts[x, y] = Cart(track, x, y, dx, dy)

        assert len(columns) == 0

    def print(self):
        maxx = max(t.ux for t in self.tracks)
        maxy = max(t.uy for t in self.tracks)
        canvas = Canvas(maxx+1, maxy+1)
        for t in self.tracks:
            t.paint(canvas)
        for i in self.intersections:
            canvas[i] = "+"
        for c in self.carts.values():
            c.paint(canvas)
        canvas.print()
  
    def tick(self):
        # Put carts in the order they will move
        for cart in sorted(self.carts.values(), key=lambda c: (c.y, c.x)):
            # Advance the cart.
            del self.carts[cart.x, cart.y]
            cart.x += cart.dx
            cart.y += cart.dy
            pos = (cart.x, cart.y)
            if pos in self.carts:
                # COLLISION!
                return cart
            self.carts[pos] = cart

            # If at an intersection, time to turn and switch tracks (maybe).
            crossed_tracks = self.intersections.get(pos)
            if crossed_tracks:
                turn = next(cart.turns)
                if turn:
                    cart.dx, cart.dy = turn[cart.dx, cart.dy]
                    cart.track = crossed_tracks[0 if cart.track == crossed_tracks[1] else 1]

            # If reached a corner, turn.
            else:
                track = cart.track
                if pos == (track.lx, track.ly):
                    if cart.dx == 0:
                        cart.dx, cart.dy = 1, 0
                    else:
                        cart.dx, cart.dy = 0, 1
                elif pos == (track.lx, track.uy):
                    if cart.dx == 0:
                        cart.dx, cart.dy = 1, 0
                    else:
                        cart.dx, cart.dy = 0, -1
                elif pos == (track.ux, track.ly):
                    if cart.dx == 0:
                        cart.dx, cart.dy = -1, 0
                    else:
                        cart.dx, cart.dy = 0, 1
                elif pos == (track.ux, track.uy):
                    if cart.dx == 0:
                        cart.dx, cart.dy = -1, 0
                    else:
                        cart.dx, cart.dy = 0, -1

        return None

def run_until_crash(input_lines, show=False):
    world = World()
    world.read_map(input_lines)
    while True:
        if show:
            world.print()
            print("-"*80)
        result = world.tick()
        if result:
            return result

def test_tick():
    crash_cart = run_until_crash(TEST_INPUT, show=True)
    assert (crash_cart.x, crash_cart.y) == (7, 3)

if __name__ == "__main__":
    with open("day13_input.txt") as f:
        crash_cart = run_until_crash(f)
    print(f"Part 1: the first crash is at {crash_cart.x}, {crash_cart.y}")
