import sys

def ParseValidRanges(part):
    ranges = {}
    for line in part.split('\n'):
        key, values = line.split(': ')
        ranges[key] = []
        for part in values.split(' or '):
            lo, hi = map(int, part.split('-'))
            assert lo <= hi
            ranges[key].append((lo, hi))
    return ranges

def ParseYourTicket(part):
    first, second = part.split('\n')
    assert first == 'your ticket:'
    return list(map(int, second.split(',')))

def ParseNearbyTickets(part):
    first, *rest = part.split('\n')
    assert first == 'nearby tickets:'
    return [list(map(int, line.split(','))) for line in rest]

# Parse input
part1, part2, part3 = sys.stdin.read().strip().split('\n\n')
ranges = ParseValidRanges(part1)            # key -> [(lo, hi)]
my_ticket = ParseYourTicket(part2)          # [num]
nearby_tickets = ParseNearbyTickets(part3)  # [[num]]

# Part 1: filter out invalid tickets
valid_tickets = []
invalid_sum = 0
for nums in nearby_tickets:
    valid = True
    for num in nums:
        if not any(lo <= num <= hi for bounds in ranges.values() for lo, hi in bounds):
            valid = False
            invalid_sum += num
    if valid:
        valid_tickets.append(nums)
print(invalid_sum)


def CalculatePositions():
    # For each position, keep track of set of possible keys.
    possibilities = [set(ranges) for _ in my_ticket]  # [set([key])]

    # Pass 1: remove all keys that would make a ticket invalid.
    for nums in valid_tickets:
        for i, num in enumerate(nums):
            for key in list(possibilities[i]):
                if not any(lo <= num <= hi for lo, hi in ranges[key]):
                    possibilities[i].remove(key)

    # Pass 2: find uniquely-determined keys and remove it as a possibility
    # from oher positions (like naked singles in Sudoku). Repeat recursively.
    positions = {}  # key (str) -> position (int)
    def Check(i):
        assert len(possibilities[i]) > 0
        if len(possibilities[i]) > 1:
            return
        key, = possibilities[i]
        if key in positions:
            assert positions[key] == i
            return
        positions[key] = i
        for j, keys in enumerate(possibilities):
            if i != j and key in keys:
                keys.remove(key)
                Check(j)
    for i in range(len(possibilities)):
        Check(i)
    return positions

# Part 2: find which keys map to which field indices, then compute
# the product of the fields with key prefix "departure".
positions = CalculatePositions()
departure_product = 1
for key in ranges:
    if key.startswith('departure '):
        departure_product *= my_ticket[positions[key]]
print(departure_product)
