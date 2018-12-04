import collections
import re

INPUT = '../inputs/day3.txt'
REGEX = r'#(?P<id>\d+)\s@\s(?P<x>\d+),(?P<y>\d+):\s(?P<w>\d+)x(?P<h>\d+)'

Point = collections.namedtuple('Point', 'x y')
Rectangle = collections.namedtuple('Rectangle', 'p1 p2')
Claim = collections.namedtuple('Claim', 'id bounds width height')


def part1(claims):
    for index, claim in enumerate(claims):
        for comparison in claims[index + 1:]:
            intersection = calculate_intersection(
                claim.bounds, comparison.bounds)
            isvalid = isvalid_rectangle(intersection)


def calculate_intersection(rectangle1, rectangle2):
    x1 = max(rectangle1.p1.x, rectangle2.p1.x)
    y1 = max(rectangle1.p1.y, rectangle2.p1.y)
    x2 = max(rectangle1.p2.x, rectangle2.p2.x)
    y2 = max(rectangle1.p2.y, rectangle2.p2.y)
    return Rectangle(Point(x1, y1), Point(x2, y2))


def isvalid_rectangle(rectangle):
    # TODO: Actually check if rectangle is valid
    return True


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
    return Claim(int(groups['id']), Rectangle(Point(x1, y1), Point(x2, y2)), w, h)


if __name__ == '__main__':
    claims = parsefile(INPUT, REGEX)
    part1_test_data = [
        Claim(1, Rectangle(Point(1, 3), Point(5, 8)), 4, 4),
        Claim(2, Rectangle(Point(3, 1), Point(8, 5)), 4, 4),
        Claim(3, Rectangle(Point(5, 5), Point(7, 7)), 2, 2)
    ]
    part1(claims)
