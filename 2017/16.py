import sys

def Dance(input, moves):
    s = list(input)
    for move in moves:
        if move[0] == 's':
            n = int(move[1:])
            s = s[-n:] + s[:-n]
        elif move[0] == 'x':
            i, j = map(int, move[1:].split('/'))
            s[i], s[j] = s[j], s[i]
        elif move[0] == 'p':
            i, j = map(s.index, move[1:].split('/'))
            s[i], s[j] = s[j], s[i]
        else:
            assert False
    return ''.join(s)

def DetectCycleLength(input, moves):
    seen = set()
    while input not in seen:
        seen.add(input)
        input = Dance(input, moves)
    return len(seen)

# Part 1
initial = 'abcdefghijklmnop'
moves = sys.stdin.readline().strip().split(',')
print(Dance(initial, moves))

# Part 2
cycle_length = DetectCycleLength(initial, moves)
state = initial
for _ in range(1000000000%cycle_length):
    state = Dance(state, moves)
print(state)
