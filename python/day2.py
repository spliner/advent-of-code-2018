INPUT = '../inputs/day2.txt'


def part1(box_ids):
    twos = 0
    threes = 0
    for box_id in box_ids:
        two_count = filter_by_char_count(box_id, 2)
        twos = twos + 1 if two_count else twos
        three_count = filter_by_char_count(box_id, 3)
        threes = threes + 1 if three_count else threes
    return twos * threes


def filter_by_char_count(box_id, count):
    return [c for c in set(box_id) if box_id.count(c) == count]


def part2(box_ids):
    list_index = 1
    for box_id in box_ids:
        for to_compare in box_ids[list_index:]:
            zipped = zip(box_id, to_compare)
            for index, pair in enumerate(zipped):
                if pair[0] != pair[1]:
                    new_box_id = remove_string(box_id, index)
                    new_to_compare = remove_string(to_compare, index)
                    if new_box_id == new_to_compare:
                        return new_box_id
    return None


def remove_string(text, index):
    return text[:index] + text[index + 1:]


def parsefile(path):
    with open(path) as data:
        return [l.replace('\n', "") for l in data.readlines() if l]


if __name__ == '__main__':
    box_ids = parsefile(INPUT)
    part1_test_data = [
        'abcdef',
        'bababc',
        'abbcde',
        'abcccd',
        'aabcdd',
        'abcdee',
        'ababab'
    ]
    assert part1(part1_test_data) == 12
    part1_result = part1(box_ids)
    print(part1_result)

    part2_test_data = [
        'abcde',
        'fghij',
        'klmno',
        'pqrst',
        'fguij',
        'axcye',
        'wvxyz'
    ]
    assert part2(part2_test_data) == 'fgij'
    part2_result = part2(box_ids)
    print(part2_result)
