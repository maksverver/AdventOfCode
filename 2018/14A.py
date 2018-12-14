import sys

offset = int(sys.stdin.readline())
scores = [3, 7]
i = 0
j = 1
while len(scores) < offset + 10:
    x = scores[i] + scores[j]
    if x < 10:
        scores.append(x)
    else:
        scores.append(x//10)
        scores.append(x%10)
    i = (i + 1 + scores[i])%len(scores)
    j = (j + 1 + scores[j])%len(scores)
print(''.join(map(str, scores[offset:offset + 10])))
