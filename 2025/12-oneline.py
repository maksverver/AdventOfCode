import re

print(sum(h*w > 8*sum(counts) for h, w, *counts in
        (map(int, re.findall(r'\d+', line)) for line in open(0) if 'x' in line)))
