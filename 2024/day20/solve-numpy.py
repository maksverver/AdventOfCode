import functools
import numpy as np
import sys
import time

def Time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        finish = time.perf_counter()
        duration = finish - start
        print(f'{func.__name__}{args} took {duration:.4f} seconds')
        return result
    return wrapper

# Define value used as infinity: larger than all distances that will reasonably
# occur, while being able to fit in a 32-bit integer twice without overlow.
INF = 10**9

MAX_SHORTCUT = 20

# Read input grid from stdin. Separate function to allow garbage collection of
# intermediate data.
@Time
def ReadInput():
    global W, H, start, end, walls
    data = np.frombuffer(sys.stdin.buffer.read(), dtype=np.uint8)
    W = np.argwhere(data == ord('\n'))[0][0]
    assert len(data) % (W + 1) == 0
    H = len(data) // (W + 1)
    grid = data.reshape((H, W + 1))
    assert np.all(grid[:,W] == ord('\n'))
    grid = np.delete(grid, W, axis=1)
    start, = (tuple(map(int, a)) for a in np.argwhere(grid == ord('S')))
    end,   = (tuple(map(int, a)) for a in np.argwhere(grid == ord('E')))
    walls  = grid == ord('#')

ReadInput()


# Breadth-first search to find all distances of cells reachable from `start`.
# Returns an array padded to the right/bottom with MAX_SHORTCUT infinity cells.
@Time
def FindDistances(start):
    flat_walls = walls.ravel()
    flat_dists = [INF]*W*H
    stride = W
    start_index = start[0] * stride + start[1]
    todo = [start_index]
    flat_dists[start_index] = dist = 0
    while todo:
        dist += 1
        batch = todo
        todo = []
        for i in batch:
            for j in (i - stride, i - 1, i + 1, i + stride):
                if flat_dists[j] == INF and not flat_walls[j]:
                    flat_dists[j] = dist
                    todo.append(j)
    dists = np.array(flat_dists, dtype=np.int32).reshape(W, H)
    return np.pad(dists, ((0, MAX_SHORTCUT), (0, MAX_SHORTCUT)), constant_values=[INF])

# Find distances from start and to end.
dists1 = FindDistances(start)
dists2 = FindDistances(end)
min_dist = dists1[end]

@Time
def Solve(max_shortcut, min_saved=100):
    answer = 0
    for dr in range(-max_shortcut, max_shortcut + 1):
        for dc in range(-max_shortcut + abs(dr), max_shortcut - abs(dr) + 1):
            new_dists = np.roll(dists1, (-dr, -dc), axis=(0, 1)) + dists2
            answer += np.sum(new_dists <= min_dist - min_saved - abs(dr) - abs(dc))
    return answer

for max_shortcut in 2, MAX_SHORTCUT:
    print(Solve(max_shortcut))
