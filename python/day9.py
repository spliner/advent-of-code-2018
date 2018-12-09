import re
import operator

INPUT = '../inputs/day9.txt'
REGEX = r'^(?P<player_count>\d+) players; last marble is worth (?P<last_marble_value>\d+) points$'
TEST_DATA = '10 players; last marble is worth 1618 points'


class Marble:
    def __init__(self, value):
        self.value = value
        self.next = self
        self.previous = self

    def __str__(self):
        return f'{self.previous.value} <- {self.value} -> {self.next.value}'

    def __repr__(self):
        return self.__str__()


def get_high_score(config):
    player_count = config['player_count']
    last_marble_value = config['last_marble_value']
    scores = {}
    for i in range(player_count):
        scores[i] = 0

    current_marble = Marble(0)
    for i in range(1, last_marble_value + 1):
        if i % 23 == 0:
            current_player = i % player_count
            for _ in range(7):
                current_marble = current_marble.previous
            scores[current_player] += (i + current_marble.value)
            next_marble = current_marble.next
            previous_marble = current_marble.previous
            previous_marble.next = next_marble
            next_marble.previous = previous_marble
            current_marble = next_marble
        else:
            marble = Marble(i)
            to_insert = current_marble.next
            to_insert.next.previous = marble
            marble.next = to_insert.next
            marble.previous = to_insert
            to_insert.next = marble
            if to_insert.previous == to_insert:
                to_insert.previous = marble
            current_marble = marble
    sorted_high_scores = sorted(
        scores.items(),
        key=operator.itemgetter(1),
        reverse=True)
    return sorted_high_scores[0][1]


def parsefile(path, regex):
    with open(path, mode='r') as data:
        return parsedata(data.read().rstrip(), regex)


def parsedata(data, regex):
    match = re.match(regex, data)
    return {k: int(v) for k, v in match.groupdict().items()}


if __name__ == '__main__':
    test_config = parsedata(TEST_DATA, REGEX)
    assert get_high_score(test_config) == 8317

    config = parsefile(INPUT, REGEX)
    result1 = get_high_score(config)
    print(result1)

    config['last_marble_value'] *= 100
    result2 = get_high_score(config)
    print(result2)
