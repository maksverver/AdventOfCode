from collections import Counter
import sys

doubles = triples = 0
for line in sys.stdin:
    counts = Counter(line).values()
    doubles += 2 in counts
    triples += 3 in counts
print(doubles * triples)
