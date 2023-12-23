import sys

occupied = {}
bricks = [None]
errors = 0
for i, line in enumerate(sys.stdin, 1):
  assert line.endswith('\n')
  line = line[:-1]
  (x1, y1, z1), (x2, y2, z2) = brick = tuple(map(lambda s: tuple(map(int, s.split(','))), line.split('~')))
  bricks.append(brick)

  if (x1 != x2) + (y1 != y2) + (z1 != z2) > 1:
    print(f'Line {i}: invalid shape', brick, file=sys.stderr)
    errors += 1

  # I've decided to allow this, since it's not forbidden by the probem statement (see challenge 1)
  # if x1 > x2 or y1 > y2 or z1 > z2:
  #   print(f'Line {i}: coordinates out of order', brick, file=sys.stderr)
  #   errors += 1

  if x1 < 0 or y1 < 0 or z1 < 1:
    print(f'Line {i}: coordinates too low', brick, file=sys.stderr)
    errors += 1

  for x in range(x1, x2 + 1):
    for y in range(y1, y2 + 1):
      for z in range(z1, z2 + 1):
        if (x, y, z) in occupied:
          j = occupied[x, y, z]
          print('Overlap between lines', j, 'and', i, 'brick', bricks[j], brick, file=sys.stderr)
          errors += 1
        occupied[x, y, z] = i

sys.exit(errors > 0)
