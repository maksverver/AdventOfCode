import re
import sys

# Directions (right, down, left, up)
DR = [0, 1,  0, -1]
DC = [1, 0, -1,  0]

DIR_IDS = 'RDLU'
FACE_IDS = '012345'

# Position of faces in the input
#
# Sample input
#
#          +---+
#          | 0 |
#  +---+---+---+
#  | 1 | 2 | 3 |
#  +---+---+---+---+
#          | 4 | 5 |
#          +---+---+

sample_template = [
  [ -1, -1, 0 ],
  [  1,  2, 3 ],
  [ -1, -1, 4, 5 ],
]

sample_face_size = 4

# Edges. Each edge consists of four parts:
#
#  - source face (0..5)
#  - source edge location (U/L/R/D, relative to the center of the face)
#  - whether the coordinates along the edge run in the same (+) or opposite (-) direction
#  - destination face
#  - destination edge location
#
sample_edges_part1 = [
  '0U+4D', '0L+0R', '0D+3U', '1L+3R',
  '1R+2L', '1D+1U', '2U+2D', '2R+3L',
  '3D+4U', '4L+5R', '4R+5L', '5U+5D',
]

sample_edges_part2 = [
  '0U-1U', '0L+2U', '0D+3U', '0R-5R',
  '1L-5D', '1R+2L', '1D-4D', '2R+3L',
  '2D-4L', '3R-5U', '3D+4U', '4R+5L',
]

# Real test input
#
#      +---+---+
#      | 0 | 1 |
#      +---+---+
#      | 2 |
#  +---+---+
#  | 3 | 4 |
#  +---+---+
#  | 5 |
#  +---+

real_template = [
  [ -1,  0,  1 ],
  [ -1,  2 ],
  [  3,  4 ],
  [  5 ],
]

real_edges_part1 = [
  '0U+4D', '0L+1R', '0R+1L', '0D+2U',
  '1U+1D', '2R+2L', '2D+4U', '3U+5D',
  '3L+4R', '3D+5U', '3R+4L', '5L+5R',
]

real_edges_part2 = [
  '0R+1L', '0D+2U', '0L-3L', '0U+5L',
  '1R-4R', '1D+2R', '1U+5D', '2D+4U',
  '2L+3U', '3R+4L', '3D+5U', '4D+5R',
]

real_face_size = 50


def GetFaceCoords(template, size):
  '''Parses the coordinates of each face from a template (see below).

    For each face, returns a tuple (r1, c1, r2, c2) describing the location of
    the face in the flattened input file. This is used to parse the grid and
    calculate the final answer.'''
  faces = [None]*6
  for r, row in enumerate(template):
    for c, idx in enumerate(row):
      if idx >= 0:
        assert faces[idx] is None
        faces[idx] = (r*size, c*size, (r + 1)*size, (c + 1)*size)
  return faces


def GetFaceConnections(edges):
  '''For each face and each side (right, down, left, up), returns a tuple
    (other face, direction, invert position) that it connects to.'''
  connections = [[None]*4 for _ in range(6)]
  for s in edges:
    assert len(s) == 5
    f1 = FACE_IDS.index(s[0])
    d1 = DIR_IDS.index(s[1])
    inv = '+-'.index(s[2])
    f2 = FACE_IDS.index(s[3])
    d2 = DIR_IDS.index(s[4])
    assert connections[f1][d1] is None
    assert connections[f2][d2] is None
    connections[f1][d1] = (f2, d2 ^ 2, bool(inv))
    connections[f2][d2] = (f1, d1 ^ 2, bool(inv))
  return connections


def GetFaces(face_coords, size, grid):
  '''Cuts the 6 faces of the cube out of the the flat input text file.
    The result is a list with 6 elements, each element contains a cube face as
    a list of `size` strings of length `size` each.'''
  faces = [[row[c1:c2] for row in grid[r1:r2]]
      for (r1, c1, r2, c2) in face_coords]
  assert all(ch in '.#' for face in faces for row in face for ch in row)
  return faces


class Topology:
  def __init__(self, size, edges):
    self.size = size
    self.connections = GetFaceConnections(edges)

  def RCtoPos(self, r, c, d):
    if d == 0: return r  # right
    if d == 1: return c  # down
    if d == 2: return r  # left
    if d == 3: return c  # up

  def PosToRC(self, d, pos):
    if d == 0: return (pos, 0)              # right
    if d == 1: return (0, pos)              # down
    if d == 2: return (pos, self.size - 1)  # left
    if d == 3: return (self.size - 1, pos)  # up

  def Step(self, f, r, c, d):
    f2, r2, c2, d2 = f, r + DR[d], c + DC[d], d
    if not (0 <= r2 < self.size and 0 <= c2 < self.size):
      # Cross the edge of a face:
      f2, d2, inv = self.connections[f][d]
      pos = self.RCtoPos(r, c, d)
      if inv: pos = self.size - 1 - pos
      r2, c2 = self.PosToRC(d2, pos)
    return (f2, r2, c2, d2)


class TurnInstruction:
  def __init__(self, ch):
    if ch == 'L': self.delta = -1
    if ch == 'R': self.delta = +1

  def Follow(self, topology, faces, f, r, c, d):
    d = (d + self.delta) % 4
    return (f, r, c, d)


class MoveInstruction:
  def __init__(self, dist):
    self.dist = int(dist)

  def Follow(self, topology, faces, f, r, c, d):
    for _ in range(self.dist):
      f2, r2, c2, d2 = topology.Step(f, r, c, d)
      if faces[f2][r2][c2] == '#':
        break
      assert faces[f2][r2][c2] == '.'
      f, r, c, d = f2, r2, c2, d2
    return (f, r, c, d)


class TestCase:
  def __init__(self, template, size, input):
    self.grid, self.instructions = ParseInput(input)
    self.face_coords = GetFaceCoords(template, size)
    self.faces = GetFaces(self.face_coords, size, self.grid)

  def Solve(self, topology):
    # Keep track of the current position as: face index, row, column, direction.
    # Row and column are relative to the current face. We start from the topmost/
    # leftmost one, which we assume to be face 0.
    f = 0
    r = 0
    c = self.faces[f][r].index('.')
    d = 0

    for instr in self.instructions:
      f, r, c, d = instr.Follow(topology, self.faces, f, r, c, d)

    fr, fc, _, _ = self.face_coords[f]
    return 1000*(fr + r + 1) + 4*(fc + c + 1) + d


def ParseInput(input):
  part1, part2 = input.split('\n\n')
  grid = part1.split('\n')

  assert re.match('^[LR0-9]*$', part2)
  instructions = [
    TurnInstruction(s) if s in 'LR' else MoveInstruction(s)
    for s in re.findall('[LR]|[0-9]+', part2)]

  return grid, instructions


sample_input = '''\
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
'''

sample_test_case = TestCase(sample_template, sample_face_size, sample_input)
sample_topology_1 = Topology(sample_face_size, sample_edges_part1)
sample_topology_2 = Topology(sample_face_size, sample_edges_part2)

assert sample_test_case.Solve(sample_topology_1) == 6032
assert sample_test_case.Solve(sample_topology_2) == 5031


real_input = sys.stdin.read()
real_test_case = TestCase(real_template, real_face_size, real_input)
real_topology_1 = Topology(real_face_size, real_edges_part1)
real_topology_2 = Topology(real_face_size, real_edges_part2)

print(real_test_case.Solve(real_topology_1))
print(real_test_case.Solve(real_topology_2))
