import sys

required = {
	"children":    3,
	"cats":        7,
	"samoyeds":    2,
	"pomeranians": 3,
	"akitas":      0,
	"vizslas":     0,
	"goldfish":    5,
	"trees":       3,
	"cars":        2,
	"perfumes":    1,
 }

for line in sys.stdin:
	name, rest = line.split(':', 1)
	for part in rest.split(','):
		prop, value = (s.strip() for s in part.split(':'))
		value = int(value.strip())
		if required[prop] != value: break
	else:
		sue, number = name.split()
		print number
