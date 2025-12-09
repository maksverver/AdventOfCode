import re
import sys

def IsGoal(floors):
  return all(len(items) == 0 for items in floors[:-1])

def Successors(old_level, floors):
  def IsValid(items):
    generators = set(elem for elem, kind in items if kind == 'generator')
    microchips = set(elem for elem, kind in items if kind == 'microchip')
    return not (generators and microchips.difference(generators))

  def Generate(taken, new_level):
    new_floors = list(floors)
    new_floors[old_level] = floors[old_level].difference(taken)
    if IsValid(new_floors[old_level]):
      new_floors[new_level] = floors[new_level].union(taken)
      if IsValid(new_floors[new_level]):
        results.append((new_level, new_floors))

  def Take(taken):
    if old_level > 0:
      Generate(taken, old_level - 1)
    if old_level < len(floors) - 1:
      Generate(taken, old_level + 1)

  results = []
  for item1 in floors[old_level]:
    Take(set([item1]))
    for item2 in floors[old_level]:
      if item2 != item1:
        Take(set([item1, item2]))
  return results

def Freeze(floors):
  return tuple(tuple(sorted(items)) for items in floors)

def Thaw(floors):
  return [set(items) for items in floors]

def Solve(initial_floors):
  seen = set()
  queue = []

  def Add(steps, level, floors):
    state = level, Freeze(floors)
    if state not in seen:
      seen.add(state)
      queue.append((steps,) + state)

  Add(0, 0, initial_floors)
  for steps, level, floors in queue:
    floors = Thaw(floors)
    if IsGoal(floors):
      return steps
    for new_level, new_floors in Successors(level, floors):
      Add(steps + 1, new_level, new_floors)

pattern = re.compile(r'a (\w*)(?:-compatible)? (generator|microchip)')
floors = [set(match.groups() for match in pattern.finditer(line)) for line in sys.stdin]

# Part 1
print(Solve(floors))

# Part 2 (this is pretty slow... :-/)
floors[0].add(('elerium', 'generator'))
floors[0].add(('elerium', 'microchip'))
floors[0].add(('dilithium', 'generator'))
floors[0].add(('dilithium', 'microchip'))
print(Solve(floors))
