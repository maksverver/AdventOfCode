import sys

def IsSafe1(row):
    return (all(1 <= row[i] - row[i - 1] <= 3 for i in range(1, len(row))) or
            all(1 <= row[i - 1] - row[i] <= 3 for i in range(1, len(row))))

def IsSafe2(row):
    return IsSafe1(row) or any(IsSafe1(row[:i] + row[i + 1:]) for i in range(len(row)))

rows = [list(map(int, line.split())) for line in sys.stdin]
print(sum(IsSafe1(row) for row in rows))
print(sum(IsSafe2(row) for row in rows))
