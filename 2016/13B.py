import sys

def Bitcount(i):
  n = 0
  while i:
    i &= i - 1
    n += 1
  return n

def Accessible(x, y):
  return x >= 0 and y >= 0 and Bitcount(x*x + 3*x + 2*x*y + y + y*y + N)%2 == 0

def Search(start, max_steps):
  seen = set()
  todo = []
  def Add(steps, xy):
    if steps <= max_steps and xy not in seen:
      seen.add(xy)
      todo.append((steps, xy))
  Add(0, start)
  for steps, (x, y) in todo:
    for x2, y2 in ((x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)):
      if Accessible(x2, y2):
        Add(steps + 1, (x2, y2))
  return len(seen)

N = int(sys.stdin.readline())
print(Search((1, 1), 50))
