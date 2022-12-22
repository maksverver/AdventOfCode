# Advent of Code 2022 Day 22: Monkey Map
# https://adventofcode.com/2022/day/22

from math import sqrt
import re
import sys

# Directions (right, down, left, up)
DR = [0, 1,  0, -1]
DC = [1, 0, -1,  0]
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3
Opposite = lambda dir: dir ^ 2


class Node:
  'A graph node, that connects to adjacent nodes in four orthogonal directions.'

  def __init__(self, debug_coords):
    self.adj = [None]*4
    self.wall = None
    self.coords = None
    self.debug_coords = debug_coords

  def Step(self, dir):
    'Take a step in the given direction. Returns a pair (new node, new dir).'
    return self.adj[dir]

  def __repr__(self):
    return 'Node(%s)' % repr(self.debug_coords)


def Connect(f, d, g, e):
  '''Connect edge d of node f to edge e of node g.'''
  assert f.adj[d] is None
  assert g.adj[e] is None
  f.adj[d] = (g, Opposite(e))
  g.adj[e] = (f, Opposite(d))


# Build a graph where the nodes correspond with facelets of a cube of the given
# size. This is used to solve part 2.
def BuildCube(size):
  # Create 6 faces of size × size nodes each, and connect the nodes within each face.
  faces = [[[Node((f, r, c)) for c in range(size)] for r in range(size)] for f in range(6)]
  for f in range(6):
    for i in range(size):
      for j in range(size):
        if j + 1 < size:
          Connect(faces[f][i][j], RIGHT, faces[f][i][j + 1], LEFT)
        if i + 1 < size:
          Connect(faces[f][i][j], DOWN, faces[f][i + 1][j], UP)

  # Now connect the faces to each other. We use a cube built from the following
  # template (though it doesn't really matter what layout we use, as long as we
  # connect the nodes correctly).
  #
  #         a
  #       +---+
  #    b  | 2 | c
  #   +---+---+---+
  # d | 3 | 0 | 1 | e
  #   +---+---+---+
  #     f | 4 | g
  #       +---+
  #     d | 5 | e
  #       +---+
  #         a
  z = size - 1
  for i in range(size):
    j = z - i
    Connect(faces[0][i][z], RIGHT, faces[1][i][0], LEFT)   # 0 - 1
    Connect(faces[0][0][i], UP,    faces[2][z][i], DOWN)   # 0 - 2
    Connect(faces[0][i][0], LEFT,  faces[3][i][z], RIGHT)  # 0 - 3
    Connect(faces[0][z][i], DOWN,  faces[4][0][i], UP)     # 0 - 4
    Connect(faces[2][0][i], UP,    faces[5][z][i], DOWN)   # 2 - 5 (a)
    Connect(faces[1][0][i], UP,    faces[2][j][z], RIGHT)  # 1 - 2 (c)
    Connect(faces[1][z][i], DOWN,  faces[4][i][z], RIGHT)  # 1 - 4 (g)
    Connect(faces[1][i][z], RIGHT, faces[5][j][z], RIGHT)  # 1 - 5 (e)
    Connect(faces[3][0][i], UP,    faces[2][i][0], LEFT)   # 3 - 2 (b)
    Connect(faces[3][z][i], DOWN,  faces[4][j][0], LEFT)   # 3 - 4 (f)
    Connect(faces[3][i][0], LEFT,  faces[5][j][0], LEFT)   # 3 - 5 (d)
    Connect(faces[4][z][i], DOWN,  faces[5][0][i], UP)     # 4 - 5

  # Start at the leftmost node of the topmost row of face 0.
  return faces[0][0][0]


# Build a graph of the given grid that wraps around, skipping over spaces.
# This is used to solve part 1 of the problem.
def BuildWrappingGraph(grid):
  def MakeNode(r, c, ch):
    if ch.isspace():
      return None
    assert ch in '.#'
    node = Node((r, c))
    node.wall = ch == '#'
    node.coords = (r, c, 0)
    return node

  nodes = [[MakeNode(r, c, ch) for c, ch in enumerate(row)] for r, row in enumerate(grid)]

  def FindRight(r, c):
    while True:
      c = (c + 1) % len(nodes[r])
      if nodes[r][c] is not None:
        return nodes[r][c]

  def FindDown(r, c):
    while True:
      r = (r + 1) % len(nodes)
      if c < len(nodes[r]) and nodes[r][c] is not None:
        return nodes[r][c]

  for r, row in enumerate(nodes):
    for c, node in enumerate(row):
      if node is not None:
        Connect(node, RIGHT, FindRight(r, c), LEFT)
        Connect(node, DOWN, FindDown(r, c), UP)

  # Start leftmost column in the topmost row.
  return next(node for row in nodes for node in row if node is not None)


