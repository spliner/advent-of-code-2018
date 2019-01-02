from typing import List
from day15_model import PriorityQueue, MapGrid, Unit, UnitType
import copy


def parsegrid(path: str) -> MapGrid:
    with open(path, mode='r') as data:
        lines = data.readlines()
        return _parsegrid(lines)


def parsetestgrid(grid: str) -> MapGrid:
    lines = grid.split('\n')
    return _parsegrid(lines)


def _parsegrid(lines: List[str]) -> MapGrid:
    units = []
    walls = []
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
    grid = MapGrid(width, height)
    grid.walls = walls
    grid.units = units
    return grid


def printstate(grid: MapGrid):
    for y in range(grid.height):
        line = ''
        for x in range(grid.width):
            unit = next((u for u in grid.units if u.x == x and u.y == y), None)
            if unit:
                line += 'E' if unit.type == UnitType.ELF else 'G'
            elif (x, y) in grid.walls:
                line += '#'
            else:
                line += '.'
        units_in_line = sorted([u for u in grid.units if u.y == y],
                               key=lambda u: u.x)
        if units_in_line:
            line += '   ' + ', '.join([f'({u.hp})' for u in units_in_line])
        print(line)


def heuristic(position: (int, int), grid: MapGrid) -> int:
    (x, y) = position
    return y * grid.height + x


def take_turn(unit: Unit, grid: MapGrid, sorted_units: List[Unit]):
    # Omae wa mou shindeiru
    if unit.hp <= 0:
        return

    grid.refresh_unit_positions()
    enemies = [u for u in sorted_units if u.type != unit.type and u.hp > 0]
    closest_enemy = get_adjacent_enemy(unit, enemies)
    shortest_path = []
    if not closest_enemy:
        enemy_goals = [(e, grid.neighbors((e.x, e.y))) for e in enemies]
        start = (unit.x, unit.y)
        for enemy, goals in enemy_goals:
            for goal in goals:
                path = get_path(grid, start, goal)
                if not path:
                    continue
                if not shortest_path or len(path) < len(shortest_path):
                    closest_enemy = enemy
                    shortest_path = path

    if not closest_enemy:
        return

    if shortest_path:
        (x, y) = shortest_path[0]
        unit.x = x
        unit.y = y

    enemy_to_attack = get_adjacent_enemy(unit, enemies)
    if enemy_to_attack:
        enemy_to_attack.hp -= unit.attack_power
        if enemy_to_attack.hp <= 0:
            grid.units.remove(enemy_to_attack)


def get_adjacent_enemy(unit: Unit, enemies: List[Unit]):
    adjacent_enemies = sorted(
        [e for e in enemies if man_distance(unit, e) == 1 and e.hp > 0],
        key=lambda e: (e.hp, e.y, e.x))
    if not adjacent_enemies:
        return None
    return adjacent_enemies[0]


def get_path(grid: MapGrid, start: (int, int), goal: (int, int)):
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

        for neighbor in grid.neighbors(current):
            new_cost = cost_so_far[current] + grid.cost(current, neighbor)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, grid)
                frontier.put(neighbor, priority)
                came_from[neighbor] = current

    # Reconstruct path
    current = goal
    path = []
    while current != start:
        path.append(current)
        if current not in came_from:
            return None
        current = came_from[current]
    path.reverse()
    return path


def man_distance(unit1: Unit, unit2: Unit):
    return abs(unit1.x - unit2.x) + abs(unit1.y - unit2.y)


def part1(grid: MapGrid):
    print('Initial state')
    printstate(grid)
    has_both_types = True
    turn = 0
    while has_both_types:
        sorted_units = sorted(grid.units, key=lambda u: (u.y, u.x))
        for index, unit in enumerate(sorted_units):
            take_turn(unit, grid, sorted_units)
            elves = grid.units_of_type(UnitType.ELF)
            goblins = grid.units_of_type(UnitType.GOBLIN)
            has_both_types = elves and goblins
            if not has_both_types:
                break
        if has_both_types or index == len(sorted_units) - 1:
            turn += 1
            print(f'Turn: {turn}')
            printstate(grid)

    print('Final state')
    printstate(grid)
    hp_sum = sum([u.hp for u in grid.units])
    print(hp_sum)
    result = hp_sum * turn
    print(result)
    return result


def part2(grid: MapGrid):
    print('Initial state')
    originalgrid = copy.deepcopy(grid)
    printstate(grid)
    turn = 0
    attack_power = 4
    set_elf_attack_power(grid, attack_power)
    goblins = grid.units_of_type(UnitType.GOBLIN)
    while goblins:
        original_elves = grid.units_of_type(UnitType.ELF)
        sorted_units = sorted(grid.units, key=lambda u: (u.y, u.x))
        for index, unit in enumerate(sorted_units):
            take_turn(unit, grid, sorted_units)
            elves = grid.units_of_type(UnitType.ELF)
            if len(original_elves) != len(elves):
                grid = copy.deepcopy(originalgrid)
                goblins = grid.units_of_type(UnitType.GOBLIN)
                attack_power += 1
                set_elf_attack_power(grid, attack_power)
                goblins = grid.units_of_type(UnitType.GOBLIN)
                turn = -1
                break
            else:
                goblins = grid.units_of_type(UnitType.GOBLIN)
            if not goblins:
                break
        if goblins or index == len(sorted_units) - 1:
            turn += 1
            print(f'Turn: {turn}')
            printstate(grid)

    print(attack_power)
    print('Final state')
    printstate(grid)
    hp_sum = sum([u.hp for u in grid.units])
    print(hp_sum)
    result = hp_sum * turn
    print(result)
    return result


def set_elf_attack_power(grid: MapGrid, attack_power: int) -> int:
    elves = grid.units_of_type(UnitType.ELF)
    for elf in elves:
        elf.attack_power = attack_power


def main():
    gridstr = '''#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######'''
    grid = parsetestgrid(gridstr)
    assert(part1(grid)) == 27730
    grid = parsetestgrid(gridstr)
    assert(part2(grid)) == 4988
    gridstr = '''#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######'''
    grid = parsetestgrid(gridstr)
    assert(part1(grid)) == 36334
    gridstr = '''#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######'''
    grid = parsetestgrid(gridstr)
    assert(part1(grid)) == 39514
    grid = parsetestgrid(gridstr)
    assert(part2(grid)) == 31284
    gridstr = '''#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######'''
    grid = parsetestgrid(gridstr)
    assert(part1(grid)) == 27755
    gridstr = '''#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######'''
    grid = parsetestgrid(gridstr)
    assert(part1(grid)) == 28944
    gridstr = '''#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########'''
    grid = parsetestgrid(gridstr)
    assert(part1(grid)) == 18740
    grid = parsetestgrid(gridstr)
    assert(part2(grid)) == 1140

    grid = parsegrid('../inputs/day15.txt')
    print(part1(grid))
    grid = parsegrid('../inputs/day15.txt')
    part2(grid)


if __name__ == '__main__':
    main()
