import sys

grid = [s.strip() for s in sys.stdin]
H = len(grid)
W = len(grid[0])

dirs = [
  ( 0,  1),  # 0 = right
  ( 1,  0),  # 1 = down
  ( 0, -1),  # 2 = left
  (-1,  0),  # 3 = up
]

# Given a character on the grid `ch`, and a current direction `dir`,
# convert[ch][dir] contains a list of directions the light wil follow next:
convert = { #right   down    left    up
  '.':      [[0],    [1],    [2],    [3]   ],
  '|':      [[1, 3], [1],    [1, 3], [3]   ],
  '-':      [[0],    [0, 2], [2],    [0, 2]],
  '\\':     [[1],    [0],    [3],    [2]   ],
  '/':      [[3],    [2],    [1],    [0]   ],
}

# Uses depth-first search to calculate the number of positions visited
# (regardless of light direction). There are 4×H×W possible states.
def Search(r, c, dir):
  todo = [(r, c, dir)]
  seen = set(todo)
  while todo:
    r, c, dir = todo.pop()
    for dir2 in convert[grid[r][c]][dir]:
      dr, dc = dirs[dir2]
      r2 = r + dr
      c2 = c + dc
      if 0 <= r2 < H and 0 <= c2 < W and (state := (r2, c2, dir2)) not in seen:
        seen.add(state)
        todo.append(state)
  return len(set((r, c) for (r, c, dir) in seen))

def Part1():
  return Search(0, 0, 0)

def Part2():
  answer = 0
  for r in range(H): answer = max(answer, Search(r,     0,     0))
  for c in range(W): answer = max(answer, Search(0,     c,     1))
  for r in range(H): answer = max(answer, Search(r,     W - 1, 2))
  for c in range(W): answer = max(answer, Search(H - 1, c,     3))
  return answer

print(Part1())
print(Part2())
