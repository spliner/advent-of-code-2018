import re
import datetime
import itertools

INPUT = '../inputs/day4.txt'
TEST_INPUT = '../inputs/day4_test.txt'

SHIFT_REGEX = r'^\[(?P<date>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2})]\s\w+\s#(?P<id>\d+)\sbegins\sshift$'
ACTION_REGEX = r'^\[(?P<date>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2})]\s(?P<action>.+)$'


def part1(lines):
    schedules = get_sleep_schedules(lines)
    most_asleep_guard_id = None
    max_minutes_asleep = 0
    for guard_id, minutes_sleeping in schedules.items():
        total_minutes_asleep = sum(minutes_sleeping.values())
        if total_minutes_asleep > max_minutes_asleep:
            most_asleep_guard_id = guard_id
            max_minutes_asleep = total_minutes_asleep
    guard_schedule = schedules[most_asleep_guard_id]
    most_frequent_minute = max(set(guard_schedule), key=guard_schedule.get)
    return int(most_asleep_guard_id) * int(most_frequent_minute.split(':')[1])


def get_sleep_schedules(lines):
    schedules = {}
    current_id = None
    slept = None
    for line in lines:
        if 'id' in line:
            # Shift start
            current_id = line['id']
            if current_id not in schedules:
                schedules[current_id] = {}
            slept = None
            continue
        action = line['action']
        if 'asleep' in action:
            slept = line['date']
            continue
        # Woke up
        woke_up = line['date']
        time_delta = woke_up - slept
        slept_for = time_delta.seconds // 60
        # Add range of minutes slept
        for minutes in range(0, slept_for):
            date = slept + datetime.timedelta(minutes=minutes)
            minute = f'{str(date.hour).zfill(2)}:{str(date.minute).zfill(2)}'
            if minute not in schedules[current_id]:
                schedules[current_id][minute] = 0
            schedules[current_id][minute] = schedules[current_id][minute] + 1
    return schedules


def part2(lines):
    schedules = get_sleep_schedules(lines)
    # Remove guards that did not sleep at all
    most_asleep_minutes = {k: max(set(v), key=v.get) for k, v in schedules.items() if v}
    most_asleep_guard = None
    most_asleep_minute = None
    most_asleep_count = 0
    # Calculate guard / minute most slept
    for k, v in most_asleep_minutes.items():
        count = schedules[k][v]
        if count > most_asleep_count:
            most_asleep_guard = k
            most_asleep_minute = v
            most_asleep_count = count
    return int(most_asleep_guard) * int(most_asleep_minute.split(':')[1])


def parsefile(path, shift_regex, action_regex):
    with open(path, mode='r') as data:
        lines = data.readlines()
        lines.sort()
        return [parseline(l.rstrip(), shift_regex, action_regex) for l in lines]


def parseline(line, shift_regex, action_regex):
    match = re.match(shift_regex, line)
    if not match:
        match = re.match(action_regex, line)
    data = match.groupdict()
    data['date'] = datetime.datetime.strptime(data['date'], "%Y-%m-%d %H:%M")
    return data


if __name__ == '__main__':
    test_lines = parsefile(TEST_INPUT, SHIFT_REGEX, ACTION_REGEX)
    assert part1(test_lines) == 240

    lines = parsefile(INPUT, SHIFT_REGEX, ACTION_REGEX)
    result1 = part1(lines)
    print(result1)

    assert part2(test_lines) == 4455
    result2 = part2(lines)
    print(result2)
