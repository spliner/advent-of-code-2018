import re
import itertools

from operator import itemgetter

INPUT = '../inputs/day7.txt'
TEST_INPUT = '../inputs/day7_test.txt'

REGEX = r'^Step (?P<requirement>\w+) must be finished before step (?P<step>\w+) can begin.$'


def part1(steps):
    sorted_steps = sorted(steps, key=itemgetter(0))
    grouped = itertools.groupby(sorted_steps, key=itemgetter(0))
    graph = {k: list(map(lambda x: x[1], v)) for k, v in grouped}

    step_id = next(k for k, v in graph.items() if k not in [
                   item for sublist in graph.values() for item in sublist])
    performed_steps = [step_id]
    available_steps = graph[step_id]
    while available_steps:
        step_id = available_steps.pop(0)
        performed_steps.append(step_id)
        if step_id in graph:
            available_steps.extend(
                [i for i in graph[step_id] if i not in available_steps and i not in performed_steps and can_perform(i, performed_steps, graph)])
            available_steps.sort()
    return ''.join(performed_steps)


def can_perform(step, performed_steps, graph):
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
