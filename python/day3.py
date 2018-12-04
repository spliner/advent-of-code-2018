import collections
import re

INPUT = '../inputs/day3.txt'
REGEX = r'#(?P<id>\d+)\s@\s(?P<x>\d+),(?P<y>\d+):\s(?P<w>\d+)x(?P<h>\d+)'

Claim = collections.namedtuple('Claim', 'id x y width height')


def part1(claims):
    print(claims)


def parsefile(path, regex):
    with open(path, mode='r') as data:
        return [parseline(l, regex) for l in data.readlines()]


def parseline(line, regex):
    match = re.match(regex, line)
    groups = match.groupdict()
    return Claim(int(groups['id']), int(groups['x']), int(groups['y']), int(groups['w']), int(groups['h']))


if __name__ == '__main__':
    claims = parsefile(INPUT, REGEX)
    part1_test_data = [
        Claim(1, 1, 3, 4, 4),
        Claim(2, 3, 1, 4, 4),
        Claim(3, 5, 5, 2, 2)
    ]
    part1(claims)
