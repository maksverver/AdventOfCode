import sys

input_nums = [int(line) for line in sys.stdin]

last = max(input_nums) + 3
nums = [0] + sorted(input_nums) + [last]

# Part 1
diffs = [0, 0, 0, 0]
for i in range(1, len(nums)):
    diffs[nums[i] - nums[i - 1]] += 1
assert diffs[0] == 0 and diffs[2] == 0
print(diffs[1] * diffs[3])

# Part 2
counts = [1] + [0]*last
for v in nums[1:]:
    for u in range(max(0, v - 3), v):
        counts[v] += counts[u]
print(counts[last])
