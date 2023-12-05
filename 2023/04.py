import sys

def ParseCard(line):
  card, numbers = line.split(': ')
  win, have = (list(int(x) for x in s.split()) for s in numbers.split(' | '))
  return (win, have)

cards = [ParseCard(line) for line in sys.stdin]
answer1 = 0
copies = [1]*len(cards)
for i, (win, have) in enumerate(cards):
  if n := len(set(win).intersection(set(have))):
    answer1 += 2**(n - 1)
    for j in range(i + 1, i + 1 + n):
      copies[j] += copies[i]
answer2 = sum(copies)

print(answer1)
print(answer2)
