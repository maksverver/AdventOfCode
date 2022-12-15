#!/usr/bin/env python3

import sys

for line in sys.stdin:
  print(int(line) % 31337)
