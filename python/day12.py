import re
import collections

import pprint

INPUT = '../inputs/day12.txt'
TEST_INPUT = '../inputs/day12_test.txt'
GENERATIONS = 20
STATE_REGEX = r'^initial state: (?P<state>(#|\.)+)$'
NOTE_REGEX = r'^(?P<test>(#|\.)+) => (?P<result>(#|\.))$'
INITIAL_OFFSET = 2

Note = collections.namedtuple('Note', 'test result')


def parsefile(path, state_regex, note_regex, initial_offset):
    with open(path, mode='r') as data:
        lines = data.readlines()
        initial_state = parse_initial_state(
            lines[0],
            state_regex,
            initial_offset)
        notes = [parse_note(l.rstrip(), note_regex) for l in lines[2:]]
        return initial_state, notes


def parse_initial_state(line, state_regex, initial_offset):
    match = re.match(state_regex, line).groupdict()
    state = match['state']
    return add_empty_vases(match['state'], initial_offset)


def create_empty_vases(count):
    return ''.join('.' for _ in range(count))


def add_empty_vases(state, offset):
    return create_empty_vases(offset) + state + create_empty_vases(offset)


def parse_note(line, note_regex):
    match = re.match(note_regex, line).groupdict()
    return Note(match['test'], match['result'])


def part1(state, notes, generations, initial_offset, offset):
    for _ in range(generations):
        print(f'{_}: {state}')
        new_state = ''
        for i in range(len(state)):
            test = get_test(state, i)
            note = next((n for n in notes if test == n.test), None)
            if note:
                if note.result == '#':
                    if i < initial_offset:
                        new_state += create_empty_vases(initial_offset - i)
                    # elif i > len(state)
                new_state += note.result
            else:
                new_state += '.'
        state = new_state
    return state


def get_test(state, index):
    if index == 0:
        return create_empty_vases(2) + state[0:3]
    if index == 1:
        return create_empty_vases(1) + state[0:4]
    if index == len(state) - 1:
        return state[-3:] + create_empty_vases(2)
    if index == len(state) - 2:
        return state[-4:] + create_empty_vases(1)
    return state[index - 2:index + 3]


if __name__ == '__main__':
    test_initial_state, test_notes = parsefile(
        TEST_INPUT,
        STATE_REGEX,
        NOTE_REGEX,
        INITIAL_OFFSET)
    test_result1 = part1(test_initial_state,
                         test_notes,
                         GENERATIONS,
                         INITIAL_OFFSET,
                         INITIAL_OFFSET)
    print(test_result1)
