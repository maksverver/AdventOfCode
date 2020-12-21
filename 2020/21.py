import re
import sys

class Product:
    def __init__(self, ingredients, allergens):
        self.ingredients = ingredients
        self.allergens = allergens

    def parse(line):
        m = re.match(r'(?P<ingredients>(\w+ )*)[(]contains (?P<allergens>(\w+, )*\w+)[)]$', line)
        return Product(m.group('ingredients').split(), m.group('allergens').split(', '))

products = [Product.parse(line) for line in sys.stdin]

unidentified_ingredients = set(i for p in products for i in p.ingredients)
unidentified_allergens = set(a for p in products for a in p.allergens)
allergen_by_ingredient = {}
while unidentified_allergens:
    for a in unidentified_allergens:
        possible_ingredients = set(unidentified_ingredients)
        for p in products:
            if a in p.allergens:
                possible_ingredients.intersection_update(p.ingredients)
        assert possible_ingredients
        if len(possible_ingredients) == 1:
            i, = possible_ingredients
            #print('ingredient', i, 'contains allergen', a)
            allergen_by_ingredient[i] = a
            unidentified_allergens.remove(a)
            unidentified_ingredients.remove(i)
            break
    else:
        assert False

# Part 1: print total occurrences of inert ingredients
print(sum(len(unidentified_ingredients.intersection(p.ingredients)) for p in products))

# Part 2: print list of dangerous ingredients, ordered by allergen name
print(','.join(sorted(allergen_by_ingredient, key=lambda i: allergen_by_ingredient[i])))
