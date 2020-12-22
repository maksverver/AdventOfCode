from itertools import islice
from collections import deque
import sys

# Returns the initial state as a pair of tuples of ints.
# e.g. ((9, 2, 6, 3, 1), (5, 8, 4, 7, 10))
def ParseInput(input):
    def ParseHand(s, i):
        header, *cards = s.split('\n')
        assert header == 'Player %d:' % i
        return tuple(map(int, cards))
    p1, p2 = input.strip().split('\n\n')
    hand1 = ParseHand(p1, 1)
    hand2 = ParseHand(p2, 2)
    return (hand1, hand2)

def Solve1(state):
    h1, h2 = map(deque, state)
    while h1 and h2:
        c1 = h1.popleft()
        c2 = h2.popleft()
        if c1 > c2:
            h1.append(c1)
            h1.append(c2)
        else:
            h2.append(c2)
            h2.append(c1)
    return (h1, h2)

def Memoize(f):
    memo = {}
    def g(a):
        r = memo.get(a)
        if not r:
            memo[a] = r = f(a)
        return r
    return g

@Memoize
def Solve2(state):
    seen = set()
    h1, h2 = map(deque, state)
    while h1 and h2:
        # If state reoccurs, player 1 immediately wins
        state = (tuple(h1), tuple(h2))
        if state in seen:
            return (tuple(h1), [])
        seen.add(state)

        # Play next round
        c1 = h1.popleft()
        c2 = h2.popleft()
        if c1 > len(h1) or c2 > len(h2):
            winner = c2 > c1
        else:
            r1, r2 = Solve2((tuple(islice(h1, c1)), tuple(islice(h2, c2))))
            assert bool(r1) ^ bool(r2)
            winner = bool(r2)

        if winner == 0:
            h1.append(c1)
            h1.append(c2)
        else:
            h2.append(c2)
            h2.append(c1)
    return (tuple(h1), tuple(h2))

def Score(state):
    h1, h2 = state
    return sum(i * v for i, v in enumerate(reversed(h1 or h2), 1))

initial_state = ParseInput(sys.stdin.read())
print(Score(Solve1(initial_state)))
print(Score(Solve2(initial_state)))
