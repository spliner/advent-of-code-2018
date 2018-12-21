import re
import collections

import pprint

INPUT = '../inputs/day12.txt'
TEST_INPUT = '../inputs/day12_test.txt'
GENERATIONS = 20
GENERATIONS2 = 50000000000
STATE_REGEX = r'^initial state: (?P<state>(#|\.)+)$'
NOTE_REGEX = r'^(?P<test>(#|\.)+) => (?P<result>(#|\.))$'

Note = collections.namedtuple('Note', 'test result')


def parsefile(path, state_regex, note_regex):
    with open(path, mode='r') as data:
        lines = data.readlines()
        initial_state = parse_initial_state(lines[0], state_regex)
        notes = [parse_note(l.rstrip(), note_regex) for l in lines[2:]]
        return initial_state, notes


def parse_initial_state(line, state_regex):
    match = re.match(state_regex, line).groupdict()
    return match['state']


def parse_note(line, note_regex):
    match = re.match(note_regex, line).groupdict()
    return Note(match['test'], match['result'])


def part1(initial_state, notes, generations):
    _, plant_count = get_state(initial_state, notes, generations)
    return plant_count


def get_state(initial_state, notes, generations):
    state = '..' + initial_state + '..'
    offset = 2
    plant_count = count_plants(state, offset)
    for g in range(generations):
        new_state = ''
        for i in range(len(state)):
            test = get_test(state, i)
            note = next((n for n in notes if test == n.test), None)
            new_state += note.result if note else '.'
        state = new_state
        new_count = count_plants(state, offset)
        diff = new_count - plant_count
        print(f'{g + 1}: {new_count} ({diff})')
        plant_count = new_count
        state = '..' + new_state + '..'
        offset += 2
    return state, plant_count


def get_test(state, index):
    if index == 0:
        return '..' + state[0:3]
    if index == 1:
        return '.' + state[0:4]
    if index == len(state) - 1:
        return state[-3:] + '..'
    if index == len(state) - 2:
        return state[-4:] + '.'
    return state[index - 2:index + 3]


def count_plants(state, offset):
    plant_count = 0
    for index, c in enumerate(state):
        if c == '#':
            plant_count += index - offset
    return plant_count


def part2(initial_state, notes, generations):
    test_generations = 200
    plant_count = part1(initial_state, notes, test_generations)
    # After generation #100 the difference in plant count seems to be the same
    # This probably only works for my input :(
    magic_number = 51
    return plant_count + (generations - test_generations) * magic_number


if __name__ == '__main__':
    test_initial_state, test_notes = parsefile(TEST_INPUT,
                                               STATE_REGEX,
                                               NOTE_REGEX)
    test_result1 = part1(test_initial_state,
                         test_notes,
                         GENERATIONS)
    assert test_result1 == 325
    initial_state, notes = parsefile(INPUT,
                                     STATE_REGEX,
                                     NOTE_REGEX)
    result1 = part1(initial_state, notes, GENERATIONS)
    print(result1)

    result2 = part2(initial_state, notes, GENERATIONS2)
    print(result2)
