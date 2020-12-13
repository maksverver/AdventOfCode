import sys

# Note: periods in the schedule are prime numbers.
start_time = int(sys.stdin.readline())
schedule = [(i, int(word)) for (i, word) in enumerate(sys.stdin.readline().strip().split(',')) if word != 'x']

def Part1():
    min_time = best_period = None
    for _, period in schedule:
        if period is None:
            continue
        t = (start_time + period - 1) // period * period
        if min_time is None or t < min_time:
            min_time = t
            best_period = period
    return (min_time - start_time) * best_period

def Part2():
    t = 0
    m = 1
    for (i, p) in schedule:
        while (t + i) % p:
            t += m
        m *= p
    return t

print(Part1())
print(Part2())
