from random import shuffle, randint
import sys

def Interleave(a, b):
    buf = [0]*len(a) + [1]*len(b)
    shuffle(buf)
    i = j = 0
    res = []
    for x in buf:
        if x == 0:
            res.append(a[i])
            i += 1
        else:
            res.append(b[j])
            j += 1
    assert i == len(a)
    assert j == len(b)
    return res


def GenMostlyOkCase(length, start_val, errors):
    row = [start_val]
    while len(row) < length - errors:
        row.append(row[-1] + randint(1, 3))
    errors = [randint(row[0], row[-1]) for _ in range(errors)]
    return Interleave(row, errors)

def GenRandomCase(len, min_val, max_val):
    return [randint(min_val, max_val) for _ in range(len)]

ROWS=100
MAX_COLS=10000

rows = [
    GenRandomCase(1, 42, 42),
    GenRandomCase(10000, 1, 9999),
    GenRandomCase(200000, 1, 200000),
    GenMostlyOkCase(200000, randint(1, 1000), 100000),
    100*[7],
]

row = list(range(1, 10001))
shuffle(row)
rows.append(row)

for i in range(5):
    rows.append(GenRandomCase(1000, 1, 10))
    rows.append(GenRandomCase(1000, 1, 100))
    rows.append(GenRandomCase(1000, 1, 1000))
    rows.append(GenRandomCase(1000, 1, 10000))
    rows.append(GenRandomCase(1000, 1, 999999))
    rows.append(GenMostlyOkCase(1000, randint(1, 100), 1))
    rows.append(GenMostlyOkCase(1000, randint(1, 100), 10))
    rows.append(GenMostlyOkCase(1000, randint(1, 100), 100))
    rows.append(GenMostlyOkCase(1000, randint(1, 100), 500))

shuffle(rows)

for row in rows:
    print(*row)
