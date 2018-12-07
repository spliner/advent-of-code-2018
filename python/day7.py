import re
import itertools

from operator import itemgetter

INPUT = '../inputs/day7.txt'
TEST_INPUT = '../inputs/day7_test.txt'

REGEX = r'^Step (?P<requirement>\w+) must be finished before step (?P<step>\w+) can begin.$'


def part1(steps):
    print(steps)


def parsefile(path, regex):
    with open(path, mode='r') as data:
        return [parseline(l.rstrip(), regex) for l in data.readlines()]


def parseline(line, regex):
    matches = re.match(regex, line).groupdict()
    return (matches['requirement'], matches['step'])


if __name__ == '__main__':
    test_steps = parsefile(TEST_INPUT, REGEX)
    part1(test_steps)
