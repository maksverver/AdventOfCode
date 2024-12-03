import re
import sys

PATTERN = re.compile(r"mul[(]([0-9]{1,3}),([0-9]{1,3})[)]|(do)[(][)]|(don't)[(][)]")

answer1 = 0
answer2 = 0
enabled = True
for m in PATTERN.finditer(sys.stdin.read()):
    x, y, do, dont = m.groups()
    if do:
        enabled = True
    elif dont:
        enabled = False
    else:
        product = int(x) * int(y)
        answer1 += product
        answer2 += product * enabled
print(answer1)
print(answer2)
