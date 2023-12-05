import sys

def ParseSeeds(line):
  '''Seeds is a list of integers.'''
  header, rest = line.split(': ')
  return [int(v) for v in rest.split()]

def ParseMapEntry(line):
  '''A map entry is a triple (begin, end, delta).'''
  dst, src, size = tuple(int(i) for i in line.split())
  assert size > 0
  return (src, src + size, dst - src)

def ParseMapping(part):
  '''A mapping is a list of triples (begin, end, delta).'''
  header, *lines = part.split('\n')
  return list(sorted(ParseMapEntry(line) for line in lines))


def Translate(mapping, ranges):
  '''Uses `mapping` to translate `ranges` (a list of (begin, end) pairs) to new ranges.'''
  results = []
  for a, b in ranges:
    for begin, end, delta in mapping:
      assert a < b

      if a < begin <= b:
        results.append((a, begin))
        a = begin
        if a == b:
          break

      if begin <= a < end:
        if b <= end:
          results.append((a + delta, b + delta))
          a = b
          break
        else:
          results.append((a + delta, end + delta))
          a = end
          assert a < b

    if a < b:
      results.append((a, b))

  return results


def Solve(mappings, ranges):
  for mapping in mappings:
    ranges = Translate(mapping, ranges)
  return min(begin for (begin, end) in ranges)


def Main():
  # Parse input
  seeds_part, *map_parts = sys.stdin.read().strip().split('\n\n')
  seeds = ParseSeeds(seeds_part)
  mappings = tuple(ParseMapping(map_part) for map_part in map_parts)

  # Part 1: each value in seeds is a singleton range
  ranges1 = [(seed, seed + 1) for seed in seeds]
  print(Solve(mappings, ranges1))

  # Part 2: each pair of seeds describes a range of seeds
  ranges2 = [(begin, begin + size) for (begin, size) in zip(seeds[0::2], seeds[1::2])]
  print(Solve(mappings, ranges2))


if __name__ == '__main__':
  Main()
