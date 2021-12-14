def Memoize(f):
    memo = {}
    def g(*a):
        r = memo.get(a)
        if not r:
            memo[a] = r = f(*a)
        return r
    return g
