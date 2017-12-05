import sys

a = [int(line) for line in sys.stdin]
i = 0
steps = 0
while 0 <= i < len(a):
  a[i], i = a[i] + 1, i + a[i]
  steps += 1
print(steps)
