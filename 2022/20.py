class Node:
  def __init__(self, value):
    self.value = value
    self.left = None
    self.right = None

  def MoveRight(self, n):
    self.left.right = self.right
    self.right.left = self.left
    for _ in range(n):
      self.right = self.right.right
    self.left = self.right.left
    self.right.left = self.left.right = self

  def __repr__(self):
    return 'Node(%d)' % self.value


def SwapNodes(a, b, c, d):
  '''Swaps nodes b and c in the sequence a, b, c, d.'''
  a.right = c
  c.right = b
  b.right = d
  d.left = b
  b.left = c
  c.left = a


def Sequence(start_node):
  '''Generates the sequence of node moving right from the giving start node.'''
  node = start_node
  while True:
    yield node
    node = node.right
    if node == start_node:
      break


def Solve(numbers, multiplier, mix_count):
  nodes = [Node(number * multiplier) for number in numbers]
  for i, node in enumerate(nodes):
    node.left = nodes[(i - 1) % len(nodes)]
    node.right = nodes[(i + 1) % len(nodes)]

  for _ in range(mix_count):
    for node in nodes:
      node.MoveRight(node.value % (len(nodes) - 1))

  start_node, = (node for node in nodes if node.value == 0)
  seq = list(Sequence(start_node))

  return seq[1000 % len(seq)].value + seq[2000 % len(seq)].value + seq[3000 % len(seq)].value


import sys
numbers = [int(line) for line in sys.stdin]
print(Solve(numbers, 1, 1))
print(Solve(numbers, 811589153, 10))
