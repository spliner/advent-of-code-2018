import re
import itertools

from operator import itemgetter

INPUT = '../inputs/day7.txt'
TEST_INPUT = '../inputs/day7_test.txt'
WORKER_COUNT = 5
TEST_WORKER_COUNT = 2
TEST_BASE_COMPLETION_TIME = 0
BASE_COMPLETION_TIME = 60

REGEX = r'^Step (?P<requirement>\w+) must be finished before step (?P<step>\w+) can begin.$'


def part1(steps):
    sorted_steps = sorted(steps, key=itemgetter(0))
    grouped = itertools.groupby(sorted_steps, key=itemgetter(0))
    graph = {k: list(map(lambda x: x[1], v)) for k, v in grouped}

    available_steps = sorted([k for k, v in graph.items() if k not in [
                             item for sublist in graph.values() for item in sublist]])
    step_id = None
    performed_steps = []
    while available_steps:
        step_id = available_steps.pop(0)
        performed_steps.append(step_id)
        if step_id in graph:
            next_steps = [s
                          for s in graph[step_id]
                          if can_perform(s, performed_steps, available_steps, graph)]
            available_steps.extend(next_steps)
            available_steps.sort()
    return ''.join(performed_steps)


def part2(steps, worker_count, base_completion_time):
    sorted_steps = sorted(steps, key=itemgetter(0))
    grouped = itertools.groupby(sorted_steps, key=itemgetter(0))
    graph = {k: list(map(lambda x: x[1], v)) for k, v in grouped}

    available_steps = sorted([k for k, v in graph.items() if k not in [
                             item for sublist in graph.values() for item in sublist]])
    performed_steps = []
    working = {}
    seconds_elapsed = 0
    while available_steps or working:
        while len(working) < worker_count and available_steps:
            step = available_steps.pop(0)
            working[step] = 1

        finished_steps = [step
                          for step, elapsed in working.items()
                          if elapsed == get_completion_time(base_completion_time, step)]
        for step in sorted(finished_steps):
            del working[step]
            performed_steps.append(step)
            if step in graph:
                next_steps = [s
                              for s in graph[step]
                              if can_perform(s, performed_steps, available_steps, graph)]
                available_steps.extend(next_steps)
                available_steps.sort()

        for step in working:
            working[step] += 1

        seconds_elapsed += 1
    print(seconds_elapsed)
    return seconds_elapsed


def get_completion_time(base_completion_time, char):
    # A = 1, B = 2...
    return base_completion_time + ord(char) - 64


def can_perform(step, performed_steps, available_steps, graph):
    if step in available_steps:
        return True
    requirements = [k for k, v in graph.items() if step in v]
    return all(r in performed_steps for r in requirements)


def parsefile(path, regex):
    with open(path, mode='r') as data:
        return [parseline(l.rstrip(), regex) for l in data.readlines()]


def parseline(line, regex):
    matches = re.match(regex, line).groupdict()
    return (matches['requirement'], matches['step'])


if __name__ == '__main__':
    test_steps = parsefile(TEST_INPUT, REGEX)
    assert part1(test_steps) == 'CABDFE'

    steps = parsefile(INPUT, REGEX)
    result1 = part1(steps)
    print(result1)

    assert part2(test_steps, TEST_WORKER_COUNT,
                 TEST_BASE_COMPLETION_TIME) == 15
    result2 = part2(steps, WORKER_COUNT, BASE_COMPLETION_TIME)
    print(result2)
