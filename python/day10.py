import re
import pygame
import collections
import pprint
import time

from typing import List

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
BACKGROUND_COLOR = (0, 0, 0)
POINT_COLOR = (255, 0, 255)
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


def get_bounds(points):
    x1 = min(points, key=lambda p: p.position.x).position.x
    y1 = min(points, key=lambda p: p.position.y).position.y
    start = min([x1, y1])

    x2 = max(points, key=lambda p: p.position.x).position.x
    y2 = max(points, key=lambda p: p.position.y).position.y
    end = max([x2, y2])
    return (Coordinate(start, start), Coordinate(end, end))


def draw_point(point, current_step, screen, bounds, viewport_bounds):
    w = abs(bounds[0].x) + abs(bounds[1].x)
    h = abs(bounds[0].y) + abs(bounds[1].y)
    position = point.get_position(current_step)
    origin_x = viewport_bounds[1].x / 2
    origin_y = viewport_bounds[1].y / 2
    new_x = (position.x + abs(bounds[0].x)) * SCREEN_WIDTH / w
    new_y = (position.y + abs(bounds[0].y)) * SCREEN_HEIGHT / h
    return Coordinate(round(new_x), round(new_y))


if __name__ == '__main__':
    points = parsefile(INPUT, REGEX)
    bounds = get_bounds(points)
    viewport_bounds = (Coordinate(0, 0), Coordinate(
        SCREEN_WIDTH, SCREEN_HEIGHT))
    print(bounds)
    print(len(points))

    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    fontsize = 10
    font = pygame.font.SysFont('Arial', fontsize)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    current_step = 0
    steps = 1
    done = False
    keys = {
        pygame.K_DOWN: False,
        pygame.K_UP: False,
        pygame.K_LEFT: False,
        pygame.K_RIGHT: False
    }

    foo = [(p, draw_point(p, current_step, screen, bounds, viewport_bounds)) for p in points]
    bar = sorted(foo, key=lambda f: f[1].x)
    baz = [(p, p.get_position(1000)) for p in points]
    pprint.pprint(baz)
    # for b in baz:
    #     pygame.draw.rect(screen, POINT_COLOR, (b[0].x, b[0].y, 1, 1))

    # pprint.pprint(bar)
    # for i, f in enumerate(foo):
    #     text = font.render(f'{f[0].position.x}, {f[0].position.y}', False, FONT_COLOR)
    #     screen.blit(text, (f[1].x, f[1].y))
    #     pygame.display.flip()
    #     pygame.time.wait(1000)

    while not done:
        screen.fill(BACKGROUND_COLOR)
        text = font.render('Right arrow: next step', False, FONT_COLOR)
        rightarrow_rect = text.get_rect()
        rightarrow_rect.left = PADDING
        rightarrow_rect.top = SCREEN_HEIGHT - rightarrow_rect.height - PADDING
        screen.blit(text, rightarrow_rect)

        text = font.render('Left arrow: previous step', False, FONT_COLOR)
        leftarrow_rect = text.get_rect()
        leftarrow_rect.left = rightarrow_rect.left
        leftarrow_rect.top = rightarrow_rect.top - leftarrow_rect.height
        screen.blit(text, leftarrow_rect)

        text = font.render('Up arrow: increase step', False, FONT_COLOR)
        uparrow_rect = text.get_rect()
        uparrow_rect.left = SCREEN_WIDTH - uparrow_rect.width - PADDING
        uparrow_rect.top = SCREEN_HEIGHT - rightarrow_rect.height - PADDING
        screen.blit(text, uparrow_rect)

        text = font.render('Down arrow: decrease step', False, FONT_COLOR)
        downarrow_rect = text.get_rect()
        downarrow_rect.left = SCREEN_WIDTH - downarrow_rect.width - PADDING
        downarrow_rect.top = uparrow_rect.top - downarrow_rect.height
        screen.blit(text, downarrow_rect)

        text = font.render(f'Current step: {current_step}', False, FONT_COLOR)
        screen.blit(text, (PADDING, 0))

        text = font.render(f'Steps: {steps}', False, FONT_COLOR)
        step_rect = text.get_rect()
        step_rect.left = SCREEN_WIDTH - step_rect.width - PADDING
        step_rect.top = PADDING
        screen.blit(text, step_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    keys[pygame.K_UP] = True
                elif event.key == pygame.K_DOWN:
                    keys[pygame.K_DOWN] = True
                elif event.key == pygame.K_RIGHT:
                    keys[pygame.K_RIGHT] = True
                elif event.key == pygame.K_LEFT:
                    keys[pygame.K_LEFT] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    keys[pygame.K_UP] = False
                elif event.key == pygame.K_DOWN:
                    keys[pygame.K_DOWN] = False
                elif event.key == pygame.K_RIGHT:
                    keys[pygame.K_RIGHT] = False
                elif event.key == pygame.K_LEFT:
                    keys[pygame.K_LEFT] = False

        if keys[pygame.K_UP]:
            steps += 1
        elif keys[pygame.K_DOWN]:
            steps = max(1, steps - 1)
        elif keys[pygame.K_RIGHT]:
            current_step += steps
        elif keys[pygame.K_LEFT]:
            current_step = max(0, current_step - steps)

        foo = [(p, draw_point(p, current_step, screen, bounds, viewport_bounds)) for p in points]
        for f in foo:
            text = font.render(f'{f[0].velocity.x}, {f[0].velocity.y}', False, FONT_COLOR)
            screen.blit(text, (f[1].x, f[1].y))
            # pygame.draw.rect(screen, POINT_COLOR, (f[1].x, f[1].y, 1, 1))

        pygame.display.flip()
        clock.tick(10)
