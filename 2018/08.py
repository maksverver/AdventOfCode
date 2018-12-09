import sys

class Node(object):
    def __init__(self, numbers):
        n = next(numbers)
        m = next(numbers)
        self.children = [Node(numbers) for _ in range(n)]
        self.metadata = [next(numbers) for _ in range(m)]

def Checksum(node):
    return sum(node.metadata) + sum(map(Checksum, node.children))

def Value(node):
    if not node.children:
        return sum(node.metadata)
    return sum(Value(node.children[i - 1])
        for i in node.metadata if 1 <= i <= len(node.children))

tree = Node(map(int, sys.stdin.readline().split()))
print(Checksum(tree))
print(Value(tree))
