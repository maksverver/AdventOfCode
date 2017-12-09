import sys

def Parse(line):
    depth = 0
    in_garbage = False
    escape = False
    score = 0
    garbage_chars = 0
    for ch in line:
        if escape:
            escape = False
        elif in_garbage:
            if ch == '!':
                escape = True
            elif ch == '>':
                in_garbage = False
            else:
                garbage_chars += 1
        else:
            if ch == '<':
                in_garbage = True
            elif ch == '{':
                depth += 1
                score += depth
            elif ch == '}':
                depth -= 1
            else:
                assert depth > 0
    return score, garbage_chars

for answer in Parse(sys.stdin.readline().strip()):
    print(answer)
