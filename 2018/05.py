from string import ascii_lowercase
import sys

def React(string):
    rest = []
    for c in string:
        if rest and c.swapcase() == rest[-1]:
            rest.pop()
        else:
            rest.append(c)
    return ''.join(rest)

def RemoveLetter(string, letter):
    return ''.join(c for c in string if c.lower() != letter)

S = React(sys.stdin.readline().strip())
print(len(S))
print(min(len(React(RemoveLetter(S, letter))) for letter in ascii_lowercase))
