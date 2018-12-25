from day15_collections import SimpleGraph, Queue, SquareGrid


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

bfs1(example_graph, 'A')


def parsemap(path) -> SquareGrid:
    with open(path, mode='r') as data:
        walls = []
        lines = data.readlines()
        for y, line in enumerate(lines):
            tiles = [t for t in line if t and t != ' ']
            for x, tile in enumerate(tiles):
                if tile == '#':
                    walls.append((x, y))
        width = x + 1
        height = y + 1
        grid = SquareGrid(width, height)
        grid.walls = walls
        return grid
