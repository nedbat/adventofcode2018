# https://adventofcode.com/2018/day/4

import collections
import re

TEST_INPUT = """\
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
""".splitlines()

def analyze_records(records):
    # key: guard id, value: counter of minutes
    guards = collections.defaultdict(collections.Counter)

    current_gid = None      # Who is on guard
    fell = None             # When did they fall asleep

    for record in records:
        m = re.search(r"(?P<minute>\d\d)] (?:Guard #(?P<id>\d+)|(?P<fall>falls)|(?P<wake>wakes))", record)
        if not m:
            print(f"Unexpected input: {record!r}")
            continue
        minute, gid, falls, wakes = m.groups()
        if gid is not None:
            # New guard
            assert fell is None
            current_gid = int(gid)
        elif falls is not None:
            assert current_gid is not None
            assert fell is None
            fell = int(minute)
        elif wakes is not None:
            assert current_gid is not None
            assert fell is not None
            for min in range(fell, int(minute)+1):
                guards[current_gid][min] += 1
            fell = None

    return guards

def most_minutes_asleep(guards):
    """Which guard slept the most, and for how long?"""
    g_min = ((gid, sum(minutes)) for gid, minutes in guards.items())
    return max(g_min, key=lambda gm: gm[1])

def test_minutes_asleep():
    gid, minutes = most_minutes_asleep(analyze_records(TEST_INPUT))
    assert gid, minutes == (10, 50)

def sleepiest_minute(guards, gid):
    """What minute was this guard asleep the most?"""
    return guards[gid].most_common(1)[0][0]

def test_sleepiest_minute():
    guards = analyze_records(TEST_INPUT)
    gid, minutes = most_minutes_asleep(guards)
    assert sleepiest_minute(guards, gid) == 24

def puzzle_input():
    with open("day04_input.txt") as f:
        return sorted(f.readlines())

if __name__ == "__main__":
    guards = analyze_records(puzzle_input())
    gid, minutes = most_minutes_asleep(guards)
    sleepiest = sleepiest_minute(guards, gid)
    print(f"Part 1: the answer is {gid * sleepiest}")
