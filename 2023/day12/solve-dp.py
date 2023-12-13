from functools import cache
import sys


def CountCombinations(s, runs):
  '''Returns the number of ways question marks in `s` can be filled in
     consistent with `runs`. `s` must have an extra '.' appended.'''

  # One way to view the problem is that we must construct a solution string by
  # concatenating several strings of the form "###." (where the number of hashes
  # in each string matches the values of `runs`); however we are also allowed to
  # insert extra filler characters ('.'). This interpretation requires that s
  # ends with a '.'.
  assert s[-1] == '.'

  # max_hashes[j] is the maximum number of hashes at the end of prefix s[:j].
  # For example, for s = "?#?.#", max_hashes = [0, 1, 2, 3, 0, 1] because we can
  # change the question marks to hashes, but not the fixed '.'.
  max_hashes = [0]*(len(s) + 1)
  for j, ch in enumerate(s):
    if ch != '.':
      max_hashes[j + 1] = max_hashes[j] + 1

  # dp[i][j] is the number of ways the prefix of s of length i (s[:i]) can be
  # filled to match the prefix of runs of length j (runs[:j]).
  dp = [[0]*(len(s) + 1) for _ in range(len(runs) + 1)]

  # First row: using no runs, we can fill any prefix that does not contain a
  # '#' in exactly 1 way: by setting all characters to '.'.
  dp[0][0] = 1
  for j, ch in enumerate(s):
    if ch == '#': break
    dp[0][j + 1] = 1

  # Subsequent rows: if a prefix ends with '#', there is no solution. Otherwise,
  # we either keep the last '.' as filler, or match a pattern '###.'
  for i, n in enumerate(runs):
    for j in range(len(s)):
      if s[j] != '#':
        dp[i + 1][j + 1] = dp[i + 1][j] + (n <= max_hashes[j] and dp[i][j - n])

  return dp[len(runs)][len(s)]


def Solve(records):
  return sum(CountCombinations(s + '.', runs) for s, runs in records)


def ParseLine(line):
  '''Parses a line like "???.### 1,1,3" into a pair ("???.###", [1, 1, 3]).'''
  a, b = line.split()
  return a, list(map(int, b.split(',')))


# Part 1
records1 = [ParseLine(line) for line in sys.stdin]
print(Solve(records1))

# Part 2
records2 = [('?'.join([s]*5), runs*5) for (s, runs) in records1]
print(Solve(records2))
