# Advent of Code 2023 Day 20: Pulse Propagation
# https://adventofcode.com/2023/day/20

from collections import deque
from math import lcm
import sys

class Module:
  def __init__(self, name):
    self.name = name
    self.dests = []
    self.sources = []

  def AddSource(self, source):
    self.sources.append(source)

  def AddDest(self, dest):
    self.dests.append(dest)

  def __repr__(self):
    return self.name


class Broadcaster(Module):
  def __init__(self, name):
    super().__init__(name)

  def HandleSignal(self, source, input, send):
    for dest in self.dests:
      send(dest, input)


class FlipFlop(Module):
  def __init__(self, name):
    super().__init__(name)
    self.value = 0

  def HandleSignal(self, source, input, send):
    if input == 0:
      self.value ^= 1
      for dest in self.dests:
        send(dest, self.value)

  def __repr__(self):
    return '%' + self.name


class Conjunction(Module):
  def __init__(self, name):
    super().__init__(name)
    self.values = None
    self.last = {}
    self.values = []

  def AddSource(self, source):
    self.values.append(0)
    super().AddSource(source)

  def HandleSignal(self, source, input, send):
    self.values[self.sources.index(source)] = input

    output = 1 - all(self.values)
    for dest in self.dests:
      send(dest, output)

  def __repr__(self):
    return '&' + self.name


class Dummy(Module):
  def __init__(self, name):
    super().__init__(name)

  def HandleSignal(self, source, input, send):
    pass


# Parses a line into a module definition triple: (name, type, [destination names]).
def ParseModuleDef(line):
  src, dests = line.strip().split(' -> ')
  dests = dests.split(', ')
  if src == 'broadcaster':
    type = Broadcaster
    name = src
  else:
    type = [FlipFlop, Conjunction]['%&'.index(src[0])]
    name = src[1:]
  return (name, type, dests)


class Orchestrator:
  def __init__(self, module_defs, listener):
    self.listener = listener

    # Create modules
    self.modules = {'rx': Dummy('rx')}
    for name, type, dests in module_defs:
      assert name not in self.modules
      self.modules[name] = type(name)

    # Connect modules
    for source_name, _, dest_names in module_defs:
      source = self.modules[source_name]
      for dest_name in dest_names:
        dest = self.modules[dest_name]
        source.AddDest(dest)
        dest.AddSource(source)

  def Send(self, source, dest, v):
    self.todo.append((source, dest, v))

  def PressButton(self):
    todo = deque()
    dest = None
    send = lambda dest2, signal2: todo.append((dest, dest2, signal2))
    send(self.modules['broadcaster'], 0)
    while todo:
      source, dest, signal = todo.popleft()
      dest.HandleSignal(source, signal, send)
      self.listener(source, dest, signal)

# Solve part 1 by simulation: simply press the button 1000 times and count
# how often each signal occurs.
def Part1():
  signal_counts = [0, 0]
  def OnSend(source, dest, signal):
    signal_counts[signal] += 1

  orchestrator = Orchestrator(module_defs, OnSend)
  for _ in range(1000):
    orchestrator.PressButton()

  lo, hi = signal_counts
  return lo * hi


# Solve part 2, using some assumptions about how the input is constructed and
# how it behaves: the `rx` module has a single conjunction module as its source,
# which itself has four sources. Each of those sources sends a 1 periodically
# with offset 0. Therefore, we can calculate the first time all sources send a
# 1 during the same period as the least common multiple (LCM) of the invididual
# periods, once we've determined them.
def Part2():
  def OnSend(source, dest, signal):
    if dest == conj and signal:
      times_by_source[source].append(time)

  orchestrator = Orchestrator(module_defs, OnSend)

  conj, = orchestrator.modules['rx'].sources
  assert isinstance(conj, Conjunction)
  times_by_source = dict((source, []) for source in conj.sources)

  # Simulate until we have at least two times per source.
  time = 0
  while any(len(times) < 2 for times in times_by_source.values()):
    time += 1
    orchestrator.PressButton()

  # Verify that times are periodic, as far as we can tell from the limited data
  # available:
  for times in times_by_source.values():
    for i, t in enumerate(times, 1):
      assert t == i*times[0]

  # Calculate the combined period as the LCM of the individual periods.
  return lcm(*[times[0] for times in times_by_source.values()])


module_defs = [ParseModuleDef(line) for line in sys.stdin]

print(Part1())
print(Part2())
