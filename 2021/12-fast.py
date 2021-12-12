from collections import defaultdict
import sys

def Main():
    idx = defaultdict(lambda: len(idx))
    adj = defaultdict(set)
    for line in sys.stdin:
        v, w = map(idx.__getitem__, line.strip().split('-'))
        adj[v].add(w)
        adj[w].add(v)

    large_mask = sum((1 << i) for (s, i) in idx.items() if s.isupper())

    start = idx['start']
    end   = idx['end']

    def Solve(allow_extra_visit):
        # This version uses recursion with memoization to avoid duplicate work.
        memo = {}
        def Search(v, allow_extra_visit, blocked_mask):
            if v == end:
                return 1
            key = (blocked_mask, v, allow_extra_visit)
            res = memo.get(key)
            if res is not None:
                return res
            res = 0
            for w in adj[v]:
                if (1 << w) & large_mask:
                    # Revisit large cave
                    res += Search(w, allow_extra_visit, blocked_mask)
                elif ((1 << w) & blocked_mask) == 0:
                    # Visit a small cave for the first time
                    res += Search(w, allow_extra_visit, blocked_mask | (1 << w))
                elif allow_extra_visit and w != start:
                    # Revisit a small cave if we haven't done so before.
                    res += Search(w, False, blocked_mask)
            memo[key] = res
            return res

        return Search(start, allow_extra_visit, 1 << start)

    print(Solve(False))  # part 1
    print(Solve(True))   # part 2

Main()
