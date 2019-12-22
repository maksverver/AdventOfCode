import sys

N = 10007
cards = list(range(N))

def DealIntoNewStack():
    return list(reversed(cards))

def Cut(n):
    return cards[n:] + cards[:n]

def DealWithIncrement(n):
    assert n > 0
    result = [None]*len(cards)
    for i, v in enumerate(cards):
        result[i * n % N] = v
    return result

for line in sys.stdin:
    words = line.split()
    if len(words) == 4 and words[0] == 'deal' and words[1] == 'into' and words[2] == 'new' and words[3] == 'stack':
        cards = DealIntoNewStack()
    elif len(words) == 2 and words[0] == 'cut':
        cards = Cut(int(words[1]))
    elif len(words) == 4 and  words[0] == 'deal' and words[1] == 'with' and words[2] == 'increment':
        cards = DealWithIncrement(int(words[3]))
    else:
        print("Couldn't parse:", line)
        sys.exit(1)

print(cards.index(2019))
