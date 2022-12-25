#!/usr/bin/env pypy3

from random import randint
import sys

# Tree where only leaves have values. Every interior node has both left and right values.
class Node:
  def __init__(self, parent):
    self.parent = parent

class Branch(Node):
  def __init__(self, parent, left, right):
    super().__init__(parent)
    self.left = left
    self.right = right
    self.size = left.Size() + right.Size()

  def Size(self):
    return self.size

  def str(self):
    return 'Branch(size=%s)' % (self.size)

class Leaf(Node):
  def __init__(self, parent, value):
    super().__init__(parent)
    self.value = value

  def Size(self):
    return 1

  def str(self):
    return 'Leaf(value=%s)' % (self.value)

def IndexOf(leaf):
  i = 0
  child = leaf
  node = leaf.parent
  while node is not None:
    if child is node.right:
      i += node.left.Size()
    child = node
    node = node.parent
  return i

# Returns the new root.
def Remove(leaf):
  parent = leaf.parent
  assert parent is not None  # size at least 2
  grandparent = parent.parent
  if leaf == parent.right:
    sibling = parent.left
  else:
    assert leaf == parent.left
    sibling = parent.right

  leaf.parent = None
  sibling.parent = grandparent
  if grandparent is None:
    sibling.parent = None
    return sibling

  if parent is grandparent.right:
    grandparent.right = sibling
  else:
    assert parent is grandparent.left
    grandparent.left = sibling
  root = grandparent
  root.size -= 1
  while root.parent is not None:
    root = root.parent
    root.size -= 1
  return root

def Combine(parent, child1, child2):
  branch = Branch(parent, child1, child2)
  child1.parent = branch
  child2.parent = branch
  return branch

def InsertAt(node, parent, index, leaf):
  '''Inserts a node and returns the new root.'''
  assert 0 <= index <= node.Size()
  assert leaf.parent is None
  if isinstance(node, Leaf):
    return Combine(parent, leaf, node)
  else:
    node.size += 1
    leaf_size = node.left.Size()
    if index < leaf_size:
      node.left = InsertAt(node.left, node, index, leaf)
    else:
      node.right = InsertAt(node.right, node, index - leaf_size, leaf)
    return node

def TreeValues(node):
  if isinstance(node, Leaf):
    yield node.value
  else:
    yield from TreeValues(node.left)
    yield from TreeValues(node.right)

def CreateTree(nodes):
  while len(nodes) > 1:
    pairs = len(nodes) // 2
    nodes = [Combine(None, nodes[i], nodes[i + 1]) for i in range(0, pairs * 2, 2)] + nodes[2*pairs:]
  return nodes[0]

def PrintTree(node, indent = 0, file=sys.stderr):
  if isinstance(node, Leaf):
    print('  '*indent + str(node.value), file=file)
    return
  print('  '*indent + 'left:', file=file)
  PrintTree(node.left, indent + 1, file=file)
  print('  '*indent + 'right:', file=file)
  PrintTree(node.right, indent + 1, file=file)

def CheckIntegrity(node, parent):
  assert node.parent == parent
  if isinstance(node, Leaf):
    size = 1
  else:
    left_size = CheckIntegrity(node.left, node)
    right_size = CheckIntegrity(node.right, node)
    size = left_size + right_size
  assert node.Size() == size
  return size

def Depth(node):
  if isinstance(node, Leaf):
    return 1
  return max(Depth(node.left), Depth(node.right)) + 1


def Solve(numbers, multiplier, mix_count):
  leaves = [Leaf(None, number * multiplier) for number in numbers]
  root = CreateTree(leaves)
  for _ in range(mix_count):
    assert CheckIntegrity(root, None) == len(leaves)
    #print('depth', Depth(root), file=sys.stderr)
    for leaf in leaves:
      #print(list(TreeValues(root)))
      old_index = IndexOf(leaf)
      new_index = (old_index + leaf.value) % (len(leaves) - 1)
      #print(old_index, new_index)
      root = Remove(leaf)
      InsertAt(root, None, new_index, leaf)

      #assert CheckSize(root) == len(leaves)
      #PrintTree(root)
      #print(list(TreeValues(root)))


  values = list(TreeValues(root))
  start_pos = values.index(0)
  values = values[start_pos:] + values[:start_pos]
  #print(values[1000 % len(values)], values[2000 % len(values)], values[3000 % len(values)])
  return values[1000 % len(values)] + values[2000 % len(values)] + values[3000 % len(values)]


numbers = [int(line) for line in sys.stdin]
print(Solve(numbers, 1, 1))
print(Solve(numbers, 811589153, 10))
