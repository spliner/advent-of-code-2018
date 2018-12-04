import collections
import re

INPUT = '../inputs/day3.txt'
REGEX = r'#(?P<id>\d+)\s@\s(?P<x>\d+),(?P<y>\d+):\s(?P<w>\d+)x(?P<h>\d+)'

Claim = collections.namedtuple('Claim', 'id x1 y1 x2 y2 width height')


def part1(claims):
    print(claims)


def parsefile(path, regex):
    with open(path, mode='r') as data:
        return [parseline(l, regex) for l in data.readlines()]


def parseline(line, regex):
    match = re.match(regex, line)
    groups = match.groupdict()
    x1 = int(groups['x'])
    y1 = int(groups['y'])
    w = int(groups['w'])
    h = int(groups['h'])
    x2 = x1 + w
    y2 = y1 + h
    return Claim(
        int(groups['id']), x1, y1, x2, y2, w, h)


if __name__ == '__main__':
    claims = parsefile(INPUT, REGEX)
    part1_test_data = [
        Claim(1, 1, 3, 5, 8, 4, 4),
        Claim(2, 3, 1, 8, 5, 4, 4),
        Claim(3, 5, 5, 7, 7, 2, 2)
    ]
    part1(claims)
