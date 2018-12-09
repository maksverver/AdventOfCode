import re
import sys

def Solve(players, marbles):
    scores = [0]*players
    prev = [0]*marbles
    next = [0]*marbles
    i = 0
    for j in range(1, marbles):
        if j%23 != 0:
            i = next[i]
            k = next[i]
            next[j] = k
            prev[k] = j
        else:
            for _ in range(7):
                i = prev[i]
            player = (j - 1)%players
            scores[player] += i + j
            j = next[i]
            i = prev[i]
        next[i] = j
        prev[j] = i
        i = j
    return max(scores)

pattern = r'(\d+) players; last marble is worth (\d+) points'
line = sys.stdin.readline()
players, last_marble = map(int, re.match(pattern, line).groups())
print(Solve(players, last_marble + 1))
print(Solve(players, last_marble*100 + 1))
