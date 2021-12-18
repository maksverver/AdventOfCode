from functools import reduce
import sys

class Node:

    def Construct(value):
        '''Constructs a Node from a nested list of integers.'''
        if isinstance(value, int):
            return Leaf(value)
        else:
            a, b = map(Node.Construct, value)
            Leaf.Connect(a.RightMost(), b.LeftMost())
            return Branch(a, b)


class Leaf(Node):
    '''A leaf node has a single integer value and is connected to other leafs in a linked list.'''
    def __init__(self, value, prev = None, next = None):
        self.value = value
        self.prev = None
        self.next = None

    def LeftMost(self):
        return self

    def RightMost(self):
        return self

    def Connect(a, b):
        a.next = b
        b.prev = a

    def Magnitude(self):
        return self.value

    def __str__(self):
        return str(self.value)


class Branch(Node):
    '''A branch node has exactly two child nodes (either both branches, or both leaves).'''
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def LeftMost(self):
        return self.left.LeftMost()

    def RightMost(self):
        return self.right.RightMost()

    def Magnitude(self):
        return self.left.Magnitude()*3 + self.right.Magnitude()*2

    def __str__(self):
        return f'[{self.left},{self.right}]'


def Reduce(t):
    '''Reduces a tree and returns the updated version.'''

    def Explode(t):
        l = Leaf(0)
        p = t.left.prev
        if p:
            p.value += t.left.value
            p.Connect(l)
        n = t.right.next
        if n:
            n.value += t.right.value
            l.Connect(n)
        return l


    # Actually processes all explosions at once, which I think is safe.
    def DoExplosions(t, depth):
        if not isinstance(t, Branch):
            return t

        if depth < 4:
            t.left = DoExplosions(t.left, depth + 1)
            t.right = DoExplosions(t.right, depth + 1)
            return t

        return Explode(t)


    def TrySplit(t):
        if isinstance(t, Branch):
            t.left, split = TrySplit(t.left)
            if not split:
                t.right, split = TrySplit(t.right)
            return t, split

        if t.value < 10:
            return t, False

        a = Leaf(t.value // 2)
        b = Leaf(t.value - t.value // 2)
        Leaf.Connect(a, b)
        if t.prev:
            Leaf.Connect(t.prev, a)
        if t.next:
            Leaf.Connect(b, t.next)
        Leaf.Connect(a, b)
        c = Branch(a, b)
        return c, True

    while True:
        t = DoExplosions(t, 0)
        t, split = TrySplit(t)
        if not split:
            break

    return t


def Add(a, b):
    '''Adds two nodes and returns the result. Don't use the inputs afterwards!'''
    Leaf.Connect(a.RightMost(), b.LeftMost())
    return Reduce(Branch(a, b))


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


numbers = [Parse(line) for line in sys.stdin]
print(reduce(Add, (Node.Construct(number) for number in numbers)).Magnitude())
print(max(Add(Node.Construct(a), Node.Construct(b)).Magnitude() for a in numbers for b in numbers))
