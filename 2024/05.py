from functools import cmp_to_key
import sys

order = dict()

sort_key = cmp_to_key(lambda p, q: order.get((p, q), 0))

for line in sys.stdin:
    line = line.strip()
    if not line:
        break
    a, b = map(int, line.split('|'))
    assert a != b and (a, b) not in order
    order[a, b] = -1
    order[b, a] = +1

answer1 = 0
answer2 = 0
for line in sys.stdin:
    pages = list(map(int, line.strip().split(',')))
    assert len(pages) % 2 == 1
    sorted_pages = sorted(pages, key=sort_key)
    middle = sorted_pages[len(pages) // 2]
    if pages == sorted_pages:
        answer1 += middle
    else:
        answer2 += middle
print(answer1)
print(answer2)
