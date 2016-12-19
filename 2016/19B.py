import sys

def Solve(elves):
  next = range(1, elves) + [0]
  i = elves//2 - 1
  while elves > 1:
    next[i] = next[next[i]]
    if elves&1 == 1:
      i = next[i]
    elves -= 1
  return i
  
print Solve(int(sys.stdin.readline())) + 1
