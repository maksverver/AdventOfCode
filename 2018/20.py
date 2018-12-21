from collections import defaultdict
import sys

class TreeNode(object):
    def __init__(self):
        self.next = None

class Char(TreeNode):
    def __init__(self, char):
        super().__init__()
        self.char = char

class Branch(TreeNode):
    def __init__(self, alts):
        super().__init__()
        self.alts = tuple(alts)
        for i,alt in enumerate(alts):
            print(i,alt)

class DagNode():
    def __init__(self, prefix, alts):
        self.prefix = prefix
        self.alts = alts

def Parse(line):
    assert line[0] == '^' and line[-1] == '$'
    # each element on the stack is a list of alternatives
    # each alternative is a list of sequential nodes
    stack = [[[]]]
    def Append(node):
        seq = stack[-1][-1]
        if seq:
            seq[-1].next = node
        seq.append(node)
    def First(seq):
        return seq[0] if seq else None
    for ch in line[1:-1]:
        if ch == '(':
            stack.append([[]])
        elif ch == ')':
            Append(Branch(map(First, stack.pop())))
        elif ch == '|':
            stack[-1].append([])
        else:
            Append(Char(ch))
    assert len(stack) == 1 and len(stack[0]) == 1
    return stack[0][0][0]

def MakeDag(node, next_dag):
    if not node:
        return next_dag
    prefix = ''
    while node and type(node) == Char:
        prefix += node.char
        node = node.next
    if not node:
        if next_dag:
            prefix += next_dag.prefix
            alts = next_dag.alts
        else:
            alts = None
    else:
        assert type(node) == Branch
        next_dag = MakeDag(node.next, next_dag)
        alts = tuple(MakeDag(alt, next_dag) for alt in node.alts)
    return DagNode(prefix, alts)

DIRS = {
    'N': ( -1,  0),
    'E': (  0, +1),
    'S': ( +1,  0),
    'W': (  0, -1),
}

def CalculateDoors(dag):
    doors = defaultdict(set)
    seen = set()
    def Search(dag, r, c):
        if not dag or (dag, r, c) in seen:
            return
        seen.add((dag, r, c))
        for ch in dag.prefix:
            dr, dc = DIRS[ch]
            nr, nc = r + dr, c + dc
            doors[r, c].add((nr, nc))
            doors[nr, nc].add((r, c))
            r, c = nr, nc
        if dag.alts:
            for alt in dag.alts:
                Search(alt, r, c)
    Search(dag, 0, 0)
    return doors

def CalculateDistances(doors):
    distances = {(0, 0): 0}
    distance = 0
    todo = [(0,0)]
    todo_next = []
    while todo:
        distance += 1
        for v in todo:
            for w in doors[v]:
                if w not in distances:
                    distances[w] = distance
                    todo_next.append(w)
        todo = todo_next
        todo_next = []
    return distances

line = sys.stdin.readline().strip()
tree = Parse(line)
dag = MakeDag(tree, None)
doors = CalculateDoors(dag)
distances = CalculateDistances(doors)

print(max(distances.values()))
print(sum(distance >= 1000 for distance in distances.values()))
