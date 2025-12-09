from collections import Counter
import sys

print(''.join(Counter(line).most_common()[-1][0] for line in zip(*sys.stdin)))
