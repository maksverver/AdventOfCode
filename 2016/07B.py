import sys

def GetAbas(s):
  for i in range(len(s) - 2):
    if s[i] == s[i + 2] != s[i + 1]:
      yield s[i + 1] + s[i]

def GetBabs(s):
  return (''.join(reversed(aba)) for aba in GetAbas(s))

def SupportsSsl(line):
  parts = line.replace('[', ']').split(']')
  abas = set(aba for part in parts[0::2] for aba in GetAbas(part))
  babs = set(bab for part in parts[1::2] for bab in GetBabs(part))
  return bool(abas.intersection(babs))

addrs = [line.strip() for line in sys.stdin]
print len(filter(SupportsSsl, addrs))