def MarkCubeGraph(grid, start):
  # Do a flood fill to paint the cube with the walls of the grid (which we need
  # for the simulation), and to mark the source grid coordinates (which we need
  # to compute the final answer). We start with the leftmost nonblank character
  # on the top row.
  i = 0
  while grid[0][i].isspace(): i += 1
  seen = set([(0, i)])
  todo = [(0, i, start, 0)]
  for r, c, f, d in todo:
    # r, c are coordinates in the grid; f, d are the current node and the
    # direction on the node that corresponds with "right" on the grid.
    assert f.coords is None
    assert grid[r][c] in '#.'
    f.coords = (r, c, d)
    f.wall = grid[r][c] == '#'
    for step_dir in range(4):
      r2, c2 = r + DR[step_dir], c + DC[step_dir]
      if (0 <= r2 < len(grid) and 0 <= c2 < len(grid[r2]) and
          not grid[r2][c2].isspace() and (r2, c2) not in seen):
        f2, d2 = f.Step((step_dir + d) % 4)
        d2 = (d2 - step_dir) % 4
        seen.add((r2, c2))
        todo.append((r2, c2, f2, d2))


class TurnInstruction:
  def __init__(self, delta):
    self.delta = delta

  def Follow(self, f, d):
    d = (d + self.delta) % 4
    return f, d


class MoveInstruction:
  def __init__(self, dist):
    self.dist = dist

  def Follow(self, f, d):
    for _ in range(self.dist):
      f2, d2 = f.Step(d)
      if f2.wall:
        break
      f, d = f2, d2
    return f, d


def ParseInstruction(s):
  if s == 'L': return TurnInstruction(-1)
  if s == 'R': return TurnInstruction(+1)
  return MoveInstruction(int(s))


def ParseInput(input):
  part1, part2 = input.split('\n\n')
  grid = part1.split('\n')
  assert re.match('^([LR]|\d+)*$', part2)
  instructions = list(map(ParseInstruction, re.findall('[LR]|\d+', part2)))
  return grid, instructions


def CalculateCubeSize(grid):
  size = sqrt(sum(not ch.isspace() for row in grid for ch in row) / 6)
  assert size == int(size)
  return int(size)

class TestCase:
  def __init__(self, input):
    self.grid, self.instructions = ParseInput(input)

  def Solve(self, part2):
    if not part2:
      # Part 1: build a graph of nodes that wraps around to nonempty spaces
      start_node = BuildWrappingGraph(self.grid)
    else:
      # Part 2: apply the grid to a cube
      start_node = BuildCube(CalculateCubeSize(self.grid))
      MarkCubeGraph(self.grid, start_node)

    f, d = start_node, RIGHT

    # We should start from the “leftmost open tile of the top row of tiles”,
    # which is different from the start if the topleft nonspace character is #.
    # This doesn't happen in the sample or real test data, but let's implement
    # it anyway out of principle.
    # start_col = max(0, self.grid[0].index('#') - self.grid[0].index('.'))
    # for _ in range(start_col):
    #   f, d = f.Step(RIGHT)
    #   assert d == RIGHT

    # OK, now we're at the start, just follow the instructions one by one.
    for instr in self.instructions:
      f, d = instr.Follow(f, d)

    # Calculate the answer from the grid coordinates.
    r, c, right_dir = f.coords
    return 1000*(r + 1) + 4*(c + 1) + (d - right_dir) % 4


# Test sample case just to verify everything works as intended.
sample_test_case = TestCase('''\
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
''')
assert sample_test_case.Solve(part2=False) == 6032
assert sample_test_case.Solve(part2=True) == 5031

# Process real case.
real_test_case = TestCase(sys.stdin.read())
print(real_test_case.Solve(part2=False))
print(real_test_case.Solve(part2=True))
