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
    grid = parsemap('../inputs/day15_map_test.txt')
    print(grid)
    # came_from, cost_so_far = dijkstra(grid, (0, 0), (0, 10))
    came_from, cost_so_far = a_star(grid, (0, 0), (0, 10))
    path = reconstruct_path(came_from, (0, 0), (0, 10))
    print(path)


if __name__ == '__main__':
    main()
