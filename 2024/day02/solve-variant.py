import sys

def LongestIncreasingSubsequence(row, max_diff):
    # max_len[x] is the length of the longest valid sequence that ends with x
    max_len = {}
    for v in row:
        max_len[v] = max(max_len.get(v - d, 0) + 1 for d in range(1, max_diff + 1))
    return max(max_len.values())

def MinErrors(row):
    max_valid = max(
        LongestIncreasingSubsequence(row, 3),
        LongestIncreasingSubsequence(reversed(row), 3))
    return len(row) - max_valid

rows = [list(map(int, line.split())) for line in sys.stdin]
errors = [MinErrors(row) for row in rows]

# print(sum(e < 1 for e in errors))  # Part 1
# print(sum(e < 2 for e in errors))  # Part 2

print(sum(errors))
