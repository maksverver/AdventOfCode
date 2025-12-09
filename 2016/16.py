import sys

pattern = sys.stdin.readline().strip()

def Memoize(f):
  memo = {}
  def Wrapper(*args):
    try:
      return memo[args]
    except KeyError:
      result = f(*args)
      memo[args] = result
      return result
  return Wrapper

def Solve(pattern, N):
  lengths = [len(pattern)]
  while lengths[-1] < N:
    lengths.append(lengths[-1]*2 + 1)

  @Memoize
  def GetBitSum(i, j, d):
    assert 0 <= i < j <= lengths[d]
    if d == 0:
      if j - i == 1:
        return int(pattern[i])
      else:
        k = (i + j)//2
        return GetBitSum(i, k, 0) ^ GetBitSum(k, j, 0)
    else:
      result = 0
      if i < lengths[d - 1]:
        result ^= GetBitSum(i, min(j, lengths[d - 1]), d - 1)
      if j > lengths[d - 1] + 1:
        ii = lengths[d] - j
        jj = min(lengths[d] - i, lengths[d - 1])
        result ^= GetBitSum(ii, jj, d - 1) ^ ((jj - ii) & 1)
      return result

  chunk_size = N & ~(N - 1)
  return ''.join(str(GetBitSum(i, i + chunk_size, len(lengths) - 1) ^ 1)
      for i in range(0, N, chunk_size))

print(Solve(pattern, 272))
print(Solve(pattern, 35651584))
