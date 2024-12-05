# Fixed version of 05-incorrect.py.
#
# See small-example.txt for a case where it matters.

from functools import cmp_to_key
import sys

initial_order = dict()

for line in sys.stdin:
    line = line.strip()
    if not line:
        break
    a, b = map(int, line.split('|'))
    assert a != b and (a, b) not in initial_order
    initial_order[a, b] = -1
    initial_order[b, a] = +1

a = b = 0  # for debugging, track how many values contribute to answer1/answer2
answer1 = 0
answer2 = 0
for line in sys.stdin:
    pages = list(map(int, line.strip().split(',')))
    assert len(pages) == len(set(pages))
    assert len(pages) % 2 == 1

    # Compute transitive closure of the given pages. This is essentially
    # Warshall's algorithm, which runs in O(|pages|^3) obviously.
    order = dict(initial_order)
    for q in pages:
        for p in pages:
            for r in pages:
                if p != q and p != r and q != r:
                    if order.get((p, q), 0) > 0 and order.get((q, r), 0) > 0:
                        if (p, r) in order:
                            assert order[p, r] == 1
                        else:
                            assert (r, p) not in order
                            order[p, r] = +1
                            order[r, p] = -1

    # Now we should be able to sort, if the problem is well-defined.
    sort_key = cmp_to_key(lambda p, q: order.get((p, q), 0))
    sorted_pages = sorted(pages, key=sort_key)
    assert sorted_pages == sorted(sorted_pages, key=sort_key)
    middle = sorted_pages[len(pages) // 2]
    if pages == sorted_pages:
        a += 1
        answer1 += middle
    else:
        b += 1
        answer2 += middle
print(answer1)
print(answer2)
print(a,b)
