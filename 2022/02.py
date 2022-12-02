import sys

def MapDict(f, d):
  return {k: f(v) for k, v in d.items()}

def InvertDict(d):
  return {v: k for k, v in d.items()}

abc_to_rps = {'A': 'r', 'B': 'p', 'C': 's'}

xyz_to_rps = {'X': 'r', 'Y': 'p', 'Z': 's'}

xyz_to_payoff = {'X': 0, 'Y': 3, 'Z': 6}

move_value = {'r': 1, 'p': 2, 's': 3}

# opponent move -> my move -> my payoff
payoff = {
  'r': {'r': 3, 'p': 6, 's': 0},
  'p': {'r': 0, 'p': 3, 's': 6},
  's': {'r': 6, 'p': 0, 's': 3},
}

# opponent move -> my payoff -> my move
inv_payoff = MapDict(InvertDict, payoff)

total1 = total2 = 0
for line in sys.stdin:
  abc, xyz = line.split()
  opp_move   = abc_to_rps[abc]
  my_move    = xyz_to_rps[xyz]
  my_payoff  = xyz_to_payoff[xyz]
  total1 += payoff[opp_move][my_move] + move_value[my_move]
  total2 += my_payoff + move_value[inv_payoff[opp_move][my_payoff]]
print(total1)
print(total2)
