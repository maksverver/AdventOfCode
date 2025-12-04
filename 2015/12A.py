import re
import sys

print(sum(map(int, re.findall('-?[0-9]+', sys.stdin.read()))))
