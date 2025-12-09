from hashlib import md5
import sys

salt = sys.stdin.readline().strip()

def Memoize(f):
  memo = []
  def wrapper(i):
    while len(memo) <= i:
      memo.append(f(len(memo)))
    return memo[i]
  return wrapper

@Memoize
def GetHash(i):
  return md5(bytes(salt + str(i), 'ascii')).hexdigest()

def GetTriple(i):
  hash = GetHash(i)
  for j in range(len(hash) - 2):
    if hash[j] == hash[j + 1] == hash[j + 2]:
      return hash[j]

@Memoize
def GetQuintuples(i):
  quintuples = []
  hash = GetHash(i)
  for j in range(len(hash) - 4):
    if hash[j] == hash[j + 1] == hash[j + 2] == hash[j + 3] == hash[j + 4]:
      quintuples.append(hash[j])
  return quintuples

def Keys():
  i = 0
  while True:
    c = GetTriple(i)
    if c is not None:
      for j in range(i + 1, i + 1001):
        for d in GetQuintuples(j):
          if c == d:
            yield i
    i += 1

keygen = Keys()
for _ in range(64):
  key = next(keygen)
print(key)
