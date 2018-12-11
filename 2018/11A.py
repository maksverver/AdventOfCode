import sys

grid_size = 300
serial_no = int(sys.stdin.readline())

def GetFuel(x, y):
    rack_id = x + 10
    power_level = (rack_id * y + serial_no)*rack_id
    return (power_level // 100 % 10) - 5

best_coords = None
best_value = None
for x in range(grid_size - 2):
    for y in range(grid_size - 2):
        value = sum(GetFuel(xx, yy) for xx in range(x, x + 3) for yy in range(y, y + 3))
        if best_value is None or value > best_value:
            best_value = value
            best_coords = (x, y)

print('{},{}'.format(*best_coords))
