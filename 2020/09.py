import sys

nums = [int(line) for line in sys.stdin]

def Part1():
    past = set()
    for i, v in enumerate(nums):
        if i >= 25:
            for w in past:
                if v - w in past:
                    break
            else:
                return v
            past.remove(nums[i - 25])
        assert v not in past
        past.add(v)

def Part2(goal):
    i = 0
    total = 0
    for j, v in enumerate(nums):
        total += v
        while total > goal and i + 1 < j:
            total -= nums[i]
            i += 1
        if total == goal:
            sub = nums[i:j + 1]
            return min(sub) + max(sub)

a = Part1()
print(a)
print(Part2(a))

