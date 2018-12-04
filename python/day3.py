import collections
import re

INPUT = '../inputs/day3.txt'
REGEX = r'#(?P<id>\d+)\s@\s(?P<x>\d+),(?P<y>\d+):\s(?P<w>\d+)x(?P<h>\d+)'

Point = collections.namedtuple('Point', 'x y')
Rectangle = collections.namedtuple('Rectangle', 'p1 p2')
Claim = collections.namedtuple('Claim', 'id bounds width height')


def part1(claims):
    intersections_points = set()
    for index, claim in enumerate(claims):
        for comparison in claims[index + 1:]:
            intersection = calculate_intersection(
                claim.bounds, comparison.bounds)
            if not intersection:
                continue
            points = get_all_points(intersection)
            intersections_points.update(points)
    return len(intersections_points)


def calculate_intersection(rectangle1, rectangle2):
    x1 = max(rectangle1.p1.x, rectangle2.p1.x)
    y1 = max(rectangle1.p1.y, rectangle2.p1.y)
    x2 = min(rectangle1.p2.x, rectangle2.p2.x)
    y2 = min(rectangle1.p2.y, rectangle2.p2.y)
    intersection = Rectangle(Point(x1, y1), Point(x2, y2))
    isvalid = intersection.p1.x <= intersection.p2.x and intersection.p1.y <= intersection.p2.y
    if not isvalid:
        return None
    return intersection


def get_all_points(rectangle):
    points = []
    point = rectangle.p1
    while point.x <= rectangle.p2.x and point.y <= rectangle.p2.y:
        points.append(point)
        if point.x < rectangle.p2.x:
            point = Point(point.x + 1, point.y)
        else:
            point = Point(rectangle.p1.x, point.y + 1)
    return points


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
    x2 = x1 + w - 1
    y2 = y1 + h - 1
    return Claim(int(groups['id']), Rectangle(Point(x1, y1), Point(x2, y2)), w, h)


if __name__ == '__main__':
    lines = [
        '#1 @ 1,3: 4x4',
        '#2 @ 3,1: 4x4',
        '#3 @ 5,5: 2x2'
    ]
    part1_test_data = [parseline(l, REGEX) for l in lines]
    assert part1(part1_test_data) == 4

    claims = parsefile(INPUT, REGEX)
    area = part1(claims)
    print(area)
