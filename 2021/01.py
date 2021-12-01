import sys
from collections import deque

class Solver:
    def __init__(self, window_size):
        self.window_size = window_size
        self.values = deque()
        self.answer = 0

    def Add(self, value):
        self.values.append(value)
        if len(self.values) > self.window_size:
            self.answer += value > self.values.popleft()

solver1 = Solver(1)
solver2 = Solver(3)
for value in map(int, sys.stdin):
    solver1.Add(value)
    solver2.Add(value)
print(solver1.answer)
print(solver2.answer)
