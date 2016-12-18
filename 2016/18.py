import sys

def Solve(row, width, height):
  answer = 0
  mask = (1 << width) - 1
  for _ in range(height):
    answer += width - bin(row).count('1')
    row = ((row >> 1) ^ (row << 1)) & mask
  return answer

input = sys.stdin.readline().strip()
row = int(input.replace('.', '0').replace('^', '1'), 2)
print Solve(row, len(input), 40)
print Solve(row, len(input), 400000)
