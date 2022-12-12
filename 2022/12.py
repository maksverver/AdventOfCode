import sys

def ParseHeight(ch):
  if ch == 'S': ch = 'a'
  if ch == 'E': ch = 'z'
  if 'a' <= ch <= 'z': return ord(ch) - ord('a')
  raise Exception('Unknown height ' + ch)

grid = sys.stdin.read().splitlines()
H = len(grid)
W = len(grid[0])
heights = [[ParseHeight(ch) for ch in row] for row in grid]
start, = ((r, c) for r, row in enumerate(grid) for c, ch in enumerate(row) if ch == 'S')
finish, = ((r, c) for r, row in enumerate(grid) for c, ch in enumerate(row) if ch == 'E')
lowest = [(r, c) for r, row in enumerate(heights) for c, h in enumerate(row) if h == 0]

def Search(starts):
  seen = set(starts)
  todo = [(start, 0) for start in starts]
  for (r, c), dist in todo:
    for r2, c2 in ((r + 1, c), (r, c + 1), (r - 1, c), (r, c - 1)):
      if 0 <= r2 < H and 0 <= c2 < W and heights[r2][c2] - heights[r][c] <= 1 and (r2, c2) not in seen:
        if grid[r2][c2] == 'E':
          return dist + 1
        seen.add((r2, c2))
        todo.append(((r2, c2), dist + 1))

print(Search([start]))
print(Search(lowest))
