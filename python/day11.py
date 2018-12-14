from typing import List

SERIAL_NUMBER = 3999
DEFAULT_SQUARE_SIDE = 3
GRID_SIZE = 300


def get_power_level(x: int, y: int, serial_number: int):
    if x == 0 or y == 0:
        return 0
    rack_id = x + 10
    power_level = (rack_id * y + serial_number) * rack_id
    return power_level // 100 % 10 - 5


def part1(grid: List[List[int]]):
    return get_max_power_level(grid, DEFAULT_SQUARE_SIDE)


def get_max_power_level(grid: List[List[int]], square_size: int):
    """
    A----------B
    |          |
    |          |
    |          |
    C----------D
    Sum = D - B - C + A
    """
    max_coordinate = len(grid) - (square_size + 2)
    max_power_level = (None, -999999)
    for x in range(1, max_coordinate):
        for y in range(1, max_coordinate):
            x_a = x
            y_a = y
            x_b = x + square_size
            y_b = y
            x_c = x
            y_c = y + square_size
            x_d = x_b
            y_d = y_c
            total = grid[x_d][y_d] - grid[x_b][y_b] - grid[x_c][y_c] + grid[x_a][y_a]
            if total > max_power_level[1]:
                max_power_level = ((x_a + 1, y_a + 1), total)
    return max_power_level


def part2(grid: List[List[int]]):
    result = (None, -999999)
    for side in range(1, GRID_SIZE + 1):
        max_power_level = get_max_power_level(grid, side)
        if max_power_level[1] > result[1]:
            result = ((max_power_level[0][0], max_power_level[0][1], side), max_power_level[1])
    return result


def run():
    assert get_power_level(3, 5, 8) == 4
    assert get_power_level(122, 79, 57) == -5
    assert get_power_level(217, 196, 39) == 0
    assert get_power_level(101, 153, 71) == 4

    grid = [[get_power_level(x, y, SERIAL_NUMBER) for y in range(GRID_SIZE + 1)] for x in range(GRID_SIZE + 1)]
    for x in range(1, GRID_SIZE + 1):
        for y in range(1, GRID_SIZE + 1):
            grid[x][y] = grid[x][y] + grid[x - 1][y] + grid[x][y - 1] - grid[x - 1][y - 1]

    result1 = part1(grid)
    print(result1)

    result2 = part2(grid)
    print(result2)


if __name__ == '__main__':
    # main()
    run()
