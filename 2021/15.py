from heapq import heappush, heappop
import sys

danger = [[int(c) for c in line.strip()] for line in sys.stdin]
H = len(danger)
W = len(danger[0])

def Search(danger, H, W):
    '''Dijkstra's algorithm'''
    todo = []
    min_dist = [[float('inf')]*W for _ in range(H)]

    def TryPush(d, r, c):
        if min_dist[r][c] > d:
            min_dist[r][c] = d
            heappush(todo, (d, r, c))

    TryPush(0, 0, 0)
    while todo:
        d, r, c = heappop(todo)
        if r == H - 1 and c == W - 1:
            return d
        if min_dist[r][c] != d:
            continue
        for rr, cc in [(r - 1, c), (r, c - 1), (r + 1, c), (r, c + 1)]:
            if 0 <= rr < H and 0 <= cc < W:
                TryPush(d + danger[rr][cc], rr, cc)

print(Search(danger, H, W))

danger2 = [[(danger[r % H][c % W] - 1 + (r // H) + (c // W)) % 9 + 1 for c in range(5*W)] for r in range(5*H)]

print(Search(danger2, 5*H, 5*W))
