import re
import collections

from typing import List

INPUT = '../inputs/day10.txt'
TEST_INPUT = '../inputs/day10_test.txt'
REGEX = r'position=<\s?(?P<pos_x>-?\d+),\s+(?P<pos_y>-?\d+)>\svelocity=<\s?(?P<vel_x>-?\d+),\s+(?P<vel_y>-?\d+)>'

Coordinate = collections.namedtuple('Coordinate', 'x y')


class Point(object):
    def __init__(self, position: Coordinate, velocity: Coordinate):
        self.position = position
        self.velocity = velocity

    def get_position(self, elapsed_seconds: int) -> Coordinate:
        pos_x = self.position.x + self.velocity.x * elapsed_seconds
        pos_y = self.position.y + self.velocity.y * elapsed_seconds
        return Coordinate(pos_x, pos_y)

    def __str__(self):
        return f'({self.position.x}, {self.position.y}) @ ({self.velocity.x}, {self.velocity.y})'
    
    def __repr__(self):
        return self.__str__()


def parsefile(path: str, regex: str) -> List[Point]:
    with open(path, mode='r') as data:
        return [parseline(l.rstrip(), regex) for l in data.readlines() if l]


def parseline(line: str, regex: str) -> Point:
    match = re.match(regex, line).groupdict()
    pos_x = int(match['pos_x'])
    pos_y = int(match['pos_y'])
    vel_x = int(match['vel_x'])
    vel_y = int(match['vel_y'])
    return Point(Coordinate(pos_x, pos_y), Coordinate(vel_x, vel_y))


if __name__ == '__main__':
    test_points = parsefile(TEST_INPUT, REGEX)
    print(test_points)
