import re
import itertools
import collections
import pprint

from typing import List
from day10_ui import Day10UIHelper

SCREEN_WIDTH = 600
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

    def get_coordinate(self, step: int) -> Coordinate:
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


def get_bounds(coordinates):
    min_x = min(c.x for c in coordinates)
    min_y = min(c.y for c in coordinates)
    max_x = max(c.x for c in coordinates)
    max_y = max(c.y for c in coordinates)
    return Coordinate(min_x, min_y), Coordinate(max_x, max_y)


def get_viewport_coordinates(point, current_step, tx, ty):
    coordinate = point.get_coordinate(current_step)
    return Coordinate(tx(coordinate.x), ty(coordinate.y))


def run():
    current_step = 0
    steps = 1

    points = parsefile(INPUT, REGEX)
    coordinates = [p.get_coordinate(current_step) for p in points]
    bounds = get_bounds(coordinates)

    width = abs(bounds[0].x) + abs(bounds[1].x)
    height = abs(bounds[0].y) + abs(bounds[1].y)
    aspect_ratio = width / height
    viewport_width = SCREEN_WIDTH
    viewport_height = round(viewport_width * aspect_ratio)
    viewport_scale = viewport_width / width

    ui_helper = Day10UIHelper(FONT_COLOR,
                              FONTSIZE,
                              PADDING,
                              viewport_width,
                              viewport_height)

    def tx(x):
        return x * viewport_scale

    def ty(y):
        return y * viewport_scale

    while not ui_helper.done:
        ui_helper.onloop(BACKGROUND_COLOR, current_step, steps)

        if ui_helper.is_up_pressed():
            steps += 1
        elif ui_helper.is_down_pressed():
            steps = max(1, steps - 1)
        elif ui_helper.is_right_pressed():
            current_step += steps
        elif ui_helper.is_left_pressed():
            current_step = max(0, current_step - steps)

        coordinates = [p.get_coordinate(current_step) for p in points]
        bounds = get_bounds(coordinates)
        width = abs(bounds[0].x) + abs(bounds[1].x)
        viewport_scale = viewport_width / width

        viewport_coordinates = [get_viewport_coordinates(p, current_step, tx, ty) for p in points]
        for coordinate in viewport_coordinates:
            ui_helper.draw_coordinate(coordinate, POINT_COLOR)

        ui_helper.draw()


if __name__ == '__main__':
    run()
