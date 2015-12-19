# Let a, b, c, etc. denote any atom except Rn, Y and Ar.
# Then all rules in the input are in one of two forms:
#
# Kind 1:
#	a -> b c
#
# Kind 2:
#	a -> b Rn c Ar
#	a -> b Rn c Y d Ar
#	a -> b Rn c Y d Y e Ar
#	... or generally:
#	a -> b Rn x (Y x)* Ar
#
# The second rule has the form of a function expression, where Rn and Ar act as
# parentheses, and Y acts as a comma separating the parameters to the function.
#
# This means that if the input is well-formed, then we can parse the string
# inside out to find its derivation. However, we don't actually need to parse,
# because all we want to know is the cost of reducing a string to a single atom,
# and we can do that using the general forms of the rules:
#
# An application of kind 1 reduces the number of atoms by 1 (from 2 to 1).
# An application of kind 2 reduces the number of atoms by 1 + 2x (from 2 + 2x
# to 1) where x is the number of parameters of the function. Since the number of
# parameters is equal to the number of commas plus 1, we can state equivalently
# that the number of atoms is reduced by 2 + 2y where y is the number of commas
# in the reduction rule.
#
# Since every application of kind 2 removes one set of parentheses, we can
# calculate the total number of applications required to reduce the input to
# one atom as:
#
#   length of the input - 2*(#sets of parentheses) - 2*(#commas) - 1

import sys
for l in sys.stdin: pass
print sum(c.isupper() for c in l) - 2*l.count('Rn') - 2*l.count('Y') - 1
