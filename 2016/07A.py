import sys

def CountAbbas(s):
  return sum(s[i] == s[i + 3] != s[i + 1] == s[i + 2]
             for i in range(len(s) - 3))

def SupportsTls(line):
  parts = line.replace('[', ' ').replace(']', ' ').split()
  abbas = map(CountAbbas, parts)
  return any(abbas[0::2]) and not any(abbas[1::2])

print len(filter(SupportsTls, sys.stdin))
