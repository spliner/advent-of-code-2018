import collections
import heapq


class SimpleGraph(object):
    def __init__(self):
        self.edges = {}

    def neighbors(self, id):
        return self.edges[id]


class SquareGrid(object):
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.walls = []

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls

    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0:
            results.reverse()
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def cost(self, from_node, to_node):
        return 1

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


class Queue(object):
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()

class PriorityQueue(object):
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]