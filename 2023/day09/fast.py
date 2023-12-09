# Linear time solution for Advent of Code 2023 Day 9: Mirage Maintenance.

import sys

# Evaluate a row of Pascal's triangle: nCr(n, 1), nCr(n, 2), .., nCr(n)
def BinomialCoefficients(n):
  res = [1] + [0]*n
  for i in range(1, n + 1):
    res[i] = res[i - 1] * (n + 1 - i) // i
  return res

def Extrapolate(row):
  n = len(row)
  sign = (-1)**(n + 1)
  answer = 0
  for x, y in zip(row, BinomialCoefficients(n)):
    answer += sign * x * y
    sign = -sign
  return answer

def Solve(rows):
  return sum(map(Extrapolate, rows))

# Read input
rows = [list(map(int, line.split())) for line in sys.stdin]

# Part 1
print(Solve(rows))

# Part 2 is the same as part 1, but with each row reversed:
for row in rows: row.reverse()
print(Solve(rows))
