import collections

INPUT = '../inputs/day6.txt'
TEST_INPUT = '../inputs/day6_test.txt'

Point = collections.namedtuple('Point', 'x y')
Rectangle = collections.namedtuple('Rectangle', 'p1 p2')


def part1(points):
    bounds = get_bounds(points)
    print(bounds)
    return 10


def get_bounds(points):
    x1 = min(points, key=lambda p: p.x)
    y1 = min(points, key=lambda p: p.y)
    x2 = max(points, key=lambda p: p.x)
    y2 = max(points, key=lambda p: p.y)

    return Rectangle(Point(x1, y1), Point(x2, y2))


def parse_file(path):
    with open(path, mode='r') as data:
        return [parse_line(l.rstrip()) for l in data.readlines()]


def parse_line(line):
    coordinates = [int(i) for i in line.split(', ')]
    return Point(coordinates[0], coordinates[1])


if __name__ == '__main__':
    test_coordinates = parse_file(TEST_INPUT)
    print(test_coordinates)
    assert part1(test_coordinates) == 17
