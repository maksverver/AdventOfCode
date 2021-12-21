def Memoize(f):
    memo = {}
    dummy = object()
    def g(*a):
        r = memo.get(a, dummy)
        if r is dummy:
            memo[a] = r = f(*a)
        return r
    return g
