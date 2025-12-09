import sys

total = int(sys.stdin.readline())
answer = 0
i = 1
while answer + (1 << i) < total:
  answer += ((total >> (i - 1)) & 1) << i
  i += 1
print(answer + 1)
