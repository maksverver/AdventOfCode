# Advent of Code 2023 Day 5: If You Give A Seed A Fertilizer
# https://adventofcode.com/2023/day/5

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


def Translate(mapping, old_ranges):
  '''Uses `mapping` to translate `old_ranges` (a list of (begin, end) pairs) to new ranges.
     Both `mapping` and `old_ranges` must be sorted.'''
  new_ranges = []
  i = 0
  for a, b in old_ranges:
    while i < len(mapping):
      c, d, x = mapping[i]
      if b < c:
        break
      if a < c:
        new_ranges.append((a, c))
        a = c
      if a < d:
        if b < d:
          new_ranges.append((a + x, b + x))
          a = b
          break
        new_ranges.append((a + x, d + x))
        a = d
      i += 1
    if a < b:
      new_ranges.append((a, b))
  return new_ranges


def MergeAndSort(old_ranges):
  new_ranges = []
  a = b = 0
  for c, d in sorted(old_ranges):
    if b < c:
      if a < b:
        new_ranges.append((a, b))
      a, b = c, d
    else:
      b = max(b, d)
  if a < b:
    new_ranges.append((a, b))
  return new_ranges


def Solve(mappings, ranges):
  ranges = MergeAndSort(ranges)
  for mapping in mappings:
    ranges = MergeAndSort(Translate(mapping, ranges))
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
