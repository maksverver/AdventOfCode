import re
import sys

claims = []
for line in sys.stdin:
    id, x1, y1, w, h = map(int, re.match(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', line).groups())
    claims.append((id, x1, y1, x1 + w, y1 + h))

for a_id, a_x1, a_y1, a_x2, a_y2 in claims:
    if all(a_x2 <= b_x1 or a_x1 >= b_x2 or a_y2 <= b_y1 or a_y1 >= b_y2
            for b_id, b_x1, b_y1, b_x2, b_y2 in claims if a_id != b_id):
        print(a_id)
