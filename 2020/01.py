import sys

# Note: this assumes all numbers are distinct!
nums = set(int(line) for line in sys.stdin)

# Part 1
for a in nums:
    b = 2020 - a
    if a < b and b in nums:
        print(a * b)

# Part 2
for a in nums:
    for b in nums:
        c = 2020 - a - b
        if a < b < c and c in nums:
            print(a * b * c)
