from functools import cache
import sys

# Increase maximum recursion level. It may also be necessary to do
# `ulimit -s unlimited` on the shell, otherwise Python may segfault.
sys.setrecursionlimit(10000)


# Automatic memoization
@cache
def fib(n):
  if n == 0: return 0
  if n == 1: return 1
  return fib(n - 1) + fib(n - 2)


if __name__ == '__main__':
  assert fib(100) == 354224848179261915075
