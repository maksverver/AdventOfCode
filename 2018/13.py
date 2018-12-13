import sys

class Cart(object):
    def __init__(self, r, c, d):
        self.r = r  # row
        self.c = c  # col
        self.d = d  # direction
        self.t = 0  # turns

    def Pos(self):
        return (self.r, self.c)

    def Step(self):
        self.r += self.d == 'v'
        self.r -= self.d == '^'
        self.c += self.d == '>'
        self.c -= self.d == '<'
        ch = grid[self.r][self.c]
        if ch == '-':
            assert self.d in '<>'
        elif ch == '|':
            assert self.d in '^v'
        elif ch == '/':
            self.d = '^v><'['><^v'.index(self.d)]
        elif ch == '\\':
            self.d = 'v^<>'['><^v'.index(self.d)]
        elif ch == '+':
            dirs = '>v<^'
            self.d = dirs[(dirs.index(self.d) - 1 + self.t) % 4]
            self.t = (self.t + 1)%3
        else:
            print('Should not get here: ', self.r, self.c, self.d, ch)
            assert False

carts = []
grid = [list(line) for line in sys.stdin]
for r, row in enumerate(grid):
    for c, ch in enumerate(row):
        ch = grid[r][c]
        if ch in '><^v':
            carts.append(Cart(r, c, ch))
            grid[r][c] = "--||"["><^v".index(ch)]

first_crash = None
occupied = set(cart.Pos() for cart in carts)
while len(carts) > 1:
    for cart in sorted(carts, key=Cart.Pos):
        if not cart.Pos() in occupied:
            # Someone crashed into me :/
            continue
        occupied.remove(cart.Pos())
        cart.Step()
        if cart.Pos() not in occupied:
            occupied.add(cart.Pos())
        else:
            # I crashed into someone /:
            occupied.remove(cart.Pos())
            if first_crash is None:
                first_crash = cart.Pos()
    carts = [cart for cart in carts if cart.Pos() in occupied]

print("{1},{0}".format(*first_crash))
print("{1},{0}".format(*carts[0].Pos()))
