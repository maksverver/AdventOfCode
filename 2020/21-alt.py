import re
import sys

class Product:
    def __init__(self, ingredients, allergens):
        self.ingredients = set(ingredients)
        self.allergens = set(allergens)

    def parse(line):
        m = re.match(r'(?P<ingredients>(\w+ )*)[(]contains (?P<allergens>(\w+, )*\w+)[)]$', line)
        return Product(m.group('ingredients').split(), m.group('allergens').split(', '))

products = [Product.parse(line) for line in sys.stdin]

unidentified_ingredients = set(i for p in products for i in p.ingredients)
unidentified_allergens   = set(a for p in products for a in p.allergens)

# ingredient -> allergen, if exactly 1 ingredient is possible
allergen_by_ingredient = {}

# allergen -> set of possible ingredients
possible_ingredients = dict(
    (a, set.intersection(*[p.ingredients for p in products if a in p.allergens]))
    for a in unidentified_allergens)

# More efficient solution than 21.py. Instead of recomputing sets of possible
# ingredients, we store them (in `possible_ingredients`, defined above), and
# update them iteratively, for an O(A^2) algorithm.
identified_allergens = []
for a, pi in possible_ingredients.items():
    if len(pi) == 1:
        unidentified_allergens.remove(a)
        identified_allergens.append(a)
for a in identified_allergens:
    i, = possible_ingredients[a]
    #print('ingredient', i, 'contains allergen', a)
    assert i in unidentified_ingredients
    unidentified_ingredients.remove(i)
    allergen_by_ingredient[i] = a
    for b, pib in possible_ingredients.items():
        if b in unidentified_allergens and i in pib:
            pib.remove(i)
            if len(pib) == 1:
                unidentified_allergens.remove(b)
                identified_allergens.append(b)
assert not unidentified_allergens

# Part 1: print total occurrences of inert ingredients
print(sum(len(unidentified_ingredients.intersection(p.ingredients)) for p in products))

# Part 2: print list of dangerous ingredients, ordered by allergen name
print(','.join(sorted(allergen_by_ingredient, key=lambda i: allergen_by_ingredient[i])))
