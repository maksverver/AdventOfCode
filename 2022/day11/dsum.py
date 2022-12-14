#!/usr/bin/env python

import sys

for line in sys.stdin:
  print(sum(map(int, line.strip())))
