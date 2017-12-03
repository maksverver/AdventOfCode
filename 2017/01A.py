import sys

line = sys.stdin.readline().strip()
total = 0
for i in range(len(line)):
  if line[i] == line[i - 1]:
    total += int(line[i])
print(total)
