from collections import defaultdict
import sys

def ParseProduct(word):
    '''Converts "42 FOO" to a (product, quantity) pair like ("FOO", 42).'''
    quantity, product = word.split()
    quantity = int(quantity)
    assert quantity > 0
    return (product, quantity)

def ParseLine(line):
    inputs, output = line.split(' => ')
    return (ParseProduct(output), tuple(map(ParseProduct, inputs.split(', '))))

def ParseLines(lines):
    '''Returns a dictionary: output -> (quantity, [(input, quantity)...]).'''
    formulas = {}
    for line in lines:
        (out_p, out_q), inputs = ParseLine(line)
        assert out_p not in formulas
        formulas[out_p] = (out_q, inputs)
    assert 'ORE' not in formulas
    formulas['ORE'] = (1, ())
    return formulas

def FindDependants(formulas):
    '''Returns a dictionary: a -> [b, ..], for all `b` that have a dependency on `a` in formulas.'''
    dependants = defaultdict(list)
    for a, (_, deps) in formulas.items():
        for b, _ in deps:
            dependants[b].append(a)
    return dependants

def TopSort(dependants, initial_product):
    '''Returns a topologically ordered list of products, such that if `a` has a dependency on `b`,
       `a` will occur earlier in the list. (As a result, ORE will appear near the end.)'''
    result = []
    visited = set()
    closed = set()
    def Dfs(a):
        if a in closed:
            return
        assert a not in visited  # detects cycles
        visited.add(a)
        for b in dependants[a]:
            Dfs(b)
        closed.add(a)
        result.append(a)
    Dfs(initial_product)
    return result

# Note: we expect that the input formulas form a DAG (directed acyclic graph).
formulas = ParseLines(sys.stdin)
ordered_products = TopSort(FindDependants(formulas), 'ORE')

def CalculateNeededOre(wanted_fuel):
    needed = defaultdict(int, {'FUEL': wanted_fuel})
    for product in ordered_products:
        quantity, deps = formulas[product]
        times = (needed[product] + quantity - 1) // quantity
        for dep_product, dep_quantity in deps:
            needed[dep_product] += times * dep_quantity
    return needed['ORE']

def CalculateMaximumFuel(available_ore):
    # Binary search for the maximum amount of fuel we can produce with the given amount of ore.
    hi = 1
    while CalculateNeededOre(wanted_fuel=hi) <= available_ore:
        hi *= 2
    lo = 0
    while lo < hi:
        mid = (hi + lo) // 2
        if CalculateNeededOre(wanted_fuel=mid) <= available_ore:
            lo = mid + 1
        else:
            hi = mid
    return lo - 1

# Part 1
print(CalculateNeededOre(wanted_fuel = 1))

# Part 2
print(CalculateMaximumFuel(available_ore = 10**12))
