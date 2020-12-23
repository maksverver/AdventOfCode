import sys

def Simulate(cups, iterations):
    N = len(cups)

    # Construct an implicit linked list as a list of N integers.
    # next[i] == j if cup j comes after i in the cycle.
    next = [0] * N
    for i, v in enumerate(cups):
        next[v] = cups[(i + 1) % N]

    # Start at cup 0 and simulate iterations one by one.
    p = cups[0]
    for _ in range(iterations):
        a = next[p]
        b = next[a]
        c = next[b]
        q = next[c]
        r = (p - 1) % N
        while r == a or r == b or r == c:
            r = (r - 1) % N
        next[c] = next[r]
        next[r] = a
        next[p] = q
        p = q

    return next

def Answer1(next):
    answer = ''
    cup = next[0]
    while cup != 0:
        answer += str(cup + 1)
        cup = next[cup]
    return(answer)

def Answer2(next):
    a = next[0]
    b = next[a]
    return (a + 1) * (b + 1)

# Input cups are some permutation of integers 1 through N.
# Subtract 1 because the code is simpler if cups are between 0 and N (exclusive).
cups = tuple(int(ch) - 1 for ch in sys.stdin.readline().strip())

assert list(sorted(cups)) == list(range(len(cups)))

print(Answer1(Simulate(cups, 100)))
print(Answer2(Simulate(cups + tuple(range(len(cups), 1_000_000)), 10_000_000)))
