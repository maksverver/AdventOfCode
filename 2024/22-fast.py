import sys

sums = [ 0] * 19**4
seen = [-1] * 19**4

answer1 = 0
for itr, x in enumerate(map(int, sys.stdin)):
    last_price = x % 10
    index = 0
    for i in range(2000):
        x = (x ^ (x <<  6)) & 0xffffff
        x = (x ^ (x >>  5)) & 0xffffff
        x = (x ^ (x << 11)) & 0xffffff
        price = x % 10
        delta = price - last_price
        last_price = price
        index = index % (19**3) * 19 + delta + 9
        if i >= 2 and seen[index] != itr:
            seen[index] = itr
            sums[index] += price
    answer1 += x
answer2 = max(sums)

print(answer1)
print(answer2)
