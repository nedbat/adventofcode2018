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

def analyze_records(records, show=False):
    # key: guard id, value: counter of minutes
    guards = collections.defaultdict(collections.Counter)

    current_gid = None      # Who is on guard
    current_day = None      # What day is it?
    fell = None             # When did they fall asleep

    for record in records:
        m = re.search(r"(?P<day>\d\d-\d\d) \d\d:(?P<minute>\d\d)] (?:Guard #(?P<id>\d+)|(?P<fall>falls)|(?P<wake>wakes))", record)
        if not m:
            print(f"Unexpected input: {record!r}")
            continue
        day, minute, gid, falls, wakes = m.groups()
        if gid is not None:
            # New guard
            assert fell is None
            current_gid = int(gid)
            current_day = None
        elif falls is not None:
            assert current_gid is not None
            assert fell is None
            if current_day is None:
                current_day = day
            else:
                assert day == current_day
            fell = int(minute)
        elif wakes is not None:
            assert current_gid is not None
            assert fell is not None
            wake = int(minute)
            for min in range(fell, wake):
                guards[current_gid][min] += 1
            if show:
                xs = ("." * fell) + ("#" * (wake-fell)) + ("." * (60-wake))
                print(f"{current_day}  {current_gid:5d}  {xs}")
            fell = None

    return guards

def most_minutes_asleep(guards):
    """Which guard slept the most, and for how long?"""
    g_min = ((gid, sum(minutes.values())) for gid, minutes in guards.items())
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

def part1(records):
    guards = analyze_records(records, show=True)
    show_guards(guards)
    gid, minutes = most_minutes_asleep(guards)
    sleepiest = sleepiest_minute(guards, gid)
    return gid, sleepiest, gid * sleepiest

def test_part1():
    assert part1(TEST_INPUT) == (10, 24, 240)

def puzzle_input():
    with open("day04_input.txt") as f:
        return sorted(f.readlines())

chars = ".123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def show_guards(guards):
    for gid in sorted(guards):
        pic = ""
        for min in range(60):
            asleep = guards[gid][min]
            pic += chars[asleep]
        total = sum(guards[gid].values())
        print(f"{gid:4d}  {pic}  {total}")

if __name__ == "__main__":
    gid, sleepiest, ans = part1(TEST_INPUT)
    gid, sleepiest, ans = part1(puzzle_input())
    print(f"Part 1: Sleepiest guard is {gid}, sleepiest minute is {sleepiest}: the answer is {ans}")


def most_consistent_sleeper(guards):
    """Find the guard with the single minute with the most occurences.
    Returns: guard_id, minute_most_slept
    """
    # Tally is a sequence of:
    #   (guard id, minute most slept, times slept that minute)
    tally = ((gid, *minutes.most_common(1)[0]) for gid, minutes in guards.items())
    gid, minute_most_slept, times_slept = max(tally, key=lambda gmt: gmt[2])
    return gid, minute_most_slept

def part2(records):
    guards = analyze_records(records)
    gid, minute_most_asleep = most_consistent_sleeper(guards)
    return gid, minute_most_asleep, gid * minute_most_asleep

def test_part2():
    assert part2(TEST_INPUT) == (99, 45, 4455)

if __name__ == "__main__":
    gid, minute_most_asleep, ans = part2(puzzle_input())
    print(f"Part 2: Most consistent guard is {gid}, sleeping at minute {minute_most_asleep}: the answer is {ans}")
