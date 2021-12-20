from functools import reduce
import sys

class Node:

    def __init__(self, depth, *, value = None, left = None, right = None):
        if value is None:
            assert left is not None and right is not None
        if left is not None or right is not None:
            assert value is None

        self.depth = depth
        # If a leaf node:
        self.value = value
        self.prev = None
        self.next = None
        # If a branch node:
        self.left  = left
        self.right = right

    def LeftMost(self):
        return self.left.LeftMost() if self.left else self

    def RightMost(self):
        return self.right.RightMost() if self.right else self

    def IsLeaf(self):
        assert (self.left is None) == (self.right is None)
        return self.left is None

    def IsBranch(self):
        return not self.IsLeaf()

    def Connect(a, b):
        assert a.IsLeaf()
        assert b.IsLeaf()
        a.next = b
        b.prev = a

    def Explode(self):
        assert self.IsBranch()
        assert self.left.IsLeaf()
        assert self.right.IsLeaf()
        l = self.left
        r = self.right
        self.value = 0
        self.left = self.right = None
        if l.prev:
            l.prev.value += l.value
            Node.Connect(l.prev, self)
        if r.next:
            r.next.value += r.value
            Node.Connect(self, r.next)

    def Split(self, v, w):
        assert self.IsLeaf()
        p = self.prev
        n = self.next
        self.prev = self.next = self.value = None
        self.left = Node(self.depth + 1, value=v)
        self.right = Node(self.depth + 1, value=w)
        Node.Connect(self.left, self.right)
        if p:
            Node.Connect(p, self.left)
        if n:
            Node.Connect(self.right, n)

    def Magnitude(self):
        if self.IsLeaf():
            return self.value
        else:
            return self.left.Magnitude()*3 + self.right.Magnitude()*2

    def __str__(self):
        if self.IsBranch():
            return '[' + str(self.left) + ',' + str(self.right) + ']'
        if self.IsLeaf():
            return str(self.value)


def Reduce(t):
    '''Reduces a tree and returns the updated version.'''

    MAX_DEPTH = 4
    MAX_VALUE = 10

    def DoExplosions(t):
        if not t.IsBranch():
            return t

        if t.depth < MAX_DEPTH:
            DoExplosions(t.left)
            DoExplosions(t.right)
            return

        t.Explode()


    def DoSplits(t):
        l = t.LeftMost()
        while l:
            assert l.IsLeaf()
            if l.value < MAX_VALUE:
                l = l.next
            else:
                v = l.value // 2
                w = l.value - v
                if l.depth < MAX_DEPTH:
                    l.Split(v, w)
                    l = l.left
                else:
                    p = l.prev
                    n = l.next
                    l.value = 0
                    if p:
                        p.value += v
                    if n:
                        n.value += w
                    l = p if p else n

    DoExplosions(t)
    DoSplits(t)


def Add(a, b):
    def Copy(node, depth):
        if node.IsLeaf():
            return Node(depth, value=node.value)
        else:
            return Node(depth, left=Copy(node.left, depth + 1), right=Copy(node.right, depth + 1))

    root = Node(0, left=Copy(a, 1), right=Copy(b, 1))

    leaves = []
    def FindLeaves(t):
        if t.IsLeaf():
            leaves.append(t)
        else:
            FindLeaves(t.left)
            FindLeaves(t.right)
    FindLeaves(root)

    last = None
    for next in leaves:
        if last is not None:
            last.Connect(next)
        last = next

    Reduce(root)
    return root


def Parse(line):
    '''Parses a string into a nested list of integers. Example: Parse("[1,[2,3]]") == [1,[2,3]].'''
    stack = [[]]
    expect_terminator = False
    for ch in line:
        if ch == '[':
            assert not expect_terminator
            stack.append([])
        elif ch == ']':
            assert expect_terminator
            v = stack.pop()
            stack[-1].append(v)
        elif ch == ',':
            assert expect_terminator
            expect_terminator = False
        elif ch.isdigit():
            # only single-digit integers are supported for this problem.
            assert not expect_terminator
            stack[-1].append(int(ch))
            expect_terminator = True
        else:
            assert ch.isspace()
    (root,), = stack
    return root


def Construct(value, *, depth = 0):
    '''Constructs a Node from a nested list of integers.'''
    if isinstance(value, int):
        return Node(depth, value=value)
    else:
        a, b = (Construct(v, depth=depth + 1) for v in value)
        Node.Connect(a.RightMost(), b.LeftMost())
        return Node(depth, left=a, right=b)


# Read input
numbers = [Construct(Parse(line)) for line in sys.stdin]

# Part 1
print(reduce(Add, numbers).Magnitude())

# Part 2
print(max(Add(a, b).Magnitude() for a in numbers for b in numbers if a != b))
