import sys

opening = '([{<'
closing = ')]}>'
values = [3, 57, 1197, 25137]

answer1 = 0
scores2 = []
for line in sys.stdin:
    stack = []
    for ch in line.strip():
        if ch in opening:
            i = opening.index(ch)
            stack.append(i)
        else:
            i = closing.index(ch)
            if stack.pop() != i:
                # corrupted string found
                answer1 += values[i]
                break
    else:
        if stack:
            # incomplete string found
            score = 0
            while stack:
                score *= 5
                score += stack.pop() + 1
            scores2.append(score)
answer2 = sorted(scores2)[len(scores2) // 2]

print(answer1)
print(answer2)
