from random import randint, randrange, shuffle
import sys

parts = ['seed', 'soil', 'fertilizer', 'water', 'light', 'temperature', 'humidity', 'location']

def Generate(max_seed, base, answer):
  assert base**8 <= max_seed
  seeds = [0, max_seed]
  print('seeds:', *seeds)

  offset = [randint(0, 10**6) for _ in parts]
  offset[0] = 0
  offset[-1] = answer

  for i in range(len(parts) - 1):
    print()
    print('%s-to-%s map:' % (parts[i], parts[i + 1]))
    triples = [(offset[i + 1], offset[i] + base**(7 - i)*j, base**(7 - i)) for j in range(base)]
    for triple in triples:
      print(*triple)

  print('answer:', offset[-1], file=sys.stderr)


#Generate(2**31 - 1, 14, 123456789)
Generate(2**63 - 1, 234, 1234567890987654321)
