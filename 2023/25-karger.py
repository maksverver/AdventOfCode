# Solution to day 25 using Karger's algorithm [1], which is surprisingly simple
# to implement if you have a DisjointSet data structure, which allows an
# implementation similar to Kruskal's algorithm [2].
#
# Unfortunately this is not very efficient on large inputs.
#
#  1. https://en.wikipedia.org/wiki/Karger%27s_algorithm
#  2. https://en.wikipedia.org/wiki/Kruskal%27s_algorithm
#

import sys
from random import shuffle


class DisjointSet:
  '''Disjoint Set data structure implementing path splitting and union by size.

      The data structure tracks the partitioning of a fixed set of elements into
      any number of disjoint sets, while supporting the following operations
      efficiently (i.e., in nearly O(1) amortized time):

        - Which set does this element belong to? (Find())
        - Merge the sets to which two elements belong? (Union())

      This implementation also adds Same() and Size() as convenience methods.

      More information: https://en.wikipedia.org/wiki/Disjoint-set_data_structure'''
  def __init__(self, members):
    '''Creates disjoint singleton sets for all elements of `members`.'''
    self.parents = {k: k for k in members}
    self.sizes = {k: 1 for k in members}

  def Find(self, x):
    '''Returns a representative element for the set to which `x` belongs.'''
    while (y := self.parents[x]) != x:
      x, self.parents[x] = y, self.parents[y]
    return x

  def Union(self, x, y):
    '''Combines the sets to which `x` and `y` belong into a single set.

        Returns True if two disjoint sets were merged, or False if `x` and `y``
        already belonged to the same set.'''
    x = self.Find(x)
    y = self.Find(y)
    if x == y: return False
    if self.sizes[x] < self.sizes[y]: x, y = y, x
    self.sizes[x] += self.sizes[y]
    self.parents[y] = x
    del self.sizes[y]
    return True

  def Same(self, x, y):
    '''Returns whether `x` and `y` belong to the same set.'''
    return self.Find(x) == self.Find(y)

  def Size(self, x):
    '''Returns the size of the set to which `x` belongs.'''
    return self.sizes[self.Find(x)]



def ReadInput(file):
  nodes = set()
  edges = []
  for line in file:
    v, ws = line.split(': ')
    nodes.add(v)
    for w in ws.split():
      nodes.add(w)
      edges.append((v, w))
  return nodes, edges


nodes, edges = ReadInput(sys.stdin)


while True:
  shuffle(edges)
  size = len(nodes)
  it = iter(edges)
  ds = DisjointSet(nodes)
  while size > 2: size -= ds.Union(*next(it))
  cut = 0
  answer = None
  for v, w in it:
    if not ds.Same(v, w):
      cut += 1
      if answer is None:
        answer = ds.Size(v) * ds.Size(w)
  if cut == 3:
    print(answer)
    break
