import sys

def FindDistinct(s, k):
  'Returns the first index i in s so that s[i - k:i] are all distinct.'

  char_count = {}

  def Add(ch):
    if ch not in char_count:
      char_count[ch] = 1
    else:
      char_count[ch] += 1

  def Remove(ch):
    char_count[ch] -= 1
    if char_count[ch] == 0:
      del char_count[ch]

  for i, ch in enumerate(s):
    Add(ch)
    if i >= k:
      Remove(s[i - k])
    if len(char_count) == k:
      return i + 1

s = sys.stdin.readline().strip()
print(FindDistinct(s, 4))
print(FindDistinct(s, 14))
