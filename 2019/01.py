import sys

masses = list(map(int, sys.stdin))

def BasicFuel(mass):
    return max(mass // 3 - 2, 0)

def TotalFuel(mass):
    total_fuel = 0
    fuel = BasicFuel(mass)
    while fuel > 0:
        total_fuel += fuel
        fuel = BasicFuel(fuel)
    return total_fuel

print(sum(map(BasicFuel, masses)))  # part 1
print(sum(map(TotalFuel, masses)))  # part 2
