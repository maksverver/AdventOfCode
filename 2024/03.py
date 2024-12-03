import re
import sys

PATTERN = re.compile(r"mul[(](\d{1,3}),(\d{1,3})[)]|(do)[(][)]|(don't)[(][)]")

answer1 = 0
answer2 = 0
enabled = True
for x, y, do, dont in PATTERN.findall(sys.stdin.read()):
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
