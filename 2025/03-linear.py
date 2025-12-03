import sys
from collections import deque

# Really cool greedy solution. Runs in O(n) regardless of number base (10)
# or number of digits in the subsequence (k=12).
def Solve(digits, k):

    # Start with the final `k` digits. We split those into two parts: a maximal
    # nonincreasing suffix (e.g. "11257", at least 1 digit) and the rest.
    i = len(digits) - k + 1
    assert i > 0
    while i < len(digits) and digits[i] <= digits[i - 1]:
        i += 1
    nonincreasing = deque(digits[len(digits) - k:i])
    tail = deque(digits[i:])

    # Now process the remaining digits from back to front.
    #
    # Invariant: nondecreasing + tail is the maximal length k subsequence.
    for ch in reversed(digits[:-k]):
        # If we use the current character, it must come first, which means its
        # only useful when it's at least as large as the current leading digit.
        if ch >= nonincreasing[0]:
            # For the remaining digits, we want to keep the maximal (k - 1)
            # digit subsequence of the existing subsequence, which means
            # dropping the first digit that has a greater successor, which is
            # the last digit of the nonincreasing prefix.
            nonincreasing.pop()
            nonincreasing.appendleft(ch)
            # Finally, move characters from the tail to the nonincreasing prefix
            # if we can. Note that we execute the loop body at most k-1 times
            # across the entire algorithm, which is why the final algorithm has
            # O(n + k) = O(n) time.
            while tail and tail[0] <= nonincreasing[-1]:
                nonincreasing.append(tail.popleft())

    return int(''.join(map(str, nonincreasing + tail)))

answer1 = 0
answer2 = 0
for line in sys.stdin:
    digits = tuple(map(int, line.strip()))
    answer1 += Solve(digits,  2)
    answer2 += Solve(digits, 12)
print(answer1)
print(answer2)
