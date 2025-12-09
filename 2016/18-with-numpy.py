import numpy as np
import sys

def Solve(row, height):
  answer = 0
  pad = np.array([True, True])
  for _ in range(height):
    answer += row.sum()
    l = np.concatenate((pad, row))
    r = np.concatenate((row, pad))
    row = (l == r)[1:-1]
  return answer

row = np.array([c == '.' for c in sys.stdin.readline().strip()])
print(Solve(row, 40))
print(Solve(row, 400000))
