import re
import collections
import pprint

from typing import List
from day10_ui import Day10UIHelper

SCREEN_WIDTH = 2000
BACKGROUND_COLOR = (0, 0, 0)
POINT_COLOR = (255, 0, 255)
FONTSIZE = 10
FONT_COLOR = (255, 255, 255)
PADDING = 5
INPUT = '../inputs/day10.txt'
TEST_INPUT = '../inputs/day10_test.txt'
REGEX = r'position=<\s?(?P<pos_x>-?\d+),\s+(?P<pos_y>-?\d+)>\svelocity=<\s?(?P<vel_x>-?\d+),\s+(?P<vel_y>-?\d+)>'

Coordinate = collections.namedtuple('Coordinate', 'x y')


class Point(object):
    def __init__(self, position: Coordinate, velocity: Coordinate):
        self.position = position
        self.velocity = velocity

    def get_position(self, step: int) -> Coordinate:
        pos_x = self.position.x + self.velocity.x * step
        pos_y = self.position.y + self.velocity.y * step
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


def get_bounds(points, current_step):
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0
    for pont in points:
        position = point.get_position(current_step)
        if position.x < min_x:
            min_x = position.x
        if position.y < min_y:
            min_y = position.y
        if position.x > max_x:
            max_x = position.x
    x1 = min(points, key=lambda p: p.position.x).position.x
    y1 = min(points, key=lambda p: p.position.y).position.y
    x2 = max(points, key=lambda p: p.position.x).position.x
    y2 = max(points, key=lambda p: p.position.y).position.y
    return (Coordinate(x1, y1), Coordinate(x2, y2))


def get_viewport_coordinate(point, current_step, bounds, viewport_scale, tx, ty):
    position = point.get_position(current_step)
    new_x = (position.x + bounds[0].x * -1) * viewport_scale
    new_y = (position.y + bounds[0].y * -1) * viewport_scale
    return Coordinate(round(tx(position.x)), round(ty(position.y)))


if __name__ == '__main__':
    points = parsefile(INPUT, REGEX)
    bounds = get_bounds(points)

    width = abs(bounds[0].x) + abs(bounds[1].x)
    height = abs(bounds[0].y) + abs(bounds[1].y)
    aspect_ratio = width / height

    viewport_width = SCREEN_WIDTH
    viewport_height = round(viewport_width * aspect_ratio)
    viewport_scale = viewport_width / width
    current_step = 0
    steps = 1

    def tx(x): return viewport_width * (x + bounds[1].x) / width

    def ty(y): return viewport_height * (bounds[1].y - y) / height

    uiHelper = Day10UIHelper(FONT_COLOR,
                             FONTSIZE,
                             PADDING,
                             viewport_width,
                             viewport_height)

    for point in points:
        coordinate = get_viewport_coordinate(point,
                                             current_step,
                                             bounds,
                                             viewport_scale,
                                             tx,
                                             ty)
        print(f'{coordinate.x}, {coordinate.y}')
    while not uiHelper.done:
        uiHelper.onloop(BACKGROUND_COLOR, current_step, steps)

        if uiHelper.is_up_pressed():
            steps += 1
        elif uiHelper.is_down_pressed():
            steps = max(1, steps - 1)
        elif uiHelper.is_right_pressed():
            current_step += steps
        elif uiHelper.is_left_pressed():
            current_step = max(0, current_step - steps)

        bounds = get_bounds(points, current_step)
        viewport_coordinates = [
            get_viewport_coordinate(
                p, current_step, bounds, viewport_scale, tx, ty)
            for p in points]
        for coordinate in viewport_coordinates:
            uiHelper.draw_coordinate(coordinate, POINT_COLOR)

        uiHelper.draw()
