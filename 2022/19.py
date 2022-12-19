from collections import defaultdict
from math import inf
import re
import sys

resources = ['ore', 'clay', 'obsidian', 'geode']
R = len(resources)

blueprint_pattern = re.compile('^Blueprint (\d+): (.+)\.\n$')
robot_pattern = re.compile('^Each (\w+) robot costs ((\d+) (\w+)( and (\d+) (\w+))?)$');

def ParseBlueprint(line):
  costs = [[0]*R for _ in range(R)]
  id, robots = blueprint_pattern.match(line).groups()
  id = int(id)
  for robot in robots.split('. '):
    dst, dst_costs, *rest = robot_pattern.match(robot).groups()
    for dst_cost in dst_costs.split(' and '):
      qty, src = dst_cost.split(' ')
      costs[resources.index(dst)][resources.index(src)] = int(qty)
  return id, costs

def Add(stock, robots):
  return [a + b for a, b in zip(stock, robots)]

def Sub(stock, cost):
  return [a - b for a, b in zip(stock, cost)]

def Inc(robots, i):
  return [n + (i == j) for j, n in enumerate(robots)]

# Given a list of iterables (with all equal number of elements),
# returns a copy with duplicates and suboptimal elements removed.
#
# A vector v is inferior to w if for all i, v[i] <= w[i], and for some i,
# v[i] < w[i]. This function removes all elements that are inferior to some
# other vector in the input.
def RemoveSuboptimal(vectors):
  vectors = sorted(vectors)
  last = vectors.pop()
  keep = [last]
  while vectors:
    vector = vectors.pop()
    for x, y in zip(last, vector):
      if x < y:
        keep.append(vector)
        last = vector
        break
  return keep

def Maximize(costs, time_left):
  # Precalculate the maximum number of robots we need of each type.
  #
  # These are limited by the costs to build robots. For example, if no robot
  # costs more than 10 ore, then since we can only build one robot per minute,
  # we don't need more than 10 ore-gathering robots.
  max_robots = [max(costs[i][j] for i in range(R)) for j in range(R)]
  max_robots[-1] = inf

  # List of possible things we can have. Each element is a pair of robots
  # and stock. Initially, we can only 1 ore-gathering robot and no stock.
  have = [([1] + [0]*(R - 1), [0]*R)]

  while time_left > 0:
    next_have = []
    for robots, stock in have:
      new_stock = Add(stock, robots)
      next_have.append((robots, new_stock))
      for i, cost in enumerate(costs):
        # Consider buying another robot of type i
        if robots[i] < max_robots[i] and all(c <= s for c, s in zip(cost, stock)):
          next_have.append((Inc(robots, i), Sub(new_stock, cost)))

    time_left -= 1

    # Remove suboptimal solutions.
    vectors = []
    for robots, stock in next_have:
      # Limit stock to however many resources we still have time to use.
      limited_stock = [min(s, m * time_left) for s, m in zip(stock, max_robots)]
      vectors.append(robots + limited_stock)
    vectors = RemoveSuboptimal(vectors)
    have = [(vector[:R], vector[R:]) for vector in vectors]

  return max(stock[-1] for robots, stock in have)

blueprints = [ParseBlueprint(line) for line in sys.stdin]

def SolvePart1():
  return sum(id * Maximize(costs, 24) for id, costs in blueprints)

def SolvePart2():
  res = 1
  for id, costs in blueprints[:3]:
    res *= Maximize(costs, 32)
  return res

print(SolvePart1())
print(SolvePart2())
