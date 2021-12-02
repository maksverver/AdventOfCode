import sys

x = y1 = y2 = 0
for line in sys.stdin:
    direction, amount = line.split()
    amount = int(amount)
    if direction == 'forward':
        x += amount
        y2 += y1 * amount
    elif direction == 'up':
        y1 -= amount
    elif direction == 'down':
        y1 += amount
    else:
        assert False
print(x * y1)
print(x * y2)
