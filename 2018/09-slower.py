import re
import sys

class Node(object):
    def __init__(self, value, prev = None, next = None):
        self.value = value
        self.prev = self if prev is None else prev
        self.next = self if next is None else next

    def remove(self):
        self.next.prev = self.prev
        self.prev.next = self.next
        return self.next

    def insert(self, value):
        next = self.next
        self.next = next.prev = node = Node(value, self, next)
        return node

def Solve(players, marbles):
    scores = [0]*players
    current = Node(0)
    for i in range(1, marbles):
        if i%23 != 0:
            current = current.next
            current = current.insert(i)
        else:
            for _ in range(7):
                current = current.prev
            player = (i - 1)%players
            scores[player] += i + current.value
            current = current.remove()
    return max(scores)

pattern = r'(\d+) players; last marble is worth (\d+) points'
line = sys.stdin.readline()
players, last_marble = map(int, re.match(pattern, line).groups())
print(Solve(players, last_marble + 1))
print(Solve(players, last_marble*100 + 1))
