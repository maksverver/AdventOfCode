from random import randint, randrange, shuffle

def SplitRange(begin, end, splits):
  ranges = [(begin, end)]
  for _ in range(splits):
    i = randrange(0, len(ranges))
    begin, end = ranges[i]
    assert end - begin >= 2
    mid = randint(begin + 1, end - 1)
    ranges[i] = begin, mid
    ranges.append((mid, end))
  ranges.sort()
  return ranges

seeds_begin = randint(1, 10**8)
seeds_end   = randint(10**9 - 10**8, 10**9)
start_ranges = SplitRange(seeds_begin, seeds_end, 9)
seeds = []
for a, b in start_ranges:
  seeds.append(a)
  seeds.append(b - a)
print('seeds:', *seeds)

parts = ['seed', 'soil', 'fertilizer', 'water', 'light', 'temperature', 'humidity', 'location']
for i in range(len(parts) - 1):
  print()
  print('%s-to-%s map:' % (parts[i], parts[i + 1]))
  ranges = SplitRange(1, 10**9, randint(10, 50))
  sources = list(range(len(ranges)))
  shuffle(sources)
  triples = []
  pos = 1
  for i in sources:
    a, b = ranges[i]
    triples.append((pos, a, b - a))
    pos += b - a
  shuffle(triples)
  for triple in triples:
    print(*triple)

