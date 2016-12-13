import sys

def Bitcount(i):
  n = 0
  while i:
    i &= i - 1
    n += 1
  return n

def Blocked(x, y):
  return Bitcount(x*x + 3*x + 2*x*y + y + y*y + N)%2

def Search(start, finish):
  seen = set()
  todo = []
  def Add(steps, xy):
    if xy not in seen:
      seen.add(xy)
      todo.append((steps, xy))
  Add(0, start)
  for steps, (x, y) in todo:
    for x2, y2 in ((x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)):
      if x2 >= 0 and y2 >= 0 and not Blocked(x2, y2):
        if (x2, y2) == finish:
          return steps + 1
        Add(steps + 1, (x2, y2))

N = int(sys.stdin.readline())
print Search((1, 1), (31, 39))
