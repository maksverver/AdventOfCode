from collections import defaultdict
import re
import sys

# guard number -> sleep histogram
histograms = defaultdict(lambda: [0]*60)

def ParseInput(lines):
    for line in sorted(lines):
        time_part, event_part = re.match(r'\[([^]]*)] (.*)', line).groups()
        time = tuple(map(int, re.split('[- :]', time_part)))
        m = re.match('Guard #(\d+) begins shift', event_part)
        if m:
            guard = int(m.group(1))
        elif event_part == 'falls asleep':
            sleep_time = time
        elif event_part == 'wakes up':
            assert sleep_time[:-1] == time[:-1]
            histogram = histograms[guard]
            for minute in range(sleep_time[-1], time[-1]):
                histogram[minute] += 1
            sleep_time = None

def MostCommonMinute(guard):
    histogram = histograms[guard]
    max_freq = max(histogram)
    assert histogram.count(max_freq) == 1
    return histogram.index(max_freq)

def TotalMinutes(guard):
    return sum(histograms[guard])

def MaxMinuteFrequency(guard):
    return max(histograms[guard])

ParseInput(sys.stdin)

# Part 1
guard = max(histograms, key=TotalMinutes)
minutes = MostCommonMinute(guard)
print(guard*minutes)

# Part 2
guard = max(histograms, key=MaxMinuteFrequency)
minutes = MostCommonMinute(guard)
print(guard*minutes)
