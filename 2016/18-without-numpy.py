import sys

def Next(row):
  def Get(i):
    return row[i] if 0 <= i < len(row) else '.'
  return ''.join(
      '.^'[Get(i - 1) + Get(i) + Get(i + 1) in ("^^.", '.^^', '^..', '..^')]
      for i in range(len(row)))

def Solve(row, height):
  answer = 0
  for _ in range(height):
    answer += row.count('.')
    row = Next(row)
  return answer

row = sys.stdin.readline().strip()
print Solve(row, 40)
print Solve(row, 400000)
