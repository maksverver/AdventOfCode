def ParseStacks(text):
  """Parses the first half of the input into a list of stacks, where each stack
  is a list of boxes."""
  head, *tail = reversed(text.splitlines())
  stacks = []
  for col, label in enumerate(head):
    if label.isspace():
      continue
    #assert label == str(len(stacks) + 1)
    stack = []
    for line in tail:
      box = line[col]
      if box.isspace():
        break
      stack.append(box)
    stacks.append(stack)
  return stacks


def ParseInstructions(text):
  """Parses the second half of the input into a list of instructions, where each
  instruction is a triple (count, src, dst), where `count` is the number of boxes
  to move, and `src` and `dst`` are 0-based stack indexes."""
  return [ParseInstruction(line) for line in text.splitlines()]

def ParseInstruction(line):
  move, count, from_, src, to_, dst = line.split()
  assert move == 'move' and from_ == 'from' and to_ == 'to'
  return int(count), int(src) - 1, int(dst) - 1


def CalculateLocations(stacks, instructions, reverse):
  """Calculates the locations of the boxes used in the solution.

    - `stacks` is a list of stacks as returned by ParseBoxes()
    - `instructions is a list of instructions as returned by ParseInstructions()
    - `reverse` is a Boolean that indicates whether to reverse boxes as they are
       move (True for part 1, False for part 2)
  """

  # First, calculate heights at the end of the instructions:
  heights = [len(s) for s in stacks]
  for n, i, j in instructions:
    assert n <= heights[i]
    heights[i] -= n
    heights[j] += n

  # Record the locations of boxes on top of each stack, which are the ones used
  # to generate the answer.
  #
  # For each stack, contains a list of (pos, label) pairs where "pos" is the
  # position in the stack (counting from the bottom as 0), and "label" is the
  # index of the box in the solution. Pairs are kept sorted.
  locations = [[(h - 1, i)] for i, h in enumerate(heights)]

  # Now undo instructions, keeping track of the final boxes
  # Undo instructions
  for n, j, i in reversed(instructions):
    assert i != j
    src_pos = heights[i] - n
    assert src_pos >= 0

    k = 0  # how many elements to take from locations[i]
    while k < len(locations[i]) and locations[i][-k - 1][0] >= src_pos: k += 1
    if k > 0:
      moved = locations[i][-k:]
      locations[i] = locations[i][:-k]
      if not reverse:
        for (pos, label) in moved:
          new_pos = pos - src_pos + heights[j]
          locations[j].append((new_pos, label))
      else:
        for (pos, label) in reversed(moved):
          new_pos = n - 1 - (pos - src_pos) + heights[j]
          locations[j].append((new_pos, label))
      #assert(locations[j] == sorted(locations[j]))
    heights[i] -= n
    heights[j] += n

  return locations


def WriteTestInput(stacks, instructions):
  """Outputs a test data file to stdout. Used by the generators."""
  # Print stack boxes
  for r in range(max(map(len, stacks)) - 1, -1, -1):
    line = ''
    for s in stacks:
      if r < len(s):
        line += '[' + s[r] + '] '
      else:
        line += '    '
    print(line)

  # Print stack labels
  if len(stacks) < 10:
    print(''.join(' ' + str(col + 1) + '  ' for col in range(len(stacks))))
  else:
    print(' 0  ' * len(stacks))

  # Blank separator
  print()

  # Print instructions
  for (n, i, j) in instructions:
    print('move', n, 'from', i + 1, 'to', j + 1)
