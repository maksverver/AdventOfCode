# Returns the 4 orthogonal neighbors of (r, c).
def Neighbors4(r, c):
  return [(rr, cc)
      for (rr, cc) in [(r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)]
      if 0 <= rr < H and 0 <= cc < W]


# Returns the 8 neighbors of (r, c) if they are within bounds.
def Neighbors8(r, c):
  return [(rr, cc)
      for (rr, cc) in [
          (r - 1, c - 1), (r - 1, c), (r - 1, c + 1),
          (r,     c - 1),             (r,     c + 1),
          (r + 1, c - 1), (r + 1, c), (r + 1, c + 1)]
      if 0 <= rr < H and 0 <= cc < W]


# Directions in lexicographical order: up, left, right, down
DIRS = [(-1, 0), (0, -1), (0, 1), (1, 0)]

# Directions in clockwise order: up, right, down, left
DIRS = [(-1, 0), (0, 1), (1, 0), (-1, 0)]


if __name__ == '__main__':
  H, W = 3, 4

  assert Neighbors4(1, 2) == [(0, 2), (1, 1), (1, 3), (2, 2)]
  assert Neighbors4(0, 0) == [(0, 1), (1, 0)]
  assert Neighbors4(2, 3) == [(1, 3), (2, 2)]

  assert Neighbors8(1, 2) == [(0, 1), (0, 2), (0, 3), (1, 1), (1, 3), (2, 1), (2, 2), (2, 3)]
  assert Neighbors8(0, 0) == [(0, 1), (1, 0), (1, 1)]
  assert Neighbors8(2, 3) == [(1, 2), (1, 3), (2, 2)]
