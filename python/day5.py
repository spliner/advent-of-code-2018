INPUT = '../inputs/day5.txt'
TEST_INPUT = '../inputs/day5_test.txt'


def part1(polymer):
    stack = []
    for unit in polymer:
        if not stack:
            stack.append(unit)
            continue
        last_unit = stack.pop()
        uppercase_unit = unit.upper()
        uppercase_last_unit = last_unit.upper()
        is_unit_uppercase = unit == uppercase_unit
        is_last_unit_uppercase = last_unit == uppercase_last_unit
        if uppercase_unit != uppercase_last_unit or is_unit_uppercase == is_last_unit_uppercase:
            # Add both units to the stack if they don't react
            stack.append(last_unit)
            stack.append(unit)
    return len(stack)


def readfile(path):
    with open(path, mode='r') as data:
        return data.read().rstrip()


if __name__ == '__main__':
    test_polymer = readfile(TEST_INPUT)
    assert part1(test_polymer) == 10

    polymer = readfile(INPUT)
    result1 = part1(polymer)
    print(result1)
