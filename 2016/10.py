import re
import sys

instructions = {}  # bot -> (lo_out, lo_dst, hi_out, hi_dst)
receives = []  # (val, dst)

for line in sys.stdin:
  m = re.match(r'bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)', line)
  if m:
    src, lo_kind, lo_dst, hi_kind, hi_dst = m.groups()
    instructions[int(src)] = lo_kind == 'output', int(lo_dst), hi_kind == 'output', int(hi_dst)
    continue
  m = re.match(r'value (\d+) goes to bot (\d+)', line)
  if m:
    val, dst = m.groups()
    receives.append((int(val), int(dst)))
    continue
  assert False

outputs = {}  # output -> value
have = {}  # bot -> value
for val, dst in receives:
  if dst not in have:
    have[dst] = val
  else:
    lo, hi = sorted((val, have[dst]))
    del have[dst]
    lo_out, lo_dst, hi_out, hi_dst = instructions[dst]
    if lo_out:
      assert lo_dst not in outputs
      outputs[lo_dst] = lo
    else:
      receives.append((lo, lo_dst))
    if hi_out:
      assert hi_dst not in outputs
      outputs[hi_dst] = hi
    else:
      receives.append((hi, hi_dst))
    if (lo, hi) == (17, 61):
      print(dst)  # Part 1

print(outputs[0]*outputs[1]*outputs[2])  # Part 2
