import sys

def ValidPrefixLength(row):
    '''Returns the maximal prefix length that forms an increasing sequence
       with differences between elements between 1 and 3, inclusive.'''
    assert len(row) > 0
    i = 1
    while i < len(row) and 1 <= row[i] - row[i - 1] <= 3:
        i += 1
    return i

def CalcDeletionsForward(row):
    p = ValidPrefixLength(row)
    if p == len(row):
        # Entire row is valid.
        return 0

    # Logic: the row is valid up to the p'th element, which means that the
    # difference between row[p] and row[p + 1] is not between 1 and 3, and
    # therefore at least one of those two must be deleted. Try each option.
    if (ValidPrefixLength(row[:p - 1] + row[p    :]) == len(row) - 1 or
        ValidPrefixLength(row[:p    ] + row[p + 1:]) == len(row) - 1):
        # Error fixed by deleting 1 element.
        return 1

    # Two or more elements need to be deleted
    return 2

def CalcDeletions(row):
    return min(CalcDeletionsForward(row), CalcDeletionsForward(row[::-1]))

rows = [list(map(int, line.split())) for line in sys.stdin]
errors = [CalcDeletions(row) for row in rows]

print(sum(e < 1 for e in errors))
print(sum(e < 2 for e in errors))
