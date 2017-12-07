import re
import sys

weight = {}
parent = {}
children = {}
for line in sys.stdin:
  m = re.match(r'(\w+) [(](\d+)[)]( -> (\w+(, \w+)*))?', line)
  name = m.group(1)
  weight[name] = int(m.group(2))
  if m.group(3):
    children[name] = m.group(4).split(', ')
    for child in children[name]:
      parent[child] = name
  else:
    children[name] = []

# Part one: find the root of the tree. It's the only node that has a weight
# but no parent.
root, = set(weight).difference(parent)
print(root)

total_weight = {}
def TotalWeight(name):
  global total_weight
  if name not in total_weight:
    total_weight[name] = weight[name] + sum(map(TotalWeight, children[name]))
  return total_weight[name]

def FindInbalance(name):
  my_children = children[name]
  if not my_children:
    return None
  for answer in map(FindInbalance, my_children):
    if answer:
      return answer
  child_weights = [TotalWeight(child) for child in my_children]
  if min(child_weights) == max(child_weights):
    return None
  # Find the index of the different value. This only works if we have at
  # least three childeren!
  i, = [i for i, w in enumerate(child_weights) if child_weights.count(w) == 1]
  weight_diff = child_weights[i] - child_weights[not i]
  return weight[my_children[i]] - weight_diff

# Part two: find the correct weight for the first inbalanced node.
print(FindInbalance(root))
