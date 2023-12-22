from collections import deque
import sys

# Parses a brick into a tuple ((x1, y1, x1), (x2, y2, x2)) and normalizes the
# coordinates so that x1 ≤ x2, y1 ≤ y2, z1 ≤ z2.
def ParseBrick(line):
  (x1, y1, z1), (x2, y2, z2) = map(lambda s: map(int, s.split(',')), line.split('~'))
  assert (x1 != x2) + (y1 != y2) + (z1 != z2) <= 1
  if x1 > x2: x2, x1 = x1, x2
  if y1 > y2: y2, y1 = y1, y2
  if z1 > z2: z2, z1 = z1, z2
  return ((x1, y1, z1), (x2, y2, z2))


bricks = [ParseBrick(line.strip()) for line in sys.stdin]
bricks.sort(key=lambda brick: brick[0][2])

# Calculate where all bricks will drop
#
supported_by = [[] for _ in range(len(bricks))]
supporting   = [[] for _ in range(len(bricks))]
occupied = {}  # (x, y, z) -> brick index
for i, ((x1, y1, z1), (x2, y2, z2)) in enumerate(bricks):
  bricks_below = set()
  while z1 > 1 and not (bricks_below := set(
      occupied[x, y, z1 - 1]
      for x in range(x1, x2 + 1)
      for y in range(y1, y2 + 1)
      if (x, y, z1 - 1) in occupied)):
    z1 -= 1
    z2 -= 1

  for x in range(x1, x2 + 1):
    for y in range(y1, y2 + 1):
        for z in range(z1, z2 + 1):
          occupied[x,y,z] = i

  supported_by[i] = bricks_below
  for j in bricks_below:
    supporting[j].append(i)


# Runs a breadth-first search to calculate all bricks that will fall if the
# i-th brick is initially removed.
#
def CountFalling(i):
  fallen = set()
  todo = deque([i])
  while todo:
    i = todo.popleft()
    fallen.add(i)
    for j in supporting[i]:
      if all(k in fallen for k in supported_by[j]):
        todo.append(j)
  return len(fallen) - 1


# Calculate answers
#
answer1 = answer2 = 0
for i in range(len(bricks)):
  n = CountFalling(i)
  answer1 += n == 0
  answer2 += n
print(answer1)
print(answer2)
