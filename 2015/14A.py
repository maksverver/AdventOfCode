from lib14 import Raindeer
import sys

print(max(Raindeer(line).position_at(2503) for line in sys.stdin))
