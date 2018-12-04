import re

INPUT = '../inputs/day3.txt'
REGEX = r'#(?P<id>\d+)\s@\s(?P<x>\d+),(?P<y>\d+):\s(?P<w>\d+)x(?P<h>\d+)'


def part1(claims):
    print(claims)


def parsefile(path, regex):
    with open(path, mode='r') as data:
        return [parseline(l, regex) for l in data.readlines()]


def parseline(line, regex):
    match = re.match(regex, line)
    groups = match.groupdict()
    groupid = int(groups['id'])
    x = int(groups['x'])
    y = int(groups['y'])
    width = int(groups['w'])
    height = int(groups['h'])
    return (groupid, x, y, width, height)


if __name__ == '__main__':
    claims = parsefile(INPUT, REGEX)
    part1(claims)
