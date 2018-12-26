from enum import Enum
from typing import List
from day15_collections import SimpleGraph, Queue, PriorityQueue, SquareGrid


def bfs1(graph: SimpleGraph, start):
    frontier = Queue()
    frontier.put(start)
    visited = {}
    visited[start] = True

    while not frontier.empty():
        current = frontier.get()
        print(f'Visiting {current}')
        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                frontier.put(neighbor)
                visited[neighbor] = True


example_graph = SimpleGraph()
example_graph.edges = {
    'A': ['B'],
    'B': ['A', 'C', 'D'],
    'C': ['A'],
    'D': ['E', 'A'],
    'E': ['B']
}

# bfs1(example_graph, 'A')


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

    @staticmethod
    def __heuristic(a: (int, int), b: (int, int)) -> int:
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def __take_turn(self, graph: SquareGrid, units: List[Unit]) -> bool:
        enemies = sorted([u for u in units if u.type != self.type],
                         lambda u: (u.y, u.x))
        if not enemies:
            return False

        shortest_path = None
        closest_enemy = None
        for unit in units:
            start = (self.x, self.y)
            goal = (unit.x, unit.y)
            came_from, _ = Unit.__get_path_to_enemy(graph, start, goal)
            path = Unit.__reconstruct_path(came_from, start, goal)
            if not shortest_path or len(path) < len(shortest_path):
                shortest_path = path
                closest_enemy = unit

        if len(shortest_path) == 0:
            self.attack(closest_enemy)
        else:
            (x, y) = shortest_path[0]
            self.x = x
            self.y = y
        return True

    def attack(self, enemy: Unit):
        enemy.hp -= self.attack_power

    @staticmethod
    def __get_path_to_enemy(graph: SimpleGraph,
                            start: (int, int),
                            goal: (int, int)) -> (dict, dict):
        frontier = PriorityQueue()
        frontier.put(start, 1)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()
            if current == goal:
                break

            for neighbor in graph.neighbors(current):
                new_cost = cost_so_far[current] = graph.cost(current, neighbor)
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + Unit.__heuristic(goal, neighbor)
                    frontier.put(neighbor, priority)
                    came_from[neighbor] = current
        return came_from, cost_so_far

    @staticmethod
    def __reconstruct_path(came_from: dict,
                           start: (int, int),
                           goal: (int, int)) -> List[(int, int)]:
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path


def parsemap(path: str) -> (SquareGrid, List[Unit]):
    units = []
    with open(path, mode='r') as data:
        walls = []
        lines = data.readlines()
        for y, line in enumerate(lines):
            tiles = [t for t in line if t and t != ' ']
            for x, tile in enumerate(tiles):
                if tile == '#':
                    walls.append((x, y))
                elif tile == 'E' or tile == 'G':
                    unit_type = UnitType.ELF if tile == 'E' else UnitType.GOBLIN
                    unit = Unit(x, y, unit_type)
                    units.append(unit)
        width = x + 1
        height = y + 1
        grid = SquareGrid(width, height)
        grid.walls = walls
        return grid, units


def bfs2(graph, start, goal):
    frontier = Queue()
    frontier.put(start)
    came_from = {}
    came_from[start] = None

    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            break

        for neighbor in graph.neighbors(current):
            if neighbor not in came_from:
                frontier.put(neighbor)
                came_from[neighbor] = current
    return came_from


def dijkstra(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 1)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            break

        for neighbor in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, neighbor)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost
                frontier.put(neighbor, priority)
                came_from[neighbor] = current
    return came_from, cost_so_far


def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 1)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            break

        for neighbor in graph.neighbors(current):
            new_cost = cost_so_far[current] = graph.cost(current, neighbor)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(goal, neighbor)
                frontier.put(neighbor, priority)
                came_from[neighbor] = current
    return came_from, cost_so_far


def main():
    grid, _ = parsemap('../inputs/day15_map_test.txt')
    print(grid)
    # came_from, _ = dijkstra(grid, (0, 0), (0, 10))
    came_from, _ = a_star(grid, (0, 0), (0, 10))
    path = reconstruct_path(came_from, (0, 0), (0, 10))
    print(path)


if __name__ == '__main__':
    main()
