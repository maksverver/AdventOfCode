import sys

pad = ['~~~~~~~',
       '~~~1~~~',
       '~~234~~',
       '~56789~',
       '~~ABC~~',
       '~~~D~~~',
       '~~~~~~~']
code = ''
r,c = 3,1
for line in sys.stdin:
  for ch in line:
    if ch == 'U' and pad[r - 1][c] != '~': r -= 1
    if ch == 'D' and pad[r + 1][c] != '~': r += 1
    if ch == 'L' and pad[r][c - 1] != '~': c -= 1
    if ch == 'R' and pad[r][c + 1] != '~': c += 1
  code += pad[r][c]
print(code)
