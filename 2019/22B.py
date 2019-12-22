import sys

N = 119315717514047  # Number of cards in deck
K = 101741582076661  # Number of copies of instructions
I = 2020             # Card index to look up

def ParseLine(line):
    '''Returns a pair (a, b), such that the matrix multiplication:

           | a b |   | i |
           | 0 1 | × | 1 | = | i' 1 |

        Transforms a card index to its previous index.'''
    words = line.split()
    if len(words) == 4 and words[0] == 'deal' and words[1] == 'into' and words[2] == 'new' and words[3] == 'stack':
        return (-1, N - 1)   # N - 1 - i
    if len(words) == 2 and words[0] == 'cut':
        a = int(words[1])
        return (1, a)  # i + a
    if len(words) == 4 and  words[0] == 'deal' and words[1] == 'with' and words[2] == 'increment':
        a = int(words[3])
        return (InvModN(a), 0)   # i/a
    return None

def InvModN(a):
    # Use Fermat's little theorem to find the multiplicative inverse of `a` modulo N.
    # Note that this assumes N is prime!
    b = pow(a, N - 2, N)
    assert a * b % N == 1
    return b

def MatMulModN(a, b, c, d):
    '''Returns the pair (e,f) that is the result of the matrix multiplication:

        |a b|   |c d|   |(a×c + b×0) (a×d + b×1)|   |e f|
        |0 1| × |0 1| = |(0×c + 1×0) (0×d + 1×1)| = |0 1|
    '''
    return (a*c%N, (a*d + b)%N)

def MatPowModN(a, b, k):
    '''Returns the pair (c, d) that is the result of the matrix exponentiation:

        |a b|^k   |c d|
        |0 1|   = |0 1|
    '''
    # Use multiplication by squaring to calculate the result in O(log K) time.
    c, d = 1, 0
    while k > 0:
        if k % 2 == 1:
            c, d = MatMulModN(c, d, a, b)
        a, b = MatMulModN(a, b, a, b)
        k //= 2
    return c, d

a, b = 1, 0
for c, d in map(ParseLine, sys.stdin):
    a, b = MatMulModN(a, b, c, d)
a, b = MatPowModN(a, b, K)
print((a*I + b)%N)
