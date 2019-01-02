from __future__ import annotations
from enum import Enum
from typing import List
import collections
import heapq


class MapGrid(object):
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.walls = []
        self.units = []
        self.unit_positions = []
        self.position_availability = {}

    def refresh_unit_positions(self):
        self.unit_positions = [(u.x, u.y) for u in self.units]

    def is_available(self, position):
        if position not in self.position_availability:
            (x, y) = position
            is_passable = position not in self.walls
            in_bounds = 0 <= x < self.width and 0 <= y < self.height
            self.position_availability[position] = is_passable and in_bounds
        is_available = self.position_availability[position]
        return is_available and position not in self.unit_positions

    def neighbors(self, position):
        (x, y) = position
        results = [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
        return filter(self.is_available, results)

    def cost(self, from_node, to_node):
        return 1

    def units_of_type(self, unit_type: UnitType):
        return [u for u in self.units if u.type == unit_type]

    def __repr__(self):
        lines = []
        for y in range(self.height):
            line = ''
            for x in range(self.width):
                line += '#' if (x, y) in self.walls else '.'
            lines.append(line)
        return '\n'.join(lines)

    def __str__(self):
        return self.__repr__()


class PriorityQueue(object):
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class UnitType(Enum):
    ELF = 1,
    GOBLIN = 2


class Unit(object):
    def __init__(self, x: int, y: int, unit_type: UnitType):
        self.x = x
        self.y = y
        self.type = unit_type
        self.hp = 200
        self.attack_power = 3

    def __str__(self):
        return f'{self.type}@({self.x}, {self.y}) => {self.hp}HP'
