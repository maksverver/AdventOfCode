from lib05 import ParseStacks, ParseInstructions
import sys

def Solve(stacks, reverse):
  answer = ''
  for stack in range(len(stacks)):
    pos = 0
    for cnt, dst, src in reversed(instructions):
      assert src != dst
      if dst == stack:
        pos += cnt
      elif src == stack:
        if pos >= cnt:
          pos -= cnt
        else:
          stack = dst
          if reverse:
            pos = cnt - 1 - pos
    answer += stacks[stack][-pos - 1]
  return answer

part1, part2 = sys.stdin.read().split('\n\n')
stacks = ParseStacks(part1)
instructions = ParseInstructions(part2)

print(Solve(stacks, reverse=True))
print(Solve(stacks, reverse=False))
