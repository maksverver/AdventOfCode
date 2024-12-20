#!/bin/env pypy3

from math import floor, ceil
from random import choice, randrange, sample, shuffle, uniform, seed

import sys

sys.path.append('../../library-code/')

from disjointset import DisjointSet

def shuffled(iterable):
    l = list(iterable)
    shuffle(l)
    return l

def GenerateSpanningTree(H, W, extra_edge_chance=0):
    all_edges = (
        [((r, c), (r, c + 1)) for r in range(H) for c in range(W - 1)] +
        [((r, c), (r + 1, c)) for r in range(H - 1) for c in range(W)])

    vertices = [(r, c) for r in range(H) for c in range(W)]

    ds = DisjointSet(vertices)

    edges = set()
    for e in shuffled(all_edges):
        v, w = e
        if ds.Union(v, w) or uniform(0, 1) < extra_edge_chance:
            edges.add(e)
    return vertices, edges

def FindFurthestPoint(grid, start):
    def Neighbors(v):
        r, c = v
        assert grid[r][c] == '.'
        return [(r2, c2) for (r2, c2) in [(r-1, c), (r, c-1), (r, c+1), (r+1,c)] if grid[r2][c2] != '#']

    seen = {start}
    todo = [start]
    for v in todo:
        for w in shuffled(Neighbors(v)):
            if w not in seen:
                seen.add(w)
                todo.append(w)
    return todo[-1]

def MakeMaze(H, W, perfect=True):
    assert H % 2 == 1 and W % 2 == 1
    vertices, edges = GenerateSpanningTree(H // 2, W // 2, extra_edge_chance=0 if perfect else 0.02)
    grid = [['#'] * W for _ in range(H)]
    for v, w in edges:
        r1, c1 = v
        r2, c2 = w
        grid[2*r1 + 1][2*c1 + 1] = grid[2*r2 + 1][2*c2 + 1] = grid[r1 + r2 + 1][c1 + c2 + 1] = '.'

    start=choice([(r, c) for r in range(H) for c in range(W) if grid[r][c] == '.'])
    end=FindFurthestPoint(grid, start)
    grid[start[0]][start[1]] = 'S'
    grid[end[0]][end[1]] = 'E'
    return grid

def MakeUnicursalMaze(H, W):
    assert H % 4 == 1 and W % 4 == 1
    vertices, edges = GenerateSpanningTree(H // 4, W // 4)
    grid = [['#'] * W for _ in range(H)]
    for v, w in edges:
        r1, c1 = v
        r2, c2 = w
        dr = r2 - r1
        dc = c2 - c1
        for i in range(-1, 6):
            for w in (-1, 0, 1):
                grid[4*r1 + dr*i + 2 + w*dc][4*c1 + dc*i + 2 - w*dr] = '.'
    for v, w in edges:
        r1, c1 = v
        r2, c2 = w
        dr = r2 - r1
        dc = c2 - c1
        for i in range(5):
            grid[4*r1 + dr*i + 2][4*c1 + dc*i + 2] = '#'
    return grid

def PrintGrid(grid, file=sys.stderr):
    for row in grid:
        print(''.join(row), file=file)

def CreateInput(filename, grid):
    with open(filename, 'wt') as f:
        PrintGrid(grid, f)

def FindRandomPath(grid):
    def Neighbors(v):
        r, c = v
        assert grid[r][c] == '.'
        return [(r2, c2) for (r2, c2) in [(r-1, c), (r, c-1), (r, c+1), (r+1,c)] if grid[r2][c2] != '#']

    start = (1, 1)
    u = start
    v = choice(Neighbors(start))
    path = [u]
    while v != start:
        path.append(v)
        w, = (n for n in Neighbors(v) if n != u)
        u, v = v, w
    i = randrange(len(path))
    return path[i:] + path[:i]

def ManhattanDistance(v, w):
    r1, c1 = v
    r2, c2 = w
    return abs(r1 - r2) + abs(c1 - c2)

def MarkBeginAndEnd(grid, fill_all=True):
    # Only works for the unicursal mazes
    path = FindRandomPath(grid)

    def Set(v, ch):
        r, c = v
        assert grid[r][c] == '.'
        grid[r][c] = ch

    start = path[0]
    for i, v in enumerate(path):
        if ManhattanDistance(path[0], v) > 20:
            break
    else:
        print('Maze too small!', file=sys.stderr)
        assert False
    assert i > 2

    fill_char = '#'
    if fill_all:
        for j in range(1, i):
            Set(path[j], fill_char)
    else:
        Set(path[1], fill_char)
        Set(path[i - 1], fill_char)
    Set(path[0], 'S')
    Set(path[i], 'E')

def DuplicateRow(grid):
    # Duplicate row, but not one containing start/finish
    i = randrange(len(grid) // 2 - 1) * 2 + 2
    return grid[:i] + [list(grid[i])] + grid[i:]

def DuplicateCol(grid):
    # Duplicate col, but not one containing start/finish
    i = randrange(len(grid[0]) // 2 - 1) * 2 + 2
    return [row[:i+1] + row[i:] for row in grid]

def DuplicateRowCol(grid):
    return DuplicateRow(DuplicateCol(grid))


def MakeRegularCase(filename, H, W, seed_value):
    # Unicursal grid
    seed(seed_value)
    grid = MakeUnicursalMaze(H, W)
    MarkBeginAndEnd(grid)
    CreateInput(filename, grid)


def MakeDupeCase(filename, H, W, seed_value):
    # Unicursal grid with duplicated row/column to create some odd shortcuts
    # Also makes the path less unique.
    seed(seed_value)
    grid = DuplicateRowCol(MakeUnicursalMaze(H, W))
    MarkBeginAndEnd(grid)
    CreateInput(filename, grid)

def MakeInaccessibleAreaCase(filename, H, W, seed_value):
    # Unicursal grid with an inaccessible open area
    seed(seed_value)
    vertices, edges = GenerateSpanningTree(H, W)
    grid = MakeUnicursalMaze(H, W)
    MarkBeginAndEnd(grid, fill_all=False)
    CreateInput(filename, grid)

def MakePerfectMazeCase(filename, H, W, seed_value):
    # Perfect maze (many dead ends!)
    seed(seed_value)
    grid = MakeMaze(H, W)
    CreateInput(filename, grid)

def MakeMazeWithCyclesCase(filename, H, W, seed_value):
    seed(seed_value)
    grid = MakeMaze(H, W, perfect=False)
    CreateInput(filename, grid)


# Regular cases of various square sizes
#MakeRegularCase('aoc-2024-day-20-challenge-1.txt',  501,  501, seed_value=31337 + 31*1)
#MakeRegularCase('aoc-2024-day-20-challenge-2.txt', 1501, 1501, seed_value=31337 + 31*2)
#MakeRegularCase('aoc-2024-day-20-challenge-3.txt', 5001, 5001, seed_value=31337 + 31*3)

# Weird cases
#MakeDupeCase            ('aoc-2024-day-20-challenge-4.txt', 201, 301, seed_value=31337 + 31*4)
#MakeInaccessibleAreaCase('aoc-2024-day-20-challenge-5.txt', 301, 201, seed_value=31337 + 31*5)
MakePerfectMazeCase     ('aoc-2024-day-20-challenge-6.txt', 301, 301, seed_value=31337 + 31*6)
MakeMazeWithCyclesCase  ('aoc-2024-day-20-challenge-7.txt', 301, 301, seed_value=31337 + 31*7)
