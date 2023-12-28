# Advent of Code 2023 Day 9: Mirage Maintenance
# https://adventofcode.com/2023/day/9

import sys

def Extrapolate(row):
  if row.count(0) == len(row):
    return 0
  next_row = [row[i + 1] - row[i] for i in range(len(row) - 1)]
  return row[-1] + Extrapolate(next_row)

def Solve(rows):
  return sum(map(Extrapolate, rows))

rows = [[int(i) for i in line.split()] for line in sys.stdin]

print(Solve(rows))  # Part 1

for row in rows: row.reverse()

print(Solve(rows))  # Part 2

