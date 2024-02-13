# This is a variant of fast.py that uses numpy to speed up input parsing,
# which is the slowest part. It uses regular Python integers for calculations
# to prevent integer overflow that would otherwise occur for very large inputs.
# This is not an issue with the official test data.

import numpy as np
import sys


def ReadInput():
  data = np.fromfile(sys.stdin, dtype=np.byte)
  newlines, = np.nonzero(data == ord('\n'))
  height = len(newlines)
  width = newlines[0]
  # Check all lines have the same length:
  assert all(newlines == np.arange(width, len(data), width + 1))
  matrix = np.delete(data, newlines) == ord('#')
  matrix.resize((height, width))
  return matrix


def SolveAxis(counts):
  total_dist = 0
  acc_dist   = 0
  acc_count  = 0
  # convert to int because numpy does not support bigints :/
  for n in map(int, counts):
    acc_dist   += acc_count*(1 if n else expand)
    acc_count  += n
    total_dist += acc_dist*n
  return total_dist


matrix = ReadInput()

for expand in 2, 1000000:
  print(sum(SolveAxis(matrix.sum(axis=axis)) for axis in range(2)))
