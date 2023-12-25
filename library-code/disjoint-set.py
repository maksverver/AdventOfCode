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


if __name__ == '__main__':
  ds = DisjointSet({'foo', 'bar', 'baz'})

  assert ds.Find('foo') == 'foo'
  assert ds.Find('bar') == 'bar'
  assert ds.Find('baz') == 'baz'

  assert ds.Size('foo') == 1
  assert ds.Size('bar') == 1
  assert ds.Size('baz') == 1

  assert ds.Same('foo', 'bar') == False
  assert ds.Same('foo', 'baz') == False
  assert ds.Same('bar', 'baz') == False

  res = ds.Union('foo', 'foo')
  assert res == False

  res = ds.Union('foo', 'bar')
  assert res == True

  assert ds.Size('foo') == 2
  assert ds.Size('bar') == 2
  assert ds.Size('baz') == 1

  assert ds.Same('foo', 'bar') == True 
  assert ds.Same('foo', 'baz') == False
  assert ds.Same('bar', 'baz') == False

  res = ds.Union('foo', 'baz')
  assert res == True

  assert ds.Size('foo') == 3
  assert ds.Size('bar') == 3
  assert ds.Size('baz') == 3

  assert ds.Same('foo', 'bar') == True 
  assert ds.Same('foo', 'baz') == True 
  assert ds.Same('bar', 'baz') == True

  res = ds.Union('bar', 'baz')
  assert res == False
