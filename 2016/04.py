from collections import defaultdict
import re
import sys

def decode(string, shift):
  return ''.join(
      ' ' if ch == '-' else chr(ord('a') + (ord(ch) - ord('a') + shift)%26)
      for ch in string)

answer1 = 0
for line in sys.stdin:
  name, sect, csum = re.match('([a-z-]*)-([0-9]*)\\[([a-z]*)\\]', line).groups()
  sect = int(sect)

  # For part 1: calculate checksum
  counts = defaultdict(lambda: 0)
  for letter in re.findall('[a-z]', name):
    counts[letter] += 1
  if ''.join(sorted(counts.keys(), key=lambda x: (-counts[x], x))[:5]) == csum:
    answer1 += sect

    # For part 2: decode and find North Pole objects storage.
    if decode(name, sect) == 'northpole object storage':
      answer2 = sect

print answer1
print answer2 
