import sys

def Eq(x): return lambda y: y == x
def Gt(x): return lambda y: y > x
def Lt(x): return lambda y: y < x

required = {
	"children":    Eq(3),
	"cats":        Gt(7),
	"samoyeds":    Eq(2),
	"pomeranians": Lt(3),
	"akitas":      Eq(0),
	"vizslas":     Eq(0),
	"goldfish":    Lt(5),
	"trees":       Gt(3),
	"cars":        Eq(2),
	"perfumes":    Eq(1),
}

for line in sys.stdin:
	name, rest = line.split(':', 1)
	for part in rest.split(','):
		prop, value = (s.strip() for s in part.split(':'))
		value = int(value.strip())
		if not required[prop](value): break
	else:
		print name
