import sys

code = ''
r,c = 1,1
for line in sys.stdin:
  for ch in line:
    if ch == 'U' and r > 0: r -= 1
    if ch == 'D' and r < 2: r += 1
    if ch == 'L' and c > 0: c -= 1
    if ch == 'R' and c < 2: c += 1
  code += str(3*r + c + 1)
print code
