import sys

codes = sys.stdin.readline().strip().split(',')

def Hash(s):
  h = 0
  for ch in s:
    h += ord(ch)
    h *= 17
    h %= 256
  return h

def Part1():
  return sum(map(Hash, codes))

def Part2():
  # Execute all instructions. We can use the fact that Python dictionaries
  # maintain insertion order of keys, exactly as required by the problem
  # statement.
  hashmap = [dict() for _ in range(256)]
  for code in codes:
    if code.endswith('-'):
      # Remove
      key = code[:-1]
      hashmap[Hash(key)].pop(key, None)
    else:
      # Add/replace
      key, val = code.split('=')
      hashmap[Hash(key)][key] = int(val)

  # Calculate the answer
  return sum((1 + i) * (j + 1) * v for i, m in enumerate(hashmap) for j, v in enumerate(m.values()))

print(Part1())
print(Part2())
