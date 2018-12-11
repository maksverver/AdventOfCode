import sys

grid_size = 300
serial_no = int(sys.stdin.readline())

def GetFuel(x, y):
    rack_id = x + 10
    power_level = (rack_id * y + serial_no)*rack_id
    return (power_level // 100 % 10) - 5

# fuel[y][x] contains fuel in rectangle from (0,0) to (x,y), inclusive.
fuel = [[0]*(grid_size + 1) for _ in range(grid_size + 1)]
for y in range(1, grid_size + 1):
    for x in range(1, grid_size + 1):
        fuel[y][x] = GetFuel(x, y) + fuel[y - 1][x] + fuel[y][x - 1] - fuel[y - 1][x - 1]

best_coords = None
best_value = None
for size in range(1, grid_size + 1):
    for x in range(size, grid_size + 1):
        for y in range(size, grid_size + 1):
            value = fuel[y][x] - fuel[y - size][x] - fuel[y][x - size] + fuel[y - size][x - size]
            if best_value is None or value > best_value:
                best_value = value
                best_coords = (x - size + 1, y - size + 1, size)

print('{},{},{}'.format(*best_coords))
