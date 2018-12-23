from enum import Enum
from typing import List

INPUT_TEST1 = '../inputs/day13_test1.txt'
INPUT_TEST2 = '../inputs/day13_test2.txt'
INPUT = '../inputs/day13.txt'


class Cart(object):
    def __init__(self, id: int, x: int, y: int, direction: str, tile: str):
        self.id = id
        self.x = x
        self.y = y
        self.direction = direction
        self.tile = tile
        self.intersection_count = 0
        self.crashed = False

    def move(self, track, carts):
        if self.crashed:
            return

        if self.direction == '>':
            self.x += 1
        elif self.direction == '<':
            self.x -= 1
        elif self.direction == '^':
            self.y -= 1
        elif self.direction == 'v':
            self.y += 1

        new_tile = track[self.y][self.x]
        if new_tile == '/':
            if self.direction == '>':
                self.direction = '^'
            elif self.direction == '<':
                self.direction = 'v'
            elif self.direction == '^':
                self.direction = '>'
            elif self.direction == 'v':
                self.direction = '<'
        elif new_tile == '\\':
            if self.direction == '>':
                self.direction = 'v'
            elif self.direction == '<':
                self.direction = '^'
            elif self.direction == '^':
                self.direction = '<'
            elif self.direction == 'v':
                self.direction = '>'
        elif new_tile == '+':
            intersection_turn = self.intersection_count % 3
            # Turn left
            if intersection_turn == 0:
                if self.direction == '^':
                    self.direction = '<'
                elif self.direction == 'v':
                    self.direction = '>'
                elif self.direction == '<':
                    self.direction = 'v'
                elif self.direction == '>':
                    self.direction = '^'
            # Turn right
            elif intersection_turn == 2:
                if self.direction == '^':
                    self.direction = '>'
                elif self.direction == 'v':
                    self.direction = '<'
                elif self.direction == '<':
                    self.direction = '^'
                elif self.direction == '>':
                    self.direction = 'v'
            self.intersection_count += 1

        crashes = [c for c in carts
                   if c.id != self.id and c.x == self.x and c.y == self.y]
        if crashes:
            self.crashed = True
            self.direction = 'x'
            for c in [c for c in crashes if not c.crashed]:
                c.crashed = True
                c.direction = 'x'

        self.tile = new_tile


def parsefile(input) -> List:
    track = []
    carts = []
    with open(input, mode='r') as data:
        lines = [l.rstrip() for l in data.readlines()]
        for y, line in enumerate(lines):
            line_tiles = []
            for x, tile in enumerate(line):
                actual_tile = tile
                if tile == '>' or tile == '<' or tile == '^' or tile == 'v':
                    if tile == '>' or tile == '<':
                        actual_tile = '-'
                    else:
                        actual_tile = '|'
                    cart = Cart(len(carts) + 1, x, y, tile, actual_tile)
                    carts.append(cart)
                line_tiles.append(actual_tile)
            track.append(line_tiles)
        return track, carts


def print_track(track: List[List[str]], carts: List[Cart]):
    print('\n======')
    for y, line in enumerate(track):
        toprint = ''
        for x, tile in enumerate(line):
            cart = next((c for c in carts if c.x == x and c.y == y), None)
            toprint += cart.direction if cart else tile
        print(toprint)
    print('======\n')


def part1(track: List[List[str]], carts: List[Cart]):
    crashes = []
    # print_track(track, carts)
    while not crashes:
        tick(track, carts)
        crashes = [c for c in carts if c.crashed]
        # print_track(track, carts)
        # input()
    print([(c.x, c.y) for c in crashes])

 
def tick(track: List[List[str]], carts: List[Cart]):
    ordered_carts = sorted(carts, key=lambda c: (c.x, -c.y))
    for cart in ordered_carts:
        cart.move(track, carts)


def main():
    track1, carts1 = parsefile(INPUT_TEST1)
    # part1(track1, carts1)
    track2, carts2 = parsefile(INPUT_TEST2)
    # part1(track2, carts2)
    track3, carts3 = parsefile(INPUT)
    part1(track3, carts3)


if __name__ == "__main__":
    main()
