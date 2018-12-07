import collections

INPUT = '../inputs/day6.txt'
TEST_INPUT = '../inputs/day6_test.txt'
TEST_MAX_COORDINATE_SUM = 32
MAX_COORDINATE_SUM = 10000

Point = collections.namedtuple('Point', 'x y')
Rectangle = collections.namedtuple('Rectangle', 'p1 p2')


def part1(coordinates):
    distance_count = {}
    infinite_coordonates = []
    for p in coordinates:
        key = get_key(p)
        distance_count[key] = 0

    bounds = get_bounds(coordinates)
    for x in range(bounds.p1.x, bounds.p2.x):
        for y in range(bounds.p1.y, bounds.p2.y):
            current_coordinate = Point(x, y)
            distances = {get_key(c): get_distance(c, current_coordinate)
                         for c in coordinates}
            min_dist_value = min(distances.values())
            min_coordinates = [
                k for k, v in distances.items() if v == min_dist_value]

            # Ignore coordinate min distance is the same for two or more coordinates
            if len(min_coordinates) != 1:
                continue

            min_dist_key = min_coordinates[0]
            if is_out_of_bounds(bounds, current_coordinate):
                infinite_coordonates.append(min_dist_key)
            else:
                distance_count[min_dist_key] = distance_count[min_dist_key] + 1
    counts = {k: v for k, v in distance_count.items()
              if k not in infinite_coordonates}
    return max(counts.values())


def get_key(point):
    return f'{point.x}, {point.y}'


def get_point(key):
    values = key.split(', ')
    return Point(values[0], values[1])


def is_out_of_bounds(bounds, point):
    return point.x <= bounds.p1.x or point.x >= bounds.p2.x or point.y < bounds.p1.y or point.y > bounds.p2.y


def part2(coordinates, max_sum):
    bounds = get_bounds(coordinates)
    coordinate_count = 0
    for x in range(bounds.p1.x, bounds.p2.x):
        for y in range(bounds.p1.y, bounds.p2.y):
            current_coordinate = Point(x, y)
            coordinate_sum = sum([get_distance(p, current_coordinate)
                                  for p in coordinates])
            if coordinate_sum < max_sum:
                coordinate_count += 1
    return coordinate_count


def get_bounds(points):
    x1 = min(points, key=lambda p: p.x).x
    y1 = min(points, key=lambda p: p.y).y
    x2 = max(points, key=lambda p: p.x).x
    y2 = max(points, key=lambda p: p.y).y
    return Rectangle(Point(x1, y1), Point(x2, y2))


def get_distance(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def parse_file(path):
    with open(path, mode='r') as data:
        return [parse_line(l.rstrip()) for l in data.readlines()]


def parse_line(line):
    coordinates = [int(i) for i in line.split(', ')]
    return Point(coordinates[0], coordinates[1])


if __name__ == '__main__':
    test_coordinates = parse_file(TEST_INPUT)
    assert part1(test_coordinates) == 17

    coordinates = parse_file(INPUT)
    result1 = part1(coordinates)
    print(result1)

    assert part2(test_coordinates, TEST_MAX_COORDINATE_SUM) == 16
    result2 = part2(coordinates, MAX_COORDINATE_SUM)
    print(result2)
