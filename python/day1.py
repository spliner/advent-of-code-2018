def part1(frequencies):
    return sum(frequencies)


def part2(frequencies):
    freq_set = set()
    i = 0
    freq_set.add(0)
    current = frequencies[i]
    while current not in freq_set:
        freq_set.add(current)
        i = (i + 1) % len(frequencies)
        current += frequencies[i]
    return current


def parsefile(path):
    with open(path, mode='r') as data:
        return [int(x) for x in data.readlines() if x]


if __name__ == '__main__':
    assert part1([1, 1, 1]) == 3
    assert part1([1, 1, -2]) == 0
    assert part1([-1, -2, -3]) == -6

    frequencies = parsefile('../inputs/day1.txt')
    result1 = part1(frequencies)
    print(f'Part 1: {result1}')

    assert part2([1, -1]) == 0
    assert part2([3, 3, 4, -2, -4]) == 10
    assert part2([-6, 3, 8, 5, -6]) == 5
    assert part2([7, 7, -2, -7, -4]) == 14

    result2 = part2(frequencies)
    print(f'Part 2: {result2}')
