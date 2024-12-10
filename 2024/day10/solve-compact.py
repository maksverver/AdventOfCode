grid = {r+c*1j: int(ch) for r, line in enumerate(open(0)) for c, ch in enumerate(line.strip())}

def search(*todo):
    for h in range(9):
        todo = container(v+n for v in todo for n in (1, -1, 1j, -1j) if grid.get(v+n, 0) == h+1)
    return todo

for container in set, list:
    print(sum(len(search(v)) for v in grid if grid[v] == 0))
