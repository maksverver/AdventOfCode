import sys

transitions = {}
for line in sys.stdin:
    if line.startswith('initial state: '):
        initial_state = line[len('initial state: '):].strip()
    elif '=>' in line:
        src, dst = (part.strip() for part in line.split('=>'))
        assert len(src) == 5
        assert len(dst) == 1
        assert '#' in src or dst == '.'
        assert src not in transitions
        transitions[src] = dst

def Next(left, state):
    state = '....' + state + '....'
    state = ''.join(transitions[state[i - 2:i + 3]] for i in range(2, len(state) - 2))
    left -= 2
    assert '#' in state
    left += state.find('#')
    state = state[state.find('#'):state.rfind('#') + 1]
    return left, state

def Solve(gens):
    left, state = 0, initial_state
    for gen in range(gens):
        next_left, next_state = Next(left, state)
        # Detect cycle: (current logic only finds cycles of length 1)
        if state == next_state:
            left += (next_left - left)*(gens - gen)
            break
        left, state = next_left, next_state
    return sum(i + left for i, x in enumerate(state) if x == '#')

# Part 1
print(Solve(20))

# Part 2
print(Solve(50 * 10**9))
