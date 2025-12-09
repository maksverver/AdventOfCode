import sys

def CountAbbas(s):
  return sum(s[i] == s[i + 3] != s[i + 1] == s[i + 2]
             for i in range(len(s) - 3))

def SupportsTls(addr):
  parts = addr.replace('[', ']').split(']')
  abbas = list(map(CountAbbas, parts))
  return any(abbas[0::2]) and not any(abbas[1::2])

addrs = [line.strip() for line in sys.stdin]
print(sum(map(SupportsTls, addrs)))
