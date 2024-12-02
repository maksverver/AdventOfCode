from random import shuffle, randint
import sys

ROWS=100
MAX_COLS=10000

def IsSafe1(row):
    return (all(1 <= row[i] - row[i - 1] <= 3 for i in range(1, len(row))) or
            all(1 <= row[i - 1] - row[i] <= 3 for i in range(1, len(row))))

def IsSafe2(row):
    return IsSafe1(row) or any(IsSafe1(row[:i] + row[i + 1:]) for i in range(len(row)))

def RandomValue():
    return randint(1, 1000)

def IntroduceSingleError(row):
    i = randint(0, len(row) - 1)
    return row[:i] + [RandomValue()] + row[i:-1]

def IntroduceShiftError(row):
    i = randint(2, len(row) - 2)
    delta = randint(3, 10)
    if delta > 5:
        delta = -delta
    return row[:i] + [v + delta for v in row[i:]]

error_freq = [0, 0, 0]

def GenRow(length):
    row = [RandomValue()]
    while len(row) < length: row.append(row[-1] + randint(1, 3))

    errors = randint(0, min(2, length - 1))
    error_freq[errors] += 1
    if errors == 0:
        # Keep row unmodified
        pass
    elif errors == 1:
        # Add a single erroneous error which can be deleted to make the row valid
        row = IntroduceSingleError(row)
    elif errors == 2:
        # Introduce two or more errors
        t = randint(0, 10)
        if t == 0:
            shuffle(row)
        elif t < 3:
            row = IntroduceShiftError(row)
        else:
            row = IntroduceSingleError(row)
            row = IntroduceSingleError(row)

        # if IsSafe2(row):
        #     print(row, file=sys.stderr)

    if randint(0, 1) == 1:
        row.reverse()

    return row

lengths = ([1] + [randint(MAX_COLS//2, MAX_COLS) for _ in range(ROWS - 1)])
shuffle(lengths)

rows = [GenRow(length) for length in lengths]
for row in rows:
    print(*row)

print(error_freq, file=sys.stderr)
