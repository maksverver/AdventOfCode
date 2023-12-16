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

def NextStates(state):
  r, c, dir = state
  states = []
  for dir2 in convert[grid[r][c]][dir]:
    dr, dc = dirs[dir2]
    r2 = r + dr
    c2 = c + dc
    if 0 <= r2 < H and 0 <= c2 < W:
      states.append((r2, c2, dir2))
  return states

# Uses depth-first search to calculate the number of positions visited
# (regardless of light direction). There are 4×H×W possible states.
def FindReachable(start_state):
  todo = [start_state]
  seen = {start_state}
  while todo:
    for state in NextStates(todo.pop()):
      if state not in seen:
        seen.add(state)
        todo.append(state)
  return seen

def Solve(start_state):
  return len(set((r, c) for (r, c, dir) in FindReachable(start_state)))

def Part1():
  return Solve((0, 0, 0))

def Part2():
  return max(Solve(state) for state in
    [(r,     0,     0) for r in range(H)] +
    [(0,     c,     1) for c in range(W)] +
    [(r,     W - 1, 2) for r in range(H)] +
    [(H - 1, c,     3) for c in range(W)])

print(Part1())
print(Part2())
