import sys

print('graph {')
for line in sys.stdin:
  v, ws = line.split(': ')
  for w in ws.split():
    print(v, '--', w)
print('}')
