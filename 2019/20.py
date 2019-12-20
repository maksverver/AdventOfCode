from collections import defaultdict
import sys

grid = tuple(line.rstrip() for line in sys.stdin)

def BuildGraph(recursive):
    def LetterAt(r, c):
        return grid[r][c] if 0 <= r < len(grid) and 0 <= c < len(grid[r]) else ' '

    graph = {}  # (row, col) -> [((adjacent row, adjacent col), level_delta), ...]
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == '.':
                graph[r, c] = [((rr, cc), 0)
                    for rr, cc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1))
                    if LetterAt(rr, cc) == '.']

    portals = defaultdict(list)  # "AB" -> [(adjacent_r, adjacent_c), ...]
    for r1, row in enumerate(grid):
        for c1, ch1 in enumerate(row):
            if ch1.isupper():
                for (r2, c2), (r3, c3) in (
                        ((r1 + 1, c1), (r1 - 1, c1)),   # opening above
                        ((r1 + 1, c1), (r1 + 2, c1)),   # opening below
                        ((r1, c1 + 1), (r1, c1 - 1)),   # opening to the left
                        ((r1, c1 + 1), (r1, c1 + 2))):  # opening to the right
                    ch2 = LetterAt(r2, c2)
                    if ch2.isupper() and LetterAt(r3, c3) == '.':
                        portals[ch1 + ch2].append((r3, c3))

    def IsOutside(r, c):
        return r < 3 or c < 3 or r >= len(grid) - 3 or c >= len(grid[r]) - 3

    for label, adjacent in portals.items():
        if len(adjacent) == 1:
            assert label in ('AA', 'ZZ')
            continue
        a, b = adjacent
        assert IsOutside(*a) ^ IsOutside(*b)
        delta = IsOutside(*b) - IsOutside(*a) if recursive else 0
        graph[a].append((b, +delta))
        graph[b].append((a, -delta))

    return portals, graph


def FindShortestPath(graph, start, finish):
    def Adjacent(v):
        p, level = v
        for q, delta in graph[p]:
            if level + delta >= 0:
                yield (q, level + delta)

    dist = {start: 0}
    todo = [start]
    for v in todo:
        if v == finish:
            return dist[v]
        for w in Adjacent(v):
            if w not in dist:
                dist[w] = dist[v] + 1
                todo.append(w)


def Solve(recursive):
    portals, graph = BuildGraph(recursive)
    start, = portals['AA']
    finish, = portals['ZZ']
    return FindShortestPath(graph, (start, 0), (finish, 0))

print(Solve(recursive=False))  # Part 1
print(Solve(recursive=True))   # Part 2
